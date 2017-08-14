#!C:\Users\sh\Anaconda3\python
import sys
sys.path.append("C:\\Users\\sh\\Documents\\devbox\\github\\auto_invest")
import time
from src.utils.database import dbMeta
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
from multiprocessing import Pool, TimeoutError
import logging
import os
from src.krx.krx_api_talker import KrxApiTalker



if __name__ == '__main__':
    today = date.today()
    update_tbs = ['tbl_dailystock', 'tbl_timeconclude']

    """     LOGGER INSTANCE     """
    log_dir = """C:\\Users\\sh\\Documents\\devbox\\log\\cybos\\%s""" % today.strftime('%Y-%m-%d')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_loc = os.path.join(log_dir, 'krx_api_call_%s_%d.log' % (today.strftime('%Y-%m-%d'), os.getpid()))
    formatter = logging.Formatter("%(asctime)s: %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
                                  , "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_loc)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger = logging.getLogger('krx')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    """     Log as stdout       """
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if today.weekday() in (5, 6):
        print("does not operate on the weekends.")
        exit()

    """     REMOVE YESTERDAY'S DATA FROM cybos.market_eye_today and INSERT TO cybos.market_eye_history     """
    logger.info('Migrating data krx data to history table.')
    inserted = dbMeta.call_proc('sp_krx_today_to_history')
    logger.info('%d inserted to krx_timeconclude_history. %d inserted to  krx_dailystock_history.' % inserted[0])

    """     SET UP DATE PARAMS    """
    market_open = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
    market_close = datetime.combine(today, datetime.min.time()) + timedelta(hours=18)

    pool = Pool(1)
    while True:
        now = datetime.now()
        before_market = True if now < market_open else False
        mkt_is_open = True if market_open <= now <= market_close \
            else False

        if before_market:
            time.sleep(1)
        elif mkt_is_open:
            res = pool.apply_async(KrxApiTalker.api_to_mysql, [update_tbs])
            try:
                d = res.get(600)
                if 'tbl_dailystock' in update_tbs:
                    "   After the first iteration tbl_dailystock is unnecessary     "
                    update_tbs.remove('tbl_dailystock')

                logger.info("Insertion result: %s" % " ".join(["%s: %d" % (k, v) for k, v in d.items()]))

            except IntegrityError as e:
                logger.error(str(e))

            except TimeoutError:
                logger.error('***********************API Call timeout.***********************')

        else:
            logger.debug('Stock market closed, exiting ...')
            exit(0)