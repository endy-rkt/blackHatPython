#!/bin/python3
import socket
import sys
import threading

target_host = "127.0.0.1"
target_port = 8000

#create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)

print(f"[*] Connected to: {target_port}")

#connect
try:
	client.connect((target_host, target_port))

except BlockingIOError:
	print("Connection in progression...")

#receiving response
def	handle_receive():
	while True:
		try:
			response = client.recv(4096)
			response = response.decode().strip()
			if (response.lower() == "quit"):
				print("Quitting...")
				client.close()
				sys.exit()
			print(f"{response}")
		except BlockingIOError:
			pass
		except Exception as e:
			print(f"\nError receiving data: {e}")
			client.close()
			sys.exit()

#receive in another thread
receive_thread = threading.Thread(target=handle_receive, daemon=True)
receive_thread.start()

while True:
	try:
		msg = input()
		msg += "\n"
		client.send(msg.encode("utf-8"))
	except BlockingIOError:
			pass
	except KeyboardInterrupt:
		print("\nExiting...")
		client.close()
		sys.exit()
	except Exception as e:
			print(f"\nError receiving data: {e}")
			client.close()
			sys.exit()

client.close()
