from six import string_types
from datetime import datetime
from sqlalchemy import create_engine
import pandas


def get_market_data(date, exchange=None, base_ccy=None, quote_ccy=None, start_time=0, end_time=99999, level=2):

    if level != 2:
        raise ValueError("Currently only Level 2 data is supported.")

    if exchange is not None and exchange not in {"GDAX"}:
        raise ValueError("Exchange %s is not supported" % exchange)

    date_str = date if isinstance(date, string_types) else date.strftime('%Y-%m-%d')

    qry = """
        SELECT DataDate, Exchange, TimeIdx, 
               BaseCrncy, QuoteCrncy, Side, Price, Size, NumOrders 
        FROM   MarketDataL2 
        WHERE  DataDate = '%s' 
          AND  TimeIdx BETWEEN %.3f AND %.3f
        """ % (date_str, start_time, end_time)

    if exchange is not None:
        qry += " AND Exchange   = '%s' " % exchange
    if base_ccy is not None:
        qry += " AND BaseCrncy  = '%s' " % base_ccy
    if quote_ccy is not None:
        qry += " AND QuoteCrncy = '%s' " % quote_ccy

    db_engine = create_engine("mysql+mysqldb://root:Research527@localhost/crypto_crncy")
    dfBook = pandas.read_sql(qry, con=db_engine)
    dfBook['DataDate'] = pandas.to_datetime(dfBook['DataDate'], utc=True)

    return dfBook
