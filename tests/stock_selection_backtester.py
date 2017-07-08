from datetime import datetime, timedelta

from clairvoyant import Backtest

from src.cybos.cybos_talker import CybosTalker

# Testing performance on a single stock

variables  = [
    "전일대비",
    "exchange_portion",
    # "외국인현보유비율",
    "delta_portion",
]     # Financial indicators of choice
# Start of training period
trainStart = (datetime.today() - timedelta(weeks=104)).strftime('%Y%m%d')
# trainEnd   = (datetime.today() - timedelta(weeks=14, days=1)).strftime('%Y%m%d') # End of training period
# testStart  = (datetime.today() - timedelta(weeks=14)).strftime('%Y%m%d')  # Start of testing period
test_portion = 0.2
testEnd = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')    # End of testing period
buyThreshold = 0.5          # Confidence threshold for predicting buy (default = 0.65)
sellThreshold = 0.5            # Confidence threshold for predicting sell (default = 0.65)
C = 1                           # Penalty parameter (default = 1)
gamma = 10                      # Kernel coefficient (default = 10)
continuedTraining = False       # Continue training during testing period? (default = false)
ct = CybosTalker()
# Testing performance across multiple stocks
global_stocks = ct.get_domestic_stock_list()
# stocks = random.sample(global_stocks.keys(), 1)
stocks = ['롯데쇼핑']

for stock in stocks:
    print('******************************************************')
    print('*******\tBACK TESTING FOR %s\t*******' % stock)
    print('******************************************************')

    data = ct.get_training_set_dataframe(global_stocks[stock], 'range'
                                         , trainStart
                                         , testEnd)
    data = data.round(3)
    data['delta_portion'] = (data['High'] - data['Low']) / data['Open']
    data['exchange_portion'] = data['거래량'] / data['상장주식수'] * 100
    print(data.loc[:, variables].head(5))
    print(data.loc[:, variables].tail(5))

    if trainStart <= data["Date"][0].strftime('%Y%m%d'):
        trainStart = data["Date"][0].strftime('%Y%m%d')
    backtest = Backtest(stock, data, variables, trainStart, testEnd, test_portion
                        , buyThreshold=buyThreshold
                        , sellThreshold=sellThreshold
    )
    for i in range(0, 200):
        backtest.runModel()
    backtest.displayConditions()
    backtest.displayStats()