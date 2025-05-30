#sniff packet though all interfaces

from scapy.all import *

packet = sniff(count=10)

# print(packet)

packet.summary()