-- Connect to  database
\c ohlcvt

-- Create the "historical" table
CREATE TABLE historical (
    asset TEXT,
    epoch BIGINT,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    trades NUMERIC
);

-- Create the "user" table
CREATE TABLE users  (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);


-- Insert records into the "users" table
INSERT INTO users (id, username, email, hashed_password, role)
VALUES
    (1, 'john Doe', 'john.doe@example.com', 'password123', 'admin'),
    (2, 'jane Smith', 'jane.smith@example.net', 'password456', 'user');