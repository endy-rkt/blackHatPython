import socket
import threading

#listening ip and port
bind_ip = "0.0.0.0"
bind_port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

server.bind((bind_ip, bind_port))

server.listen(5)

print("[*] Listening on {}:{} ...".format(bind_ip, bind_port))

def	handle_client(client_socket):
	while True:
		#this need to be in try catch
		request = client_socket.recv(1024).decode('utf-8')

		print("[*] Received: {}".format(request))
		
		client_socket.send("ACK!".encode("utf-8"))
		if (request.lower() == "quit"):
			print("Quitting ...")
			client_socket.close()

while True:
	client, addr = server.accept()

	print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))

	client_handler = threading.Thread(target=handle_client, args=(client,))
	client_handler.start()