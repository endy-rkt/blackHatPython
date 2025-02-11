#!/bin/python3
import sys
import socket
import textwrap
import argparse
import threading
import subprocess

def run_command(cmd):
    cmd = cmd.rstrip()
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return output

def client_handler(args, client_socket):
    # upload file
    if args.upload is not None:
        file_buffer = b""  # Use bytes instead of string
    
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        
        try:
            with open(args.upload, "wb") as fd:  # 'with' ensures file is closed automatically
                fd.write(file_buffer)
            client_socket.send(f"Successfully saved file to {args.upload}\r\n".encode("utf-8"))
        except OSError:
            client_socket.send(f"Failed to save file to {args.upload}\r\n".encode("utf-8"))
    
    # execute command
    if args.execute is not None:
        output = run_command(args.execute)
        client_socket.send(output)
    
    # command shell
    if args.command:
        while True:
            client_socket.send("<minincat:#> ".encode("utf-8"))
            cmd_buffer = b""

            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            response = run_command(cmd_buffer.decode("utf-8"))
            client_socket.send(response)
    
    client_socket.close()  # Make sure to close the socket after handling it

def server_loop(_args):
    print(f"[*] Listen on {_args.target}:{_args.port}...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((_args.target, _args.port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(_args, client_socket))
        client_thread.start()

def client_sender(args, buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((args.target, args.port))

        if len(buffer):
            client.send(buffer.encode("utf-8"))
        
        while True:
            recv_len = 1
            response = b''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response.decode("utf-8"), end=' ')

            buffer = input("")
            buffer += "\n"

            client.send(buffer.encode("utf-8"))
    except socket.error as exc:
        print("[*] Exception! Existing.")
        print(f"[*] Caught exception socket.error: {exc}")
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="my_netcat",
        description="A netcat-like cli",
        usage=textwrap.dedent('''Example:
            ft_netcat.py -t 127.0.0.1 -p 5555 -l -c # command shell
            ft_netcat.py -t 127.0.0.1 -p 5555 -l -u=mytest.txt # upload file
            ft_netcat.py -t 127.0.0.1 -p 5555 -l -e="cat /etc/passwd" # execute command
            echo 'ABC' | ./ft_netcat.py -t 127.0.0.1 -p 135 # echo text to server port 135
            ft_netcat.py -t 127.0.0.1 -p 5555 # connect to server
        '''),
        epilog="Thanks for using %(prog)s",
        add_help=True
    )
    parser.add_argument("-c", "--command", action="store_true", help="command shell")
    parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument("-l", "--listen", action="store_true", help="listen")
    parser.add_argument("-p", "--port", type=int, default=8000, help="specified port")
    parser.add_argument("-t", "--target", default="127.0.0.1", help="specified IP")
    parser.add_argument("-u", "--upload", help="upload file")
    args = parser.parse_args()

    if not args.listen:
        buffer = sys.stdin.read()
        client_sender(args, buffer)
    if args.listen:
        server_loop(args)
