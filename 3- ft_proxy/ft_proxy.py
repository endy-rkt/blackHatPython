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
        server.bind((args.localhost, int(args.localport)))
    except socket.error as exc:
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


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join([b"%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(
            b"%04X  %-*s  %s" % (i, length * (digits + 1), hexa, text)
        )
    print(b'\n'.join(result))

def receive_from(connection):
    buffer = b''

    # We set a 2 second time-out. Depending on your target this may need
    # to be adjusted
    connection.settimeout(2)

    try:
        # keep reading into the buffer until there's no more data or we
        # time-out
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    
    except TimeoutError:
        pass
    return buffer

#modify any requests destined for the remote host
def request_handler(buffer):
    #we perform packet modification here
    return (buffer)

#modify any responses destined for the local host
def response_handler(buffer):
    #we perform packet modification here
    return buffer

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

