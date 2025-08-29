# insider-data-exfil
Start ARP spoofing (attacker)
Trigger database queries (workstation runs ./db_queries.sh)
Monitor traffic interception (attacker runs ./capture_creds.py)
Exfiltrate captured data (attacker runs ./exfil.py)
Verify stolen data (exfil-server shows logged data)
