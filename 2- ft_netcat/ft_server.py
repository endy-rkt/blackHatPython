import socket
import threading

def	handle_client(client_socket):
	while True:
		#this need to be in try catch
		request = client_socket.recv(1024).decode('utf-8')

		print(request)
		msg = input()
		client_socket.send(msg.encode("utf-8"))
		if (request.lower() == "quit"):
			print("Quitting ...")
			client_socket.close()

def serve(bindIP, port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

	server.bind((bindIP, port))

	server.listen(5)

	print("[*] Listening on {}:{} ...".format(bindIP, port))

	while True:
		client, addr = server.accept()

		print("[*] Accepted connection from: {}:{}".format(addr[0], addr[1]))

		client_handler = threading.Thread(target=handle_client, args=(client,))
		client_handler.start()