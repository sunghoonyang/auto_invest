import unittest
from datetime import datetime, timedelta
from src.krx.krx_api_talker import KrxApiTalker as krx


class TestApiToDb(unittest.TestCase):
    def setUp(self):
        self.update_tbs = ['tbl_dailystock', 'tbl_timeconclude']

    def tearDown(self):
        pass

    def test_00_api_to_mysql(self):
        rc = krx.api_to_mysql(self.update_tbs)
        print(rc)