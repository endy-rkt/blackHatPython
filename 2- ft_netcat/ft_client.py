# import sys
# import socket

# def link(hostIP, port):
# 	# Create a TCP Socket
# 	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 	# Connect to the Server
# 	client.connect((hostIP, port))

# 	while True:
# 		# Send a Message to the Server
# 		clientMsg = input()
# 		client.send(clientMsg.encode('utf-8'))

# 		# Receive a Response
# 		if (clientMsg.lower() == "quit"):
# 			print("Quitting ...")
# 			break
# 		try:
# 			client.settimeout(1)  # Optional timeout to check for server response
# 			response = client.recv(4096)
# 			if response:  # Only print if there's actual data
# 				print(f"Server response: {response.decode('utf-8')}")
# 		except socket.timeout:
# 			pass  # Time

# 	# Close the Connection
# 	client.close()

import socket
import threading

def handle_receive(client):
    """Receive messages from the server."""
    while True:
        try:
            response = client.recv(4096)
            if response:
                print(f"\nServer: {response.decode('utf-8')}")
            else:
                print("\nServer disconnected.")
                break
        except ConnectionResetError:
            print("\nServer closed the connection.")
            break
        except Exception as e:
            print(f"\nError receiving data: {e}")
            break

def handle_send(client):
    """Send messages to the server."""
    while True:
        clientMsg = input("You: ")
        if clientMsg.lower() == "quit":
            print("Quitting...")
            client.close()
            break
        client.send(clientMsg.encode('utf-8'))

def link(hostIP, port):
    # Create a TCP Socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the Server
        client.connect((hostIP, port))
        print(f"Connected to server at {hostIP}:{port}.")

        # Start threads for sending and receiving
        receive_thread = threading.Thread(target=handle_receive, args=(client,))
        send_thread = threading.Thread(target=handle_send, args=(client,))
        
        # Set threads as daemon so they close when the main program exits
        receive_thread.daemon = True
        send_thread.daemon = True

        receive_thread.start()
        send_thread.start()

        # Wait for threads to finish
        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection closed.")


