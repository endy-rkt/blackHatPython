import socket

# Target IP and Port
target_host = "127.0.0.1"
target_port = 8000

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send a message
msg = "Hello world"
client.send(msg.encode('utf-8'))

# Receive a response
data = client.recv(4096)
print("Received:", data.decode('utf-8'))

# Close the socket
client.close()
