CREATE TABLE MarketDataL2 (
    DataDate    DATE      NOT NULL   -- date passed since 1970-01-01
  , Exchange    CHAR(6)   NOT NULL   -- GDAX
  , TimeIdx     REAL      NOT NULL   -- seconds passed since midnight hhmmss.fff as float   
  , DateTime_   DATETIME  NOT NULL
  , BaseCrncy   CHAR(3)   NOT NULL 
  , QuoteCrncy  CHAR(3)   NOT NULL
  , Side        Char(1)   NOT NULL   -- B/A
  , Price       REAL      NOT NULL
  , Size        REAL      NOT NULL
  , NumOrders   INT       NOT NULL
  , PRIMARY KEY (DataDate, Exchange, TimeIdx, Side, Price)
);


-- Max TradeID are saved here
CREATE TABLE TradeDataMaxID (
    Exchange    CHAR(6)    NOT NULL
  , BaseCrncy   CHAR(3)    NOT NULL
  , QuoteCrncy  CHAR(3)    NOT NULL
  , MaxTradeID  BIGINT     NOT NULL
  , PRIMARY KEY (Exchange, BaseCrncy, QuoteCrncy)
);


CREATE TABLE TradeData (
    TradeDate   DATE       NOT NULL
  , Exchange    CHAR(6)    NOT NULL
  , BaseCrncy   CHAR(3)    NOT NULL
  , QuoteCrncy  CHAR(3)    NOT NULL
  , TradeID     BIGINT     NOT NULL
  , TimeIdx     REAL       NOT NULL
  , TradeTime   DATETIME   NOT NULL
  , Side        CHAR(1)    NOT NULL
  , Price       REAL       NOT NULL
  , Size        REAL       NOT NULL
  , PRIMARY KEY (TradeDate, Exchange, BaseCrncy, QuoteCrncy, TradeID)
);
