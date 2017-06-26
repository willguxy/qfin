from time import sleep
from datetime import datetime
from sqlalchemy import create_engine
from pandas import DataFrame

import gdax

from ... import config

GDAX_Config = config.GDAX_Config

utcnow = datetime.utcnow


def snapshot_MarketDataL2_GDAX(DSN='CryptoCrncy', table='MarketDataL2'):
    
    pairs = [
      ('BTC', 'USD'),
      ('ETH', 'USD'), ('ETH', 'BTC'), 
      ('LTC', 'USD'), ('LTC', 'BTC'),
    ]

    tot_cnt   = 0
    db_engine = create_engine(config.DB_Config.crypto_crncy_str)
    client    = gdax.AuthenticatedClient(GDAX_Config.key, GDAX_Config.seckey, GDAX_Config.passwd)

    # Level 2:  price, size, num-orders
    for base_ccy, quote_ccy in pairs:
        now        = utcnow()
        pair_name  = base_ccy + '-' + quote_ccy

        order_book = client.get_product_order_book(pair_name, level=2)
        timeIdx    = now.hour * 24 * 60 + now.minute * 60 + now.second + 0.001 * (now.microsecond // 1000)

        vside, vpx, vsize, vcnt = [], [], [], []
        asks, bids = order_book.get('asks'), order_book.get('bids')

        for px, size, cnt in asks:
            vside.append( 'A'         )
            vpx  .append( float(px)   )
            vsize.append( float(size) )
            vcnt .append( int(cnt)    )

        for px, size, cnt in bids:
            vside.append( 'B'         )
            vpx  .append( float(px)   )
            vsize.append( float(size) )
            vcnt .append( int(cnt)    )

        if len(vsize) == 0:
            continue

        dfBook = DataFrame({
                      'DataDate'  : now.date()
                    , 'Exchange'  : 'GDAX'
                    , 'TimeIdx'   : timeIdx
                    , 'DateTime_' : now
                    , 'BaseCrncy' : base_ccy
                    , 'QuoteCrncy': quote_ccy
                    , 'Side'      : vside
                    , 'Price'     : vpx
                    , 'Size'      : vsize
                    , 'NumOrders' : vcnt
                    })
        cols   = ['DataDate', 'Exchange', 'TimeIdx', 'DateTime_', 'BaseCrncy', 'QuoteCrncy', 
                'Side', 'Price', 'Size', 'NumOrders' ]
        dfBook = dfBook[cols].copy()

        qry = "DELETE FROM MarketDataL2 WHERE DataDate = '%s' AND TimeIdx BETWEEN %.3f AND %.3f" % (
                    now.strftime('%Y-%m-%d'), timeIdx - .001, timeIdx + .001)
        db_engine.execute(qry)
        dfBook.to_sql('MarketDataL2', db_engine, if_exists='append', index=False)

        tot_cnt += dfBook.shape[0]
        sleep(0.25)

    return tot_cnt
