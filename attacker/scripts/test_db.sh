#!/bin/bash
echo "[TEST] Testing captured credentials on database..."
mysql -h 172.20.0.10 -u sarah_chen -p'Portfolio2024!' customer_db --ssl-mode=DISABLED -e "SELECT * FROM clients;"
