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
            print("GDAX: loaded %s rows" % cnt)
            wait = 1
        except Exception as err:
            print("GDAX: failed to load market data")
            traceback.print_exc(file=exception_str)
            print('Stack info: \n' + exception_str.getvalue() + '\n')

            sleep(wait)
            wait *= 2


if __name__ == '__main__':
    run()

        

