import sys
import socket

def link(hostIP, port):
	# Create a TCP Socket
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the Server
	client.connect((hostIP, port))

	while True:
		# Send a Message to the Server
		clientMsg = input()
		client.send(clientMsg.encode('utf-8'))

		# Receive a Response
		if (clientMsg.lower() == "quit"):
			print("Quitting ...")
			break
		try:
			client.settimeout(1)  # Optional timeout to check for server response
			response = client.recv(4096)
			if response:  # Only print if there's actual data
				print(f"Server response: {response.decode('utf-8')}")
		except socket.timeout:
			pass  # Time

	# Close the Connection
	client.close()

