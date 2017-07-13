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

class KrxApiTalker(object):
    @classmethod
    def call_krx_api(cls, code):
        code_request_url = 'http://asp1.krx.co.kr/servlet/krx.asp.XMLSiseEng'
        code = str(np.asscalar(code))
        code = '0' * (6 - len(code)) + code
        code_request_url = "%s?code=%s" % (code_request_url, code)
        print(code_request_url)
        opener = urllib.request.build_opener()
        request = urllib.request.Request(code_request_url)
        response = opener.open(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read()
            return response_body
        else:
            print("Error Code:" + rescode)
            raise

    @classmethod
    def xml2df(cls, xml_data, update_tbs):
        """
        XML to DataFrame
        """
        try:
            root = ET.XML(xml_data.strip())
        except ET.ParseError as e:
            print(str(e))
            return None
        all_records = {}
        for child in [child for child in root if child.tag in update_tbs]:
            records = []
            for subchild in child:
                row = {}
                for name, value in subchild.items():
                    row[name] = value
                records.append(row)
            key = str(child.tag)
            all_records.update({key: records})

        return all_records

    @classmethod
    def api_to_mysql(cls, update_tbs):
        code_df = dbMeta.get_krx_stock_list('코스닥')
        codes = code_df['종목코드']
        df_dict = dict(zip(update_tbs, [pd.DataFrame()] * len(update_tbs)))
        for c in codes:
            stock_name = code_df[code_df['종목코드'] == c]['종목명'].iloc[0]
            res = cls.call_krx_api(c)
            all_records = cls.xml2df(res, update_tbs)
            if not all_records:
                continue # all_records returned zero due to xml parse error
            for k, v in all_records.items():
                if k not in update_tbs:
                    continue
                if len(v) == 0:
                    print('%s returned an empty data set.' % stock_name)
                    break
                stock_cd = {'item_cd': [c] * len(v)}
                df = pd.concat([
                                    pd.DataFrame(data=stock_cd, index=list(range(0, len(v))))
                                    , pd.DataFrame(data=v)
                                ]
                               , axis=1)
                df_dict[k] = df_dict[k].append(df, ignore_index=True)
        engine = dbMeta.get_mysql_engine()
        rc = {}
        for tb, df in df_dict:
            df.to_sql(tb.lower()
                        , engine
                        , if_exists='append'
                        , index=False
                        )
            rc.update({tb: df.shape[0]})
        return rc

if __name__ == '__main__':
    pass

