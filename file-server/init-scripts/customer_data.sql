CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(100),
    account_balance DECIMAL(15,2),
    status VARCHAR(20)
);

CREATE TABLE trades (
    trade_id INT PRIMARY KEY,
    client_id INT,
    trade_date DATE,
    amount DECIMAL(15,2),
    security_symbol VARCHAR(10)
);
CREATE TABLE client_activity (
    client_id INT PRIMARY KEY,
    last_login TIMESTAMP,
    session_count INT DEFAULT 0
);

INSERT INTO client_activity VALUES (1001, NOW(), 1);

INSERT INTO clients VALUES 
    (1001, 'Goldman Investments LLC', 2500000.00, 'active'),
    (1002, 'Blackstone Holdings', 1800000.00, 'active'),
    (1003, 'pension Fund Alpha', 3200000.00, 'active');
