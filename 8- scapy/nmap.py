#port scan
# from scapy.all import *

# target_ip = "127.0.0.1"

# ports = [i for i in range(1000)]

# for port in ports:
#     print(f"port={port}")
#     packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
#     response = sr1(packet, timeout=1, verbose=0)
#     if response:
#         if respone[TCP].flags == "SA":
#             print(f"port {port} open.")
#         elif response[TCP].flags == "RA":
#             print(f"port {port} closed.")

from scapy.all import IP, TCP, sr1

# target_ip = "127.0.0.1"
target_ip = "10.0.2.15"
ports = [i for i in range(20)]

for port in ports:
    print(f"Scanning port={port}")
    packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)
    if response and response.haslayer(TCP):
        tcp_flags = response[TCP].flags
        if tcp_flags == 0x12:  # SYN-ACK
            print(f"Port {port} open.")
        elif tcp_flags == 0x14:  # RST-ACK
            print(f"Port {port} closed.")