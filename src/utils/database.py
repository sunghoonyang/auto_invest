from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from src.cybos.cybos_talker import CybosTalker


class dbMeta(object):
    @classmethod
    def get_mysql_engine(cls):
        conn_args = dict(host='localhost',
                         user='root',
                         port=3306,
                         password='Admin1234',
                         db='cybos',
                         charset='utf8mb4',
                         )
        conn_str = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset={charset}'.format(**conn_args)
        engine = create_engine(conn_str, echo=False)
        return engine

    @classmethod
    def execute_sql(cls, engine, sql):
        conn = engine.raw_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as e:
            cur.rollback()
            print(e)
            res = None

        conn.close()
        return res

    @classmethod
    def replace_cybos_column_names(cls, df):
        def replace_char(s):
            chars = [' ', '-', '/']
            rv = ''
            for c in s:
                rv += '_' if c in chars else c
            return rv

        col_list = {c: replace_char(c) for c in df.columns.values}
        df.rename(columns=col_list, inplace=True)
        return df

    @classmethod
    def get_market_eye_res(cls, stock_code):
        dfs = []
        query_time = datetime.now()
        for i in range(0, 4):
            min_col = i * 40
            max_col = min((i + 1) * 40, 147)
            all_params = {
                '0': tuple(range(min_col, max_col))
            }
            ct = CybosTalker()
            if isinstance(stock_code, tuple):
                assert len(stock_code) <= 200, 'array of stocks must be not greater than 200 stocks.'
            dfs.append(ct.get_per_eps_as_dataframe(stock_code, **all_params))
        ts_d = {'load_dt': [query_time] * len(stock_code)}
        ts_df = pd.DataFrame(data=ts_d, index=list(range(0, len(stock_code))))
        dfs.append(ts_df)
        df = pd.concat(dfs, axis=1)
        return cls.replace_cybos_column_names(df)

    @classmethod
    def snapshot_market_eye_res(cls):
        ct_obj = CybosTalker()
        engine = dbMeta.get_mysql_engine()
        stock_list = ct_obj.get_domestic_stock_list()
        global_stocks = list(stock_list.values())
        batch_size = int(len(global_stocks) / 200) + 1
        dups = cls.get_today_data()
        dups.drop(['LOAD_DT', 'QUERY_DT', 'SEQ'], axis=1, inplace=True, errors='ignore')
        for i in range(0, batch_size):
            lower, upper = i * 200, min((i + 1) * 200, len(global_stocks))
            df = dbMeta.get_market_eye_res(global_stocks[lower:upper])
            df['시간'] = df['시간'].apply(pd.to_numeric)
            pks = ['종목코드', '시간']
            df = df.merge(dups
                          , how='left'
                          , on=pks
                          , suffixes=('_L', '_R')
                          )
            df = df[pd.isnull(df['현재가_R'])]
            drop_cols = [c for c in df.columns.values if c.endswith('_R')]
            df.drop(drop_cols, axis=1, inplace=True, errors='ignore')
            rename_cols = {c: c[:-2] for c in df.columns.values if c.endswith('_L')}
            df.rename(columns=rename_cols, inplace=True)
            df.to_sql('market_eye_today'
                      , engine
                      , if_exists='append'
                      , index=False
                      )
        ct_obj = None


    @classmethod
    def get_today_data(cls):
        sql = """
        SELECT 
            * 
            FROM cybos.market_eye_today
        """
        engine = dbMeta.get_mysql_engine()
        df = pd.read_sql(sql, engine)
        return df

    @classmethod
    def call_proc(cls, proc_name, args=None):
        try:
            connection = cls.get_mysql_engine().raw_connection()
            cursor = connection.cursor()
            cursor.callproc(proc_name, args)
            res = cursor.fetchall()
            cursor.close()
            connection.close()
            return res
        except Exception as e:
            print(str(e))
            connection.rollback()
            connection.close()
            raise