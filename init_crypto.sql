-- Create your database (if it doesn't already exist)
CREATE DATABASE crypto_data;
-- Switch into it
\c crypto_data;
-- Create the coins table
CREATE TABLE coins (
    id            TEXT,
    symbol        TEXT,
    current_price NUMERIC(12,2),
    market_cap    BIGINT,
    last_updated  TIMESTAMP
);

