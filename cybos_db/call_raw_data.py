#!C:\Users\sh\Anaconda3\python
import sys
from multiprocessing.pool import Pool

sys.path.append("C:\\Users\\sh\\Documents\\devbox\\github\\auto_invest")
import time
from src.utils.database import dbMeta
from multiprocessing import Pool, TimeoutError
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
import logging
import os

if __name__ == '__main__':
    today = date.today()


    """     LOGGER INSTANCE     """
    log_dir = """C:\\Users\\sh\\Documents\\devbox\\log\\cybos\\%s""" % today.strftime('%Y-%m-%d')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_loc = os.path.join(log_dir, 'cybos_api_call_%s_%d.log' % (today.strftime('%Y-%m-%d'), os.getpid()))
    formatter = logging.Formatter("%(asctime)s: %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
                                  , "%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(log_loc)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger = logging.getLogger('cybos')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    """     Log as stdout       """
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if today.weekday() in (5, 6):
        logger.error("does not operate on the weekends.")
        exit()

    last_etl_dt = today - timedelta(days=3) if today.weekday() == 0 else today - timedelta(days=1)

    """     SET UP DATE PARAMS    """
    market_open = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
    market_close = datetime.combine(today, datetime.min.time()) + timedelta(hours=23)

    """     REMOVE YESTERDAY'S DATA FROM cybos.market_eye_today and INSERT TO cybos.market_eye_history     """
    # logger.info('Migrating data from cybos.market_eye_today to cybos.market_eye_history.')
    # inserted = dbMeta.call_proc('sp_market_eye_today_to_history', (int(last_etl_dt.strftime('%Y%m%d')),))
    # logger.info('%d rows inserted to cybos.market_eye_history.' % inserted[0])

    while True:
        pool = Pool(1)
        now = datetime.now()
        next_iter = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
        before_market = True if now < market_open else False
        mkt_is_open = True if market_open <= now <= market_close \
            else False

        if before_market:
            time.sleep(100)
        elif mkt_is_open:
            res = pool.apply_async(dbMeta.snapshot_market_eye_res)
            try:
                ins = res.get(1)
                logger.info("%d inserted from API call." % ins)
                while datetime.now() < next_iter:
                    time.sleep(1)

            except IntegrityError as e:
                logger.error(str(e))
            except AssertionError as e:
                logger.error(str(e))
                exit(1)
            except TimeoutError:
                logger.error('***********************API Call timeout.***********************')
        else:
            logger.debug('Stock market closed, exiting ...')
            exit(0)

