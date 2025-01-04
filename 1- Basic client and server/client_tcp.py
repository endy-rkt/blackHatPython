import socket

# Target Server Details
target_host = "127.0.0.1"
target_port = 8000

# Create a TCP Socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the Server
client.connect((target_host, target_port))

while True:
	# Send a Message to the Server
	clientMsg = input("Enter you message:")
	client.send(clientMsg.encode('utf-8'))

	# Receive a Response
	response = client.recv(4096)
	print(f"[+] Server Response: {response.decode('utf-8')}")
	if (clientMsg.lower() == "quit"):
		print("Quitting ...")
		break

# Close the Connection
client.close()
