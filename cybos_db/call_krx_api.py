#!C:\Users\sh\Anaconda3\python
import sys
sys.path.append("C:\\Users\\sh\\Documents\\devbox\\github\\auto_invest")
import time
from src.utils.database import dbMeta
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
import logging
log_dir = """C:\\Users\\sh\\Documents\\devbox\\log\\cybos"""
import os
from src.krx.api_to_db import KrxApiTalker

today = date.today()
update_tbs = ['tbl_dailystock', 'tbl_timeconclude']

"""     LOGGER INSTANCE     """
log_loc = os.path.join(log_dir, 'krx_api_call_%s_%d.log' % (today.strftime('%Y-%m-%d'), os.getpid()))
formatter = logging.Formatter("%(asctime)s: %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
                              , "%Y-%m-%d %H:%M:%S")
fh = logging.FileHandler(log_loc)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

"""     Log as stdout       """
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

if today.weekday() in (5, 6):
    print("does not operate on the weekends.")
    exit()

last_etl_dt = today - timedelta(days=3) if today.weekday() == 1 else today - timedelta(days=1)

"""     SET UP DATE PARAMS    """
market_open = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
market_close = datetime.combine(today, datetime.min.time()) + timedelta(hours=15, minutes=30)

"""     REMOVE YESTERDAY'S DATA FROM cybos.market_eye_today and INSERT TO cybos.market_eye_history     """
# logger.info('Migrating data from cybos.market_eye_today to cybos.market_eye_history.')
# inserted = dbMeta.call_proc('sp_krx_today_to_history', [int(last_etl_dt.strftime('%Y%m%d'))])
# logger.info('%d rows inserted to cybos.market_eye_history.' % inserted[0])

while True:
    now = datetime.now()
    before_market = True if now < market_open else False
    mkt_is_open = True if market_open <= now <= market_close \
        else False

    if before_market:
        time.sleep(1)
    elif mkt_is_open:
        try:
            d = KrxApiTalker.api_to_mysql(update_tbs)
            logger.info("%s" % str(d))
        except IntegrityError as e:
            logger.error(str(e))
    else:
        logger.debug('Stock market closed, exiting ...')
        exit(0)

