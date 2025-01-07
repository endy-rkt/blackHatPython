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
		response = client.recv(4096)
		print(f"{response.decode('utf-8')}")
		if (clientMsg.lower() == "quit"):
			print("Quitting ...")
			break

	# Close the Connection
	client.close()
