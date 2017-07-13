import random as rnd
import unittest
import pandas as pd
from src.cybos.cybos_talker import CybosTalker
from src.utils.database import dbMeta


class TestDatabase(unittest.TestCase):
    def setUp(self):
        try:
            self.ct_obj = CybosTalker()
            stock_list = self.ct_obj.get_domestic_stock_list()
            self.test_stock_codes = rnd.sample(list(stock_list.values()), 200)
        except AssertionError as e:
            self.ct_obj = None
            self.test_stock_codes = None
            print(str(e))


    def tearDown(self):
        self.ct_obj = None

    @unittest.skip
    def test_00_get_market_eye_res(self):
        df = dbMeta.get_market_eye_res(self.test_stock_codes)
        print(df.head(20))


    @unittest.skip
    def test_01_snapshot_market_eye_res(self):
        dbMeta.snapshot_market_eye_res()

    @unittest.skip
    def test_02_get_today_date(self):
        df = dbMeta.get_today_date()

    @unittest.skip
    def test_03_execute_sql(self):
        sql = """
        SELECT 
            * 
        FROM cybos.vw_latest_stock_info;
        """
        engine = dbMeta.get_mysql_engine()
        res = dbMeta.execute_sql(engine, sql)
        self.assertEqual(len(res), 863)

    def test_04_get_krx_stock_list(self):
        df = dbMeta.get_krx_stock_list('코스피')
        print(df.head(10))