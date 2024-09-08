
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
    trades DOUBLE PRECISION
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

-- Insert records into the "users" table
INSERT INTO assets (id, asset, symbol, exchange)
VALUES
    (1, 'XXBTZUSD', 'BTZUSD', 'kraken');

-- Insert records into the "users" table
INSERT INTO members (id, username, email, hashed_password, role)
VALUES
    (1, 'john Doe', 'john.doe@example.com', 'password123', 'admin'),
    (2, 'jane Smith', 'jane.smith@example.net', 'password456', 'user');
