#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GET XML FROM API
"""
import numpy as np
import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd
from src.utils.database import dbMeta
from sqlalchemy import Table
from datetime import date
import logging

logger = logging.getLogger('krx')


class KrxApiTalker(object):
    _STOCK_LIST = None

    @classmethod
    def get_krx_stock_list(cls):
        if cls._STOCK_LIST is None:
            cls._STOCK_LIST = dbMeta.get_krx_stock_list('코스닥')
        return cls._STOCK_LIST

    @classmethod
    def call_krx_api(cls, code):
        code_request_url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng'
        code = str(np.asscalar(code))
        code = '0' * (6 - len(code)) + code
        code_request_url = "%s?code=%s" % (code_request_url, code)
        opener = urllib.request.build_opener()
        request = urllib.request.Request(code_request_url)
        response = opener.open(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            return response_body
        else:
            logger.error("Error Code:" + rescode)
            raise

    @classmethod
    def xml2df(cls, xml_data, update_tbs):
        """
        XML to DataFrame
        """
        try:
            root = ET.XML(xml_data.strip())
        except ET.ParseError as e:
            logger.error(str(e))
            return None
        all_records = {}
        for child in [child for child in root if child.tag.lower() in update_tbs]:
            records = []
            for subchild in child:
                row = {}
                for name, value in subchild.items():
                    if value == '':
                        value = '0'
                    row[name] = value.replace(',', '')
                records.append(row)
            key = str(child.tag.lower())
            all_records.update({key: records})

        return all_records

    @classmethod
    def api_to_mysql(cls, update_tbs):
        code_df = cls.get_krx_stock_list()
        codes = code_df['종목코드']
        df_dict = dict(zip(update_tbs, [pd.DataFrame()] * len(update_tbs)))
        for c in codes:
            stock_name = code_df[code_df['종목코드'] == c]['종목명'].iloc[0]
            res = cls.call_krx_api(c)
            all_records = cls.xml2df(res, update_tbs)
            if not all_records:
                continue # all_records returned zero due to xml parse error
            for k, v in all_records.items():
                if k.lower() not in update_tbs:
                    continue
                if len(v) == 0:
                    logger.debug('%s returned an empty data set.' % stock_name)
                    break
                stock_cd = {'item_cd': [c] * len(v)}
                df = pd.concat([pd.DataFrame(data=stock_cd, index=list(range(0, len(v)))), pd.DataFrame(data=v)]
                               , axis=1)
                master = df_dict[k]
                df_dict[k] = master.append(df, ignore_index=True)

        """TIME STRING TO DATETIME OBJ"""
        df_timeconclude = df_dict['tbl_timeconclude']
        df_timeconclude['time'] = df_timeconclude['time'].apply(lambda x: " ".join([date.today().strftime('%Y-%m-%d'), x]))
        df_dict['tbl_timeconclude'] =  df_timeconclude

        engine = dbMeta.get_mysql_engine()
        rc = {}
        target_tb_dict = {
            'tbl_timeconclude': {'tb_nm': 'krx_timeconclude_today', 'dt_col': 'time'}
            , 'tbl_dailystock': {'tb_nm': 'krx_dailystock_today', 'dt_col': 'day_Date'}
        }

        metadata = dbMeta.get_metadata()
        for tb, df in df_dict.items():
            logger.debug('replacing {tb}'.format(tb=tb.lower()))
            df.to_sql(tb.lower()
                      , engine
                      , if_exists='append'
                      , index=False
                      )

            logger.debug('%d inserted to %s' % (df.shape[0], tb.lower()))
            join_insert_sql = """
            INSERT INTO cybos.{tgt}
            SELECT 
                s.*
            FROM cybos.{src} s 
            LEFT OUTER JOIN cybos.{tgt} t
            ON s.item_cd = t.item_cd
            AND s.{dt_col} = t.{dt_col}
            WHERE t.{dt_col} IS NULL
            ;
            TRUNCATE TABLE cybos.{src}
            ;
            """.format(tgt=target_tb_dict[tb.lower()]['tb_nm']
                       , src=tb.lower()
                       , dt_col=target_tb_dict[tb.lower()]['dt_col'])
            logger.debug('Inserted to {tgt} : {sql}'.format(
                    tgt=target_tb_dict[tb.lower()]['tb_nm']
                    , sql=join_insert_sql.strip().replace("\n", "")
                )
            )
            dbMeta.execute_sql(engine, join_insert_sql)
            rc.update({tb: df.shape[0]})
        return rc


if __name__ == '__main__':
    pass

