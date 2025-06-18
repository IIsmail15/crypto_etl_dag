CREATE  DATABASE crypto_data;

USE crypto_data, 

CREATE TABLE coins (
    id TEXT, 
    symbol TEXT,  
    current_price INTEGER,
    market_cap BIGINT,
    last_updated TIMESTAMP, 
 );

