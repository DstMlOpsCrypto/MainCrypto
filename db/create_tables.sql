
-- Connect to  database
--\c cryptoDb

-- Create the "historical" table
CREATE TABLE ohlc (
    asset TEXT,
    dtutc TIMESTAMPTZ NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume DOUBLE PRECISION,
    trades DOUBLE PRECISION DEFAULT NULL
);

CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    asset TEXT NOT NULL,
    symbol TEXT NOT NULL,
    exchange TEXT NOT NULL
); 

-- Create the "user" table
CREATE TABLE members  (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- START:ADDED FOR API
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    prediction_date TIMESTAMP,
    prediction_value NUMERIC
);


CREATE TABLE model_evaluation (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255),
    model_version VARCHAR(255),
    evaluation_date TIMESTAMP,
    mse_train NUMERIC,
    r2_score_train NUMERIC,
    mse_test NUMERIC,
    r2_score_test NUMERIC
);
-- END:ADDED FOR API

-- Insert records into the "assets" table
INSERT INTO assets (id, asset, symbol, exchange)
VALUES
    (1, 'XXBTZUSD', 'BTZUSD', 'kraken');

-- Insert records into the "members" table
INSERT INTO members (id, username, email, hashed_password, role)
VALUES
    (1, 'admin', 'admin@admin.com', '$argon2id$v=19$m=65536,t=3,p=4$U2qt1XoPYSxFyPn/fy8FgA$2xQ08S6Nq2dez3i0b9en6tAO55aHTe4y6jvg3RqPUr4', 'admin'),
    (2, 'user', 'user@user.com', '$argon2id$v=19$m=65536,t=3,p=4$DGEs5ZyTsnZuDcH4X+v9Xw$hXkcx5V+RA8IlZ3TBMK2Yz/kO9mbGljBQqKRvK8CaOQ', 'user');


-- Avant les commandes COPY, ajoutez ces configurations
SET datestyle = 'ISO, DMY';

-- Modifiez la commande COPY pour gérer le format des nombres
COPY ohlc (asset, dtutc, open, high, low, close, volume)
FROM '/docker-entrypoint-initdb.d/BTC_Historic.csv'
WITH (
    FORMAT csv,
    HEADER true,
    DELIMITER ','
);

UPDATE ohlc SET trades = NULL;