import time
from src.utils.database import dbMeta
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError

today = date.today()
yesterday = today - timedelta(days=1)
market_open = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
market_close = datetime.combine(today, datetime.min.time()) + timedelta(hours=15, minutes=30)

"""     REMOVE YESTERDAY'S DATA FROM cybos.market_eye_today     """
inserted = dbMeta.call_proc('sp_market_eye_today_to_history', [int(today.strftime('%Y%m%d'))])
print(inserted)
print('%d rows inserted' % inserted[0])

while True:
    now = datetime.now()
    min_ltr = now.replace(second=0, microsecond=0) + timedelta(minutes=1)
    mkt_is_open = True if market_open <= now <= market_close \
        else False
    if mkt_is_open:
        print("%s CALLING - dbMeta.snapshot_market_eye_res()" % now.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            dbMeta.snapshot_market_eye_res()
        except IntegrityError as e:
            print(str(e))
        while datetime.now() < min_ltr:
            time.sleep(1)
    else:
        print('Stock market closed.')
        break

