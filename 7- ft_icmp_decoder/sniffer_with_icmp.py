#!/usr/bin/python3

import	time
import	socket
import	threading
from netaddr import IPNetwork, IPAddress

#host to listen on 
# host = "127.0.0.1"
host = "172.18.0.1"

#subnet to target
subnet = "172.18.0.0/16"

#magic string we'll check ICMP responses for 
magic_message = "PYTHONRULES!"

#this sprays out the UDP datagrams
def	udp_sender(subnet, magic_message):
	time.sleep(5)
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	for ip in IPNetwork(subnet):
		try:
			sender.sendto(magic_message, (ip, 65212))
			# sender.sendto(magic_message,("%s" % ip,65212))
		except:
			pass

#start sending packets
t = threading.Thread(target=udp_sender, args=(subnet, magic_message))
t.start()

try:
	while True:
		print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}")

		#now check for the TYPE 3 and CODE 
		if icmp_header.coder == 3 and icmp_header.type == 3:

			#make sure host is in our target subnet
			if IPAddress(ip_header.src_address) in IPNetwork(subnet):
				#make sure it has our magic message
				if raw_buffer[len(raw_buffer) - len(magic_message):] == magic_message:
					print(f"Host Up {ip_header.src_address}")