#!/usr/bin/env python3

import os
import socket
import struct

# Host to listen on
host = "0.0.0.0"

# Check OS and select appropriate protocol
if os.name == "nt":  # Windows
    socket_protocol = socket.IPPROTO_IP
else:  # Linux/Mac
    socket_protocol = socket.IPPROTO_ICMP

# Create raw socket
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

# Bind to the host
sniffer.bind((host, 0))

# Include IP headers in capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Enable promiscuous mode on Windows
if os.name == "nt":
    import ctypes
    sniffer.ioctl(socket.SIO_RCVALL, ctypes.c_ulong(1))  # Enable

# Read in a single packet
print("Listening for incoming packets...")
packet, addr = sniffer.recvfrom(65565)
print(f"Received Packet from {addr}: {packet}")

# Disable promiscuous mode on Windows after capture
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, ctypes.c_ulong(0))  # Disable
