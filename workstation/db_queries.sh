#!/bin/bash
# Simulates Sarah Chen's daily database queries

mysql -h 172.20.0.10 -u sarah_chen -p'Portfolio2024!' customer_db --ssl-mode=DISABLED -e "
SELECT client_id, account_balance FROM clients WHERE status='active';
SELECT * FROM trades WHERE trade_date = CURDATE();
UPDATE client_activity SET last_login = NOW() WHERE client_id = 1001;
"
