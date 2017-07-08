import unittest

from src.cybos.stock_chart_config import StockChartConfig


class TestStockChartConfig(unittest.TestCase):
    def test_get_stock_chart_options(self):
        kwargs = {'1': '2', '4': 10}
        options = StockChartConfig.get_df_options('stock', **kwargs)
        self.assertFalse(options.get('7', False))
        kwargs.update({'7': True})
        options = StockChartConfig.get_df_options('stock', **kwargs)
        self.assertTrue(options.get('7', False))


if __name__ == '__main__':
    unittest.main()