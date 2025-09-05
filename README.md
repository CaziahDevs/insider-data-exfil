# Insider Data Exfiltration Lab

A cybersecurity lab demonstrating ARP spoofing attacks with credential interception and automated data exfiltration.

## Overview

This project simulates a man-in-the-middle attack using ARP spoofing to intercept database credentials and exfiltrate captured data to a remote server. The lab demonstrates network-based insider threat techniques and credential harvesting.

## Attack Flow

1. **ARP Spoofing**: Attacker performs ARP spoofing to position as man-in-the-middle
2. **Database Queries**: Workstation triggers database connections (`./db_queries.sh`)
3. **Traffic Interception**: Attacker captures credentials in transit (`./capture_creds.py`)
4. **Data Exfiltration**: Stolen credentials sent to exfil server (`./exfil.py`)
5. **Verification**: Exfil-server logs and displays captured data

## Components

- **ARP Spoofing Module**: Network layer attack implementation
- **Credential Capture**: Python-based packet sniffing and credential extraction
- **Data Exfiltration**: Automated transmission of captured data
- **Exfiltration Server**: Remote server for data collection and logging
- **Database Query Simulator**: Workstation script to generate target traffic

## Technical Stack

- **Python**: Core attack scripts and packet manipulation
- **Bash**: Automation and database query simulation
- **Network Protocols**: ARP, TCP packet crafting and analysis

## Learning Objectives

- Understand ARP spoofing attack vectors and implementation
- Practice credential interception techniques
- Develop skills in network traffic analysis and packet capture
- Learn automated data exfiltration methods

## Detection & Response

### SIEM Alerts
- **Foreign Device Detection**: Network access control (NAC) systems trigger alerts for unrecognized MAC addresses and device fingerprints
- **Anomalous ICMP Traffic**: SIEM correlation rules detect periodic ICMP pings with unusual payload sizes or frequency patterns
- **ARP Anomalies**: Monitoring for duplicate IP assignments and ARP response inconsistencies

### Incident Response
1. **Immediate Containment**: Isolate affected network segments and quarantine suspicious devices
2. **Forensic Analysis**: Capture network traffic, analyze ARP tables, and examine ICMP packet contents
3. **Credential Reset**: Force password changes for all potentially compromised database accounts
4. **Network Hardening**: Implement dynamic ARP inspection and enhanced network segmentation
5. **Physical Security Review**: Audit access controls and implement additional tailgating prevention measures

## Security Notice

⚠️ **For Educational Use Only** - This lab contains network attack tools. Use only in authorized lab environments.
