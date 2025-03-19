#!/bin/python3
import sys
import time
import socket
import threading

#listening ip and port
bind_ip = "0.0.0.0"
bind_port = 8000

#create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
server.setblocking(False)

try:
	server.bind((bind_ip, bind_port))
	server.listen(10) #only 10 connection
except BlockingIOError:
	pass

def	handle_receive(client_socket):
	try:
		while True:
			request = client_socket.recv(1024).decode('utf-8').strip()
			if (request == "quit"):
				client_socket.close()
				server.close()
				sys.exit()
			print(f"{request}")
	except BlockingIOError:
			pass
	except Exception as e:
			print(f"\nError receiving data: {e}")
			client_socket.close()
			server.close()
			sys.exit()

def handle_send(client_socket):
	try:
		while True:
			response = input()
			response += "\n"
			client_socket.send(response.encode("utf-8"))
	except BlockingIOError:
			pass
	except Exception as e:
			print(f"\nError receiving data: {e}")
			client_socket.close()
			server.close()
			sys.exit()

while True:
	try:
		client_socket, addr = server.accept()

		print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
		receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
		send_thread = threading.Thread(target=handle_send, args=(client_socket,))
		
		receive_thread.daemon = True
		send_thread.daemon = True
		
		send_thread.start()
		receive_thread.start()
	except BlockingIOError:
		time.sleep(0.1)