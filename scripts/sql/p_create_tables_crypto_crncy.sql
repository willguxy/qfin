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

