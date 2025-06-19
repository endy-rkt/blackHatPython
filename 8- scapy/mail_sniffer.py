#!/usr/bin/python3

from scapy.all import sniff, TCP, IP

def	packet_callback(packet):
	if packet[TCP].payload:
		str_packet = str(packet[TCP].payload)
		if "user" in str_packet.lower() or "pass" in str_packet.lower():
				print(f"[*] Destination: {packet[IP].dst}")
				print(f"[*] {str(packet[TCP].payload)}")

if __name__ == "__main__":
	sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)