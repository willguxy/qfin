from time import sleep
from datetime import datetime

from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame, concat

import gdax

from ...import config
from ..constants import pairs

GDAX_Config = config.GDAX_Config


def download_trade_data_GDAX():
    """
    Currently only download the past 100 trades 
    """

    # @ToDo, check if there are missing trades
    
    tot_cnt   = 0
    db_engine = create_engine(config.DB_Config.crypto_crncy_str)
    client    = gdax.AuthenticatedClient(GDAX_Config.key, GDAX_Config.seckey, GDAX_Config.passwd)

    # fetch max trade id for each pair
    qry = """SELECT Exchange, BaseCrncy, QuoteCrncy, MaxTradeId 
             FROM TradeDataMaxID WHERE Exchange = 'GDAX'; """
    dfID    = pd.read_sql(qry, db_engine)
    
    max_ids = {}
    for _, (_, base_ccy, quote_ccy, mid) in dfID.iterrows():
        max_ids[base_ccy + '-' + quote_ccy] = int(mid)

    # iterate through each pair
    hld = []
    for base_ccy, quote_ccy in pairs:
        try:
            cnt, df  = _download_trades(base_ccy, quote_ccy, client, max_ids)
            tot_cnt += cnt
            if df is not None:
                hld.append(df)
            sleep(0.25)
        except Exception as err:
            pass

    # First Update TradeDataMaxID
    vbase, vquote, vmid = [], [], []
    for k, v in max_ids.items():
        base_ccy, quote_ccy = k[:3], k[-3:]
        vbase .append(k[:3 ])
        vquote.append(k[-3:])
        vmid  .append(int(v))
    if len(vbase) > 0:
        dfID = DataFrame({
              'Exchange'  : 'GDAX'
            , 'BaseCrncy' : vbase
            , 'QuoteCrncy': vquote
            , 'MaxTradeId': vmid
            }, columns=['Exchange' , 'BaseCrncy', 'QuoteCrncy', 'MaxTradeId'])
        qry = "DELETE FROM TradeDataMaxID WHERE Exchange = 'GDAX';"
        db_engine.execute(qry)
        dfID.to_sql('TradeDataMaxID', db_engine, if_exists='append', index=False)

    # The update 
    if len(hld) > 0:
        dfTrds = concat(hld, ignore_index=True, axis=0)
        dfTrds.to_sql('TradeData', db_engine, if_exists='append', index=False)

    return tot_cnt


def _download_trades(base_ccy, quote_ccy, client, max_ids):
    
    # @ToDo: check if there are trades missing

    pair_name = base_ccy + '-' + quote_ccy
    max_id    = max_ids.get(pair_name, 0)
    trades    = client.get_product_trades(product_id=pair_name)

    vtime, vid, vpx, vsize, vside = [], [], [], [], []
    for trd in trades:

        trade_id  = int  ( trd.get('trade_id', -1) )
        if trade_id <= max_id:
            if trade_id < 0:
                print("Error: failed to parse data.")
            continue

        # time
        tradetime = trd.get('time')
        if tradetime:
            tradetime = datetime.strptime(tradetime, '%Y-%m-%dT%H:%M:%S.%fZ')

        # other info
        price     = float( trd.get('price',    -1) )
        size      = float( trd.get('size' ,    -1) )
        side      = trd.get('side', 'n')[0]

        # Sanity check
        if tradetime is None or trade_id<0 or price<0 or size<0:
            print("Error: failed to parse data.")
            continue

        vtime.append( tradetime )
        vid  .append( trade_id  )
        vpx  .append( price     )
        vsize.append( size      )
        vside.append( side      )

    if len(vid) == 0:
        return 0, None

    dfTrds = DataFrame({
                  'TradeDate' : [d.date() for d in vtime]
                , 'Exchange'  : 'GDAX'
                , 'BaseCrncy' : base_ccy
                , 'QuoteCrncy': quote_ccy
                , 'TradeId'   : vid
                , 'TimeIdx'   : 0.0
                , 'TradeTime' : vtime
                , 'Side'      : vside
                , 'Price'     : vpx
                , 'Size'      : vsize
              }, columns = ['TradeDate', 'Exchange', 'BaseCrncy', 'QuoteCrncy', 'TradeId', 
                            'TimeIdx', 'TradeTime', 'Side', 'Price', 'Size'])
    max_ids[pair_name] = int(dfTrds['TradeId'].max())
    cnt = dfTrds.shape[0]
    
    return cnt, dfTrds
