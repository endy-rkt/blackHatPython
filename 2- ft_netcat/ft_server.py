#!/bin/python3
import sys
import time
import socket
import threading

def serve(args):
	#create socket
	bindIP = args["IP"]
	port = args["PORT"]
	cmd = args["CMD"]
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	server.setblocking(False)

	try:
		server.bind((bindIP, port))
		server.listen(10) #only 10 connection
		print(f"Listening on {bindIP}:{port}...")
	except BlockingIOError:
		pass
	while True:
		try:
			client_socket, addr = server.accept()

			print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))
			receive_thread = threading.Thread(target=handle_receive, args=(client_socket, server))
			send_thread = threading.Thread(target=handle_send, args=(client_socket, server))

			receive_thread.daemon = True
			send_thread.daemon = True

			send_thread.start()
			receive_thread.start()
		except BlockingIOError:
			time.sleep(0.1)
		except BlockingIOError:
				pass
		except KeyboardInterrupt:
			print("\nExiting...")
			receive_thread.join()
			handle_receive.join()
			client_socket.close()
			server.close()
			sys.exit()
		except Exception as e:
				print(f"\nError receiving data: {e}")
				receive_thread.join()
				handle_receive.join()
				client_socket.close()
				server.close()
				sys.exit()
	receive_thread.join()
	handle_receive.join()
	client_socket.close()				
	server.close()
	sys.exit()

def	handle_receive(client_socket, server):
	try:
		while True:
			request = client_socket.recv(1024).decode('utf-8').strip()
			if (request == "quit"):
				client_socket.close()
				break
			print(f"{request}")
	except BlockingIOError:
			pass
	except Exception as e:
			print(f"\nError receiving data: {e}")

def handle_send(client_socket, server):
	try:
		while True:
			response = input()
			response += "\n"
			client_socket.send(response.encode("utf-8"))
	except BlockingIOError:
			pass
	except Exception as e:
			print(f"\nError receiving data: {e}")