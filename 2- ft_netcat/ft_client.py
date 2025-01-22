#!/bin/python3
import socket
import sys
import threading
import subprocess

def link(args):
	#create socket
	hostIP = args["IP"]
	port = args["PORT"]
	cmd = args["CMD"]
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.setblocking(False)
	print(f"[*] Connected to: {port}")

	#connect
	try:
		client.connect((hostIP, port))

	except BlockingIOError:
		print("Connection in progression...")
	#receive in another thread
	receive_thread = threading.Thread(target=handle_receive, args=(client,))
	receive_thread.daemon = True
	receive_thread.start()
	CMDEXECUTED = 0
	while True:
		try:
			msg = ""
			if cmd and CMDEXECUTED == 0:
				result = subprocess.run(cmd, capture_output=True, text=True)

				# The output is in result.stdout as a string
				msg = result.stdout.strip()
				CMDEXECUTED = 1
			else:
				msg = input()
			msg += "\n"
			client.send(msg.encode("utf-8"))
			if (CMDEXECUTED):
				receive_thread.join()
				client.close()
				sys.exit()
		except BlockingIOError:
				pass
		except KeyboardInterrupt:
			print("\nExiting...")
			receive_thread.join()
			client.close()
			sys.exit()
		except Exception as e:
				print(f"\nError receiving data: {e}")
				receive_thread.join()
				client.close()
				sys.exit()
	receive_thread.join()
	client.close()
	sys.exit()

#receiving response
def	handle_receive(client):
	while True:
		try:
			response = client.recv(4096)
			response = response.decode().strip()
			if (response.lower() == "quit"):
				print("Quitting...")
				break
			print(f"{response}")
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"\nError receiving data: {e}")
			break