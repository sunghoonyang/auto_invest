import unittest
from datetime import datetime, timedelta

import backtrader as bt
from src.backtester.observer import OrderObserver

from src.backtester.strategy import SMACrossOver, MyStrategy, TestStrategy, SMACloseSignal, SMAExitSignal, MAINSIGNALS, \
    EXITSIGNALS
from src.cybos.cybos_talker import CybosTalker


class TestBackTrader(unittest.TestCase):

    def setUp(self):
        self.__cybos_talker__ = CybosTalker()
        self.test_stock_name = '카카오톡'
        # self.test_stock_name = '삼성전자'
        self.test_stock_code = 'A035720'
        # self.test_stock_code = 'A005930'
        self.today = int(datetime.today().strftime('%Y%m%d'))
        self.yesterday = int((datetime.today() -timedelta(1)).strftime('%Y%m%d'))
        self.month_ago = int((datetime.strptime(str(self.yesterday), "%Y%m%d") - timedelta(weeks=4)).strftime("%Y%m%d"))
        self.year_ago = int((datetime.strptime(str(self.yesterday), "%Y%m%d") - timedelta(weeks=52)).strftime("%Y%m%d"))
        self.two_years_ago = int((datetime.strptime(str(self.yesterday), "%Y%m%d") - timedelta(weeks=104)).strftime("%Y%m%d"))
        self.__df_range__ = self.__cybos_talker__.get_bt_dataframe(self.test_stock_code, 'range', self.two_years_ago, self.today)
        self.__df_head__ = self.__cybos_talker__.get_bt_dataframe(self.test_stock_code, 'head', 365)

    def tearDown(self):
        self.__cybos_talker__ = None

    @unittest.skip
    def test_01_plot_cerebro_head(self):
        self.cerebro_head = bt.Cerebro(stdstats=False)
        self.cerebro_head.addstrategy(bt.Strategy)
        self.head_feed = bt.feeds.PandasData(dataname=self.__df_head__)
        print(self.__df_head__)
        self.cerebro_head.adddata(self.head_feed)
        self.cerebro_head.run()
        self.cerebro_range.plot(style='bar')

    @unittest.skip
    def test_02_plot_cerebro_range(self):
        self.cerebro_range = bt.Cerebro(stdstats=False)
        self.range_feed = bt.feeds.PandasDirectData(dataname=self.__df_range__)
        print(self.__df_range__)
        self.cerebro_range.adddata(self.range_feed)
        self.cerebro_range.run()
        self.cerebro_range.plot(style='bar')

    @unittest.skip
    def test_03_SmaCross(self):
        self.test_cerebro = bt.Cerebro()
        self.range_feed = bt.feeds.PandasData(dataname=self.__df_range__)
        self.test_cerebro.adddata(self.range_feed)
        self.test_cerebro.addstrategy(SMACrossOver)
        self.test_cerebro.run()
        self.test_cerebro.plot()

    @unittest.skip
    def test_04_my_strategy(self):
        self.test_cerebro = bt.Cerebro()
        self.test_cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
        # self.test_cerebro.addsizer(bt.sizers.PercentSizer, percents=85)
        self.test_cerebro.addstrategy(MyStrategy)
        self.range_feed = bt.feeds.PandasData(dataname=self.__df_range__)
        self.test_cerebro.adddata(self.range_feed)
        self.test_cerebro.addobserver(OrderObserver)
        self.test_cerebro.broker.setcash(100000000.0)
        # set commission scheme -- CHANGE HERE TO PLAY
        commission = 0.0016
        self.test_cerebro.broker.setcommission(commission=commission)
        # Run over everything
        self.test_cerebro.run()
        self.test_cerebro.plot()

    @unittest.skip
    def test_05_test_strategy(self):
        self.test_cerebro = bt.Cerebro()
        self.test_cerebro.addstrategy(TestStrategy)
        self.range_feed = bt.feeds.PandasData(dataname=self.__df_range__)
        self.test_cerebro.adddata(self.range_feed)
        # self.test_cerebro.addobserver(OrderObserver)
        self.test_cerebro.broker.setcash(100000000.0)
        # set commission scheme -- CHANGE HERE TO PLAY
        commission, margin, mult = 0.0016, None, 1
        self.test_cerebro.broker.setcommission(commission=commission
                                               , margin=margin
                                               , mult=mult)
        # Run over everything
        self.test_cerebro.run()
        self.test_cerebro.plot()

    # @unittest.skip
    def test_06_test_signal_strategy(self):
        self.range_feed = bt.feeds.PandasData(dataname=self.__df_range__)

        def run_cerebro(p1, p2):
            test_cerebro = bt.Cerebro()
            test_cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
            test_cerebro.broker.set_cash(100000000)
            test_cerebro.adddata(self.range_feed)
            test_cerebro.add_signal(MAINSIGNALS['longonly'],
                                         SMACloseSignal, period=p2)

            test_cerebro.add_signal(EXITSIGNALS['longexit'],
                                         SMAExitSignal,
                                         p1=p1,
                                         p2=p2)
            commission, margin, mult = 0.0016, None, 1
            test_cerebro.broker.setcommission(commission=commission
                                              , margin=margin
                                              , mult=mult)
            test_cerebro.run()
            return test_cerebro

        max_val_period, max_val, max_cerebro = 0, 0, None

        for p2 in range(2, 10):
            for p1 in range(1, p2 + 1):
                test_cerebro = run_cerebro(p1, p2)
                print('%d is the portfolio value if SMA_long is %d and SMA_short is %d'
                      % (test_cerebro.broker.get_value(), p2, p1))
                if test_cerebro.broker.get_value() > max_val:
                    max_val = test_cerebro.broker.get_value()
                    # max_val_period_short = p1
                    # max_val_period_long = p2
                    max_cerebro = test_cerebro
        max_cerebro.plot(style='bar')

if __name__ == '__main__':
    unittest.main()