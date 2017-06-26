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


def run():

    while True:

        now = utcnow()
        print('running %s' % now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]) 

        cnt = snapshot_MarketDataL2_GDAX()
        print("GDAX: loaded %s rows" % cnt)


if __name__ == '__main__':

    exception_str = StringIO()
    try:
        run()
    except Exception as err:
        traceback.print_exc(file=exception_str)
        msg = 'Stack info: \n' + exception_str.getvalue() + '\n'
        print(msg)
