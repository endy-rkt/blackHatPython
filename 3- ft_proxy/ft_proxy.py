#!/bin/python3
import sys
import socket
import argparse
import textwrap
import threading

def server_loop(args):
    #main server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((args.loclhost, int(args.localport)))
    except:
        print(f"Failed to listen on {args.localhost}:{args.localport}")
        sys.exit(0)
    
    print(f"[*] Listening on {args.localhost}:{args.localport}...")
    server.listen(5)

    while True:
        #client socket
        client_socket, addr = server.accept()
        print("[==>] Received incoming connection from {addr[0]}:{addr[1]}")

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, args))
        proxy_thread.start()


def proxy_handler(client_socket, args):
    #remote host socket 
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_socket.connect((args.remotehost, int(args.remoteport)))

    #receive data from the remote end if necessary
    if args.receive_first:
        remote_buffer = receive_from(args.remote_socket)
        hexdump(remote_buffer)

        #send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        #if we have data to send to our local client, send it
        if len(remote_buffer):
            print(f"[<==] Sending {len(remote_buffer)} bytes to localhost.")
            client_socket.send(remote_buffer.encode("utf-8"))
        
        #now lets loop and read from local,
        #send to remote, send to local
        #rinse, wash, repeat
        while True:
            #read from local host
            local_buffer = receive_from(client_socket)

            if len(local_buffer):
                print(f"[==>] Received {len(local_buffer)} bytes from localhost.")
                hexdump(local_buffer)

                #send it to our request handler
                local_buffer = request_handler(local_buffer)

                #send off the data to the remote host
                remote_socket.send(local_buffer.encode("utf-8"))
                print("[==>] Sent to remote.")
            #receive back the response
            remote_buffer  = receive_from(remote_socket)

            if len(remote_buffer):
                print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
                hexdump(remote_buffer)

                #send to our response handler
                remote_buffer = response_handler(remote_buffer)

                #send the response to the local socket
                client_socket.send(remote_buffer)

                print("[<==] Sent to localhost.")
            
            #if no more data on either side, close the connections
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.close()
                remote_socket.close()
                print("[*] No more data. Closing connections.")
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ft_proxy",
        description="A simple proxy cli in python",
        usage=textwrap.dedent('''
                ./ft_proxy.py   [localhost] [localport] [remotehost] [remoteport] [receive_first]
            
            Example:
                ./ft_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True
        '''),
        epilog="Thanks for using %(prog)s!",
        add_help=True
    )
    parser.add_argument("localhost", help="localhost ip")
    parser.add_argument("localport", help="local port")
    parser.add_argument("remotehost", help="remotehost ip")
    parser.add_argument("remoteport", help="remote port")
    parser.add_argument("receive_first", help="boolean receive_first")
    args = parser.parse_args()
    if args.receive_first == "True":
        args.receive_first = True
    elif args.receive_first == "False":
        args.receive_first = False
    else:
        print("Error receive_first can only be a boolean")
        sys.exit(1)
    server_loop(args)

