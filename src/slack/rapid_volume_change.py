# -*- coding: utf-8 -*-
# cybos related
import sys
proj_dir = "C:\\Users\\sh\\Documents\\devbox\\github\\auto_invest"
sys.path.append(proj_dir)
import os
import shutil
import time
from src.slack.slack_msg import SlackMessenger
from src.utils.database import dbMeta
import pandas as pd
from datetime import date, datetime, timedelta
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
img_dir = os.path.join(proj_dir, 'tmp', 'img')
font_loc = os.path.join(proj_dir, "asset\\human_myeongjo.ttf")
font_name = fm.FontProperties(fname=font_loc).get_name()
font = {
    'family': font_name,
    'weight': 'bold',
}
mpl.rc('font', **font)
mpl.rc('text', color='white')


def get_time_derivative(df, time_col, deriv_col, index_is_time=False):
    if index_is_time:
        df['dt'] = pd.Series(df.index.tolist(), index=df.index).diff().apply(lambda x: x.total_seconds())
    else:
        df['dt'] = df[time_col].apply(lambda x: x.timestamp()).diff()
    df['col_dt'] = df[deriv_col].diff()
    c_name = 'deriv_%s' % deriv_col
    df[c_name] = df['col_dt'] / df['dt']
    df.drop(['dt', 'col_dt'], inplace=True, errors='ignore')
    df = df.fillna(0)
    return (df, c_name)


def five_min_volume_delta(df):
    return (df.iloc[len(df) - 1]['거래량'] - df.iloc[0]['거래량']) / df.iloc[len(df) - 1]['거래량']


def five_min_price_delta(df):
    return (df.iloc[len(df) - 1]['현재가'] - df.iloc[0]['현재가']) / df.iloc[len(df) - 1]['현재가']


def get_stock_tendency(df):
    vol_delta_percent = five_min_volume_delta(df)
    p_delta = five_min_price_delta(df)
    if vol_delta_percent > 0.1 and p_delta > 0:
        return True, True
    elif vol_delta_percent > 0.1 and p_delta < 0:
        return True, False
    else:
        return False, False


def get_stock_codes(df):
    return df['종목코드'].unique().tolist()


def get_stock_name_from_code(df, cd):
    return df[df['종목코드'] == cd]['종목명'].unique().tolist()[0]


def save_graph_as_image(df, stock_name):
    df = df.set_index('time')
    df.head(10)
    target = '현재가'
    fig, ax = plt.subplots(figsize=(15, 8))
    title = r"%s over time" % target
    """     PLOT LINES      """
    ax.plot(df[target], sns.xkcd_rgb["denim blue"], label=target)
    """     GET TWIN AXES    """
    ax2 = ax.twinx()
    df, deriv_col = get_time_derivative(df, 'time', '거래량', index_is_time=True)
    ax2.plot(df[deriv_col], sns.xkcd_rgb["medium green"], label='volume')
    """   ADD LEGEND   """
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    legend.get_frame().set_facecolor('#FFFFFF')
    sns.despine(ax=ax, right=True, left=False)
    sns.despine(ax=ax2, right=False, left=True)
    img_file_abs_path = os.path.join(img_dir, '%s_%s.jpg' % (stock_name, datetime.now().strftime('%Y%m%d%H%M%S')))
    plt.savefig(img_file_abs_path)
    return img_file_abs_path


def get_all_today_stock_data(cd):
    sql = """
    SELECT 
        `거래량`
        , `현재가`
        , `time`
    FROM market_eye_today
    WHERE `종목코드` = '{}'
    """.format(cd)
    engine = dbMeta.get_mysql_engine()
    df = pd.read_sql(sql, engine)
    return df

def get_recent_data(min_ago):
    sql = """
    SELECT 
        `종목코드`
        , `종목명`
        , `거래량`
        , `현재가`
        , `time`
    FROM market_eye_today
    WHERE `time` >= '{time}'
    GROUP BY 1, 2, 3, 4, 5 
    ;
    """.format(time=min_ago)
    engine = dbMeta.get_mysql_engine()
    snapshot = pd.read_sql(sql, engine)
    return snapshot

if __name__ == '__main__':
    """     SET UP DATE PARAMS    """
    today = date.today()
    if today.weekday() in (5, 6):
        exit()

    market_open = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
    market_close = datetime.combine(today, datetime.min.time()) + timedelta(hours=16)

    while True:
        now = datetime.now()
        before_mkt = True if now <= market_open else False
        mkt_is_open = True if market_open <= now <= market_close \
            else False
        if before_mkt:
            time.sleep(1)
        elif mkt_is_open:
            ten_min_ago = datetime.now() - timedelta(minutes=10)
            ten_min_ago = ten_min_ago.replace(second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            snapshot = get_recent_data(ten_min_ago)
            stocks = get_stock_codes(snapshot)
            alerted_stocks = {}
            for s in stocks:
                s_df = snapshot[snapshot['종목코드'] == s]
                is_rapid_trade, p_is_up = get_stock_tendency(s_df)
                if is_rapid_trade:
                    stock_name = get_stock_name_from_code(s_df, s)
                    if stock_name not in alerted_stocks.keys() or \
                        (stock_name in alerted_stocks.keys() and datetime.now() - timedelta(minutes=10) < alerted_stocks[stock_name]):
                        alerted_stocks.update({stock_name: datetime.now()})
                        df = get_all_today_stock_data(s)
                        file_path = save_graph_as_image(df, stock_name)
                        title = '%s\'s volume delta: %f price fall delta: %f @ %s' \
                                % (get_stock_name_from_code(s_df, s)
                                   , five_min_volume_delta(s_df)
                                   , five_min_price_delta(s_df)
                                   , datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        target_chann = 'rapid_up' if p_is_up else 'rapid_down'
                        SlackMessenger.send_file(title, target_chann, file_path)
                        plt.close()
            time.sleep(60)
            try:
                shutil.rmtree(img_dir)
                os.makedirs(img_dir, exist_ok=True)
            except PermissionError as e:
                print('failed to truncate image directory at /tmp')
        else:
            exit(0)