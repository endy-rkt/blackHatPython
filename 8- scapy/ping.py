#crafting and sending icmp packet

from scapy.all import *

packet = IP(dst="127.0.0.1")/ICMP()

print(packet)

send(packet)