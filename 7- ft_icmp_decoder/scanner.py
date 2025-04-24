#!/usr/bin/env python3

import os
import socket
import struct
from ctypes import *
import threading
import time
from netaddr import IPNetwork, IPAddress

# --- CONFIGURATION ---

host = "10.0.2.15"
subnet = "10.0.2.0/24"
magic_message = b"PYTHONRULES!"      # Magic string to identify our packets

# --- IP Header ---

class IP(Structure):
    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_uint32),
        ("dst",           c_uint32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

# --- ICMP Header ---

class ICMP(Structure):
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass

# --- UDP Sender Thread ---

def udp_sender(subnet, magic_message):
    time.sleep(5)  # Give sniffer time to start
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message, (str(ip), 65212))
        except Exception:
            pass

# --- Main Sniffer Logic ---

def main():
    # Set socket protocol based on OS
    socket_protocol = socket.IPPROTO_ICMP
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    # Start UDP sender thread
    t = threading.Thread(target=udp_sender, args=(subnet, magic_message))
    t.start()

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ip_header = IP(raw_buffer[0:20])
            
            # Only process ICMP responses
            if ip_header.protocol == "ICMP":
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + sizeof(ICMP)]
                icmp_header = ICMP(buf)

                # Destination Unreachable (Type 3), Port Unreachable (Code 3)
                if icmp_header.type == 3 and icmp_header.code == 3:
                    # Check if source IP is in our subnet
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                        # Check for the magic message at the end of the packet
                        if raw_buffer[-len(magic_message):] == magic_message:
                            print(f"Host Up: {ip_header.src_address}")

    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        print("\nStopped.")

if __name__ == "__main__":
    main()