import unittest
from datetime import datetime, timedelta

from src.cybos.cybos_talker import CybosTalker


class TestCybosTalker(unittest.TestCase):
    def setUp(self):
        self.test_obj = CybosTalker()
        self.test_stock_name = 'SK케미칼'
        self.test_stock_code = 'A006120'
        self.today = int(datetime.today().strftime('%Y%m%d'))
        self.yesterday = int((datetime.today() - timedelta(1)).strftime('%Y%m%d'))
        self.month_ago = int((datetime.strptime(str(self.yesterday), "%Y%m%d") - timedelta(days=30)).strftime("%Y%m%d"))

    def tearDown(self):
        self.test_obj = None

    @unittest.skip
    def test_01_get_domestic_stock_list(self):
        self.test_stock_dict = {self.test_stock_name: self.test_obj.get_domestic_stock_list()[self.test_stock_name]}
        print(self.test_obj.get_domestic_stock_list())
        self.assertEqual(self.test_stock_code, self.test_stock_dict[self.test_stock_name])

    @unittest.skip
    def test_02_get_stock_chart_as_dataframe(self):
        test_req_type_range, test_req_type_head = 'range', 'head'
        dur_df = self.test_obj.get_chart_as_dataframe(self.test_stock_code, test_req_type_range, self.month_ago, self.yesterday)
        # self.assertEqual(22, len(dur_df), 'Check if the days were business days')
        # self.assertFalse(dur_df.empty)
        head_df = self.test_obj.get_chart_as_dataframe(self.test_stock_code, test_req_type_head, 10)
        print(head_df.head(20))
        self.assertEqual(10, len(head_df))
        self.assertFalse(head_df.empty)

    @unittest.skip
    def test_03_get_per_eps(self):
        df = self.test_obj.get_per_eps_as_dataframe(self.test_stock_code)
        self.assertEqual(1, len(df))
        self.assertEqual(df.iloc[0, 0], self.test_stock_code)

    @unittest.skip
    def test_04_get_bt_dataframe(self):
        start_date = self.month_ago
        df = self.test_obj.get_bt_dataframe(self.test_stock_code, 'range', start_date, self.today)
        print(df)

    @unittest.skip
    def test_05_get_ten_days_min_by_min(self):
        start_date = self.month_ago
        df = self.test_obj.get_ten_days_min_by_min(self.test_stock_code, 'range', start_date, self.today)
        print(df)

    # @unittest.skip
    def test_06_retry_connection(self):
        CybosTalker.retry_connection()

if __name__ == '__main__':
    unittest.main()