import sys

import traceback
if sys.version_info > (3, ):
    # Python 3.x
    from io import StringIO
else:
    # Python 2.x
    from io import BytesIO as StringIO

from time import sleep
from datetime import datetime
utcnow = datetime.utcnow

from qfin.CryptoCrncy.proc import (
        snapshot_MarketDataL2_GDAX, 
        download_trade_data_GDAX,
    )

import logging  # @ToDo: use logging instead of print


def run():

    wait = 1
    while True:
        now = utcnow()
        print('running %s' % now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]) 

        exception_str = StringIO()
        try:
            cnt  = snapshot_MarketDataL2_GDAX()
            print("GDAX: loaded %s quotes" % cnt)
            wait = 1
        except Exception as err:
            print("GDAX: failed to load market quote data")
            traceback.print_exc(file=exception_str)
            print('Stack info: \n' + exception_str.getvalue() + '\n')
            sleep(wait)
            wait *= 2

        # @ToDo, there might be missing trades
        exception_str = StringIO()
        try:
            cnt  = download_trade_data_GDAX()
            print("GDAX: loaded %s trades" % cnt)
            wait = 1
        except Exception as err:
            print("GDAX: failed to load market trade data")
            traceback.print_exc(file=exception_str)
            print('Stack info: \n' + exception_str.getvalue() + '\n')
            sleep(wait)
            wait *= 2


if __name__ == '__main__':
    run()
