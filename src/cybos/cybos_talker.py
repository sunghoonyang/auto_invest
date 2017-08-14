from datetime import datetime, timedelta
from functools import partial
import numpy as np
import subprocess
import os
import time
import pandas as pd
from src.cybos.cybos_helpers import *
from src.cybos.stock_chart_config import StockChartConfig as config


class CybosTalker(object):
    """
    CybosTalker is instantiated with attributes that are dispatched DLL clients.
    """
    @classmethod
    def get_df_options(cls, option_type, **kwargs):
        return config.get_df_options(option_type, **kwargs)

    @staticmethod
    def connected_to_cybos():
        import win32com.client
        return win32com.client.Dispatch("CpUtil.CpCybos").IsConnect == 1

    @staticmethod
    def __hts_running():
        p = subprocess.Popen('TASKLIST /FI "imagename eq Bos.exe"', stdout=subprocess.PIPE)
        res = p.communicate()[0]
        return 'Bos.exe' in str(res)

    @staticmethod
    def retry_connection():
        if CybosTalker.__hts_running():
            os.system("TASKKILL /F /IM Bos.exe")
            time.sleep(10)
        ahk_path = "C:\\Users\\sh\\Documents\\devbox\\ahk"
        ahk_exe_path = "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe"
        subprocess.call([ahk_exe_path, os.path.join(ahk_path, 'cp_start.ahk')])
        time.sleep(10)
        subprocess.call([ahk_exe_path, os.path.join(ahk_path, "cp_login.ahk")])

    def __init__(self):
        import win32com.client
        self.instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        self.instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        self.instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")


    @assert_cybos_connection
    def __block_request(self, chart_type, **option_dict):
        """
        Converts stockChart to DataFrame
        :return: DataFrame
        """
        """     get response    """
        df_options = config.get_df_options(chart_type, **option_dict)
        client = self.instStockChart if chart_type == 'stock' else self.instMarketEye
        for k, v in df_options.items():
            client.SetInputValue(int(k), v)
        client.BlockRequest()

    @assert_cybos_connection
    def get_domestic_stock_list(self):
        """
        Returns a dictionary of all listed stock name as key, and code as value.
        :return: dictionary(name_of_code: code)
        """
        return {self.instCpCodeMgr.CodeToName(code): code
                for code in self.instCpCodeMgr.GetStockListByMarket(1)
                if self.instCpCodeMgr.GetStockSectionKind(code) == 1}

    @assert_cybos_connection
    def get_chart_as_dataframe(self, stock_code, req_type, *args, **kwargs):
        """
        Gets the Stock Chart of the specified parameters as Pandas.DataFrame
        :param stock_code: Stock code
        :param req_code: Duration or head.
        :param kwargs: 0. 날짜: date 1. 시간: time 2. 시가: open 3. 고가: high 4. 저가: low 5. 종가: close 6. 전일대비: net_change 8. 거래량: volume 9. 거래대금: trading_value 10. 누적체결매도수량: cv
        :return: pandas.DataFrame of the Stock Chart.
        """
        """     Mandatory Params        """
        chart_type = 'stock'
        req_dict = {'0': stock_code}
        if req_type == 'range':
            req_code = '1'
            assert len(args) == 2, 'Provide start_date and end_date as YYYYMMDD'
            start_date, end_date = args
            req_dict.update({'1': req_code, '2': end_date, '3': start_date})
        elif req_type == 'head':
            req_code = '2'
            assert len(args) == 1, 'Provide number of head rows.'
            head = args[0]
            req_dict.update({'1': req_code, '4': head})
        else:
            raise ValueError('%s : req_code is either range or head.' % stock_code)

        """      Get Param Dict      """
        
        option_dict = kwargs.copy()
        option_dict.update(req_dict)
        self.__block_request(chart_type, **option_dict)
        numField = self.instStockChart.GetHeaderValue(1)
        numData = self.instStockChart.GetHeaderValue(3)
        GetDataValueHelper = lambda type, index: self.instStockChart.GetDataValue(type, index)
        x = np.array(
            [p(y) for p in [partial(GetDataValueHelper, index=x) for x in range(numData)] for y in range(numField)]) \
            .reshape(numData, numField)
        df = pd.DataFrame(x, columns=list(self.instStockChart.GetHeaderValue(2)))

        def add_hour(date, time):
            return datetime.strptime(str(int(float(date))), "%Y%m%d") + timedelta(hours=np.asscalar(time))
        # df['datetime'] = list(map(add_hour, df['날짜'], df['시간']))
        df.insert(0, 'datetime', list(map(add_hour, df['날짜'], df['시간'])))
        df.drop(['날짜', '시간'], axis=1, inplace=True, errors='ignore')
        return df

    @assert_cybos_connection
    def get_per_eps_as_dataframe(self, stocks, **kwargs):
        """
        return DataFrame of PER and EPS whose zeroth column is stock code.
        :param stocks: stock, or tuple of stocks
        :param kwargs: MarketEye params
        :return: pd.DataFrame
        """
        if not isinstance(stocks, list):
            stocks = [stocks]
        chart_type = 'per_eps'
        option_dict = kwargs.copy()
        option_dict.update({'1': stocks})
        self.__block_request(chart_type, **option_dict)
        fields = list(self.instMarketEye.GetHeaderValue(1))
        x = []
        for i in range(len(stocks)):
            for j in range(len(fields)):
                y = self.instMarketEye.GetDataValue(j, i)
                x.append(y)
        dat = np.array(x).reshape(len(stocks), len(fields))
        df = pd.DataFrame(dat, columns=fields)
        return df

    def get_bt_dataframe(self, stock, req_type, *stock_chart_args):
        volume_param = {'10': '1'}
        stk_chrt = self.get_chart_as_dataframe(stock, req_type, *stock_chart_args, **volume_param)
        eng_col_converter = {
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '종가': 'close',
            '거래량': 'volume',
            '미체결약정': 'openinterest'
        }
        stk_chrt = stk_chrt.rename(columns=eng_col_converter)
        stk_chrt['open interest'] = 0
        stk_chrt = stk_chrt.iloc[::-1]
        stk_chrt = stk_chrt.set_index('datetime')
        return stk_chrt

    def get_training_set_dataframe(self, stock, req_type, *stock_chart_args):
        volume_param = {
            '5': tuple(range(5, 37)),
            '10': '1'}
        stk_chrt = self.get_chart_as_dataframe(stock, req_type, *stock_chart_args, **volume_param)
        eng_col_converter = {
            '시가': 'Open',
            '고가': 'High',
            '저가': 'Low',
            '종가': 'Close',
            'datetime': 'Date',
        }
        stk_chrt = stk_chrt.rename(columns=eng_col_converter)
        stk_chrt.sort_values('Date', inplace=True)
        stk_chrt.reset_index(inplace=True)
        stk_chrt.drop(['index'], inplace=True, errors='ignore')
        return stk_chrt

    def get_ten_days_min_by_min(self, stock, req_type, *stock_chart_args):
        volume_param = {
            '6': 'm',
            '10': '1'}
        stk_chrt = self.get_chart_as_dataframe(stock, req_type,
                                               *stock_chart_args, **volume_param)
        stk_chrt.reset_index(inplace=True)
        stk_chrt.drop(['index'], inplace=True, errors='ignore')

        return stk_chrt


class CybosTrader:
    def __init__(self):
        import win32com.client
        self.instCpTdUtil = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.instCpTdUtil.TradeInit()
        ahk_path = "C:\\Users\\sh\\Documents\\devbox\\ahk"
        ahk_exe_path = "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe"
        subprocess.call(['runas', '/noprofile', '/user:Administrator', ahk_exe_path, os.path.join(ahk_path, 'cybos_trader_pwd_in.ahk')])
        self.instCpTd0311 = win32com.client.Dispatch("CpTrade.CpTd0311")


if __name__ == '__main__':
    ct = CybosTrader()
