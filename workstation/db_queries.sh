#!/bin/bash
# Simulates Sarah Chen's workday with only relevant queries

declare -a QUERIES=(
    "SELECT client_id, client_name, account_balance FROM clients WHERE status='active' ORDER BY account_balance DESC"
    "SELECT c.client_name, c.ssn, c.credit_limit FROM clients c WHERE c.risk_score > 700"
    "SELECT * FROM trades WHERE trade_date = CURDATE() AND amount > 100000"
    "SELECT client_id, SUM(amount) as total_trades FROM trades GROUP BY client_id"
    "SELECT w.transfer_id, w.routing_number, w.account_number, w.amount FROM wire_transfers w WHERE w.transfer_date = CURDATE()"
    "UPDATE client_activity SET last_login = NOW(), session_count = session_count + 1 WHERE client_id = 1001"
    "SELECT p.symbol, p.shares, p.current_value FROM portfolio_holdings p JOIN clients c ON p.client_id = c.client_id WHERE c.account_balance > 2000000"
    "SELECT COUNT(*) as active_clients FROM clients WHERE status = 'active'"
    "SELECT c.client_name, c.account_type, t.security_symbol, t.amount FROM clients c JOIN trades t ON c.client_id = t.client_id WHERE t.trade_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    "SELECT client_name, ssn, account_balance FROM clients WHERE client_id IN (1001, 1002, 1003)"
)

echo "[*] Starting Sarah Chen's workday simulation..."
echo "[*] Connecting as sarah_chen to database server at 172.20.0.10"

while true; do
    # Pick a random sensitive query
    QUERY="${QUERIES[$((RANDOM % ${#QUERIES[@]}))]}"
    echo "[$(date '+%H:%M:%S')] Executing work query..."
    
    # Execute the query
    mysql -h 172.20.0.10 -u sarah_chen -p'Portfolio2024!' customer_db --ssl-mode=DISABLED -e "$QUERY" 2>/dev/null
    
    # Random delay between queries (2-8 seconds)
    sleep $((RANDOM % 7 + 2))
done
