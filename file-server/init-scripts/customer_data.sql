-- customer_data.sql
CREATE DATABASE IF NOT EXISTS customer_db;
USE customer_db;

-- Main client table with sensitive financial data
CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(100),
    ssn VARCHAR(11),  -- Sensitive!
    account_balance DECIMAL(15,2),
    credit_limit DECIMAL(15,2),
    risk_score INT,
    status VARCHAR(20),
    account_type VARCHAR(50)
);

CREATE TABLE trades (
    trade_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    trade_date DATE,
    amount DECIMAL(15,2),
    security_symbol VARCHAR(10),
    trade_type VARCHAR(10),
    commission DECIMAL(10,2)
);

CREATE TABLE client_activity (
    client_id INT PRIMARY KEY,
    last_login TIMESTAMP,
    session_count INT DEFAULT 0,
    ip_address VARCHAR(15),
    failed_attempts INT DEFAULT 0
);

CREATE TABLE portfolio_holdings (
    holding_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    symbol VARCHAR(10),
    shares INT,
    purchase_price DECIMAL(10,2),
    current_value DECIMAL(15,2)
);

CREATE TABLE wire_transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    routing_number VARCHAR(9),  -- Sensitive!
    account_number VARCHAR(17),  -- Sensitive!
    amount DECIMAL(15,2),
    transfer_date DATE,
    destination_bank VARCHAR(100)
);

-- Insert realistic data
INSERT INTO clients VALUES 
    (1001, 'Goldman Investments LLC', '123-45-6789', 2500000.00, 5000000.00, 750, 'active', 'institutional'),
    (1002, 'Blackstone Holdings', '987-65-4321', 1800000.00, 3500000.00, 680, 'active', 'institutional'),
    (1003, 'Pension Fund Alpha', '456-78-9012', 3200000.00, 6000000.00, 800, 'active', 'retirement'),
    (1004, 'Morgan Family Trust', '321-54-9876', 950000.00, 1500000.00, 720, 'active', 'trust'),
    (1005, 'Chen Trading Corp', '654-32-1098', 4100000.00, 8000000.00, 690, 'active', 'corporate'),
    (1006, 'Atlas Hedge Fund', '789-01-2345', 8700000.00, 15000000.00, 710, 'active', 'hedge_fund'),
    (1007, 'Riverside Ventures', '234-56-7890', 1200000.00, 2000000.00, 650, 'suspended', 'venture'),
    (1008, 'Pacific Wealth Mgmt', '890-12-3456', 5500000.00, 10000000.00, 790, 'active', 'wealth_mgmt');

-- Generate trade history
INSERT INTO trades (client_id, trade_date, amount, security_symbol, trade_type, commission) VALUES
    (1001, CURDATE(), 150000.00, 'AAPL', 'BUY', 125.00),
    (1001, CURDATE(), 200000.00, 'MSFT', 'BUY', 150.00),
    (1002, CURDATE(), 75000.00, 'GOOGL', 'SELL', 100.00),
    (1003, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 300000.00, 'TSLA', 'BUY', 200.00),
    (1004, CURDATE(), 50000.00, 'NVDA', 'BUY', 75.00),
    (1005, CURDATE(), 425000.00, 'META', 'SELL', 300.00),
    (1006, DATE_SUB(CURDATE(), INTERVAL 2 DAY), 1000000.00, 'BTC', 'BUY', 500.00);

-- Insert wire transfer records (very sensitive!)
INSERT INTO wire_transfers VALUES
    (NULL, 1001, '021000021', '1234567890123456', 500000.00, CURDATE(), 'Chase Manhattan'),
    (NULL, 1002, '026009593', '9876543210987654', 250000.00, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Bank of America'),
    (NULL, 1003, '021001208', '1111222233334444', 750000.00, CURDATE(), 'Wells Fargo');

-- Portfolio holdings
INSERT INTO portfolio_holdings (client_id, symbol, shares, purchase_price, current_value) VALUES
    (1001, 'AAPL', 5000, 145.50, 875000.00),
    (1001, 'MSFT', 3000, 250.00, 900000.00),
    (1002, 'GOOGL', 2000, 100.25, 280000.00),
    (1003, 'TSLA', 4500, 180.00, 1125000.00);
