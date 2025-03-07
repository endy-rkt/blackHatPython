#!/bin/python3

import paramiko
import socket
import threading
import subprocess
import sys

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        print(f"Received channel request: {kind}, channel id: {chanid}")
        
        if kind == "session":
            print("Session request received")
            return paramiko.OPEN_SUCCEEDED
        elif kind == "pty-req":
            print("PTY request received")
            return paramiko.OPEN_SUCCEEDED  # Allow PTY request
        elif kind == "shell":
            print("Shell request received")
            return paramiko.OPEN_SUCCEEDED  # Allow shell request
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        print(f"Checking credentials for {username}")
        if username == "debian" and password == "debian":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"  # Allow password authentication

    def check_channel_shell_request(self, channel):
        # This method is necessary to handle shell requests explicitly.
        print("Handling shell request...")
        channel.send("Welcome to the ft_ssh shell!\n")
        return True

    def handle_command(self, cmd, channel):
        """Handle command execution in the shell."""
        try:
            cmd_output = subprocess.check_output(cmd, shell=True)
            channel.send(cmd_output)
        except subprocess.CalledProcessError as e:
            channel.send(f"Error: {e}\n")
        except Exception as e:
            channel.send(f"Failed to execute command: {e}\n")

if __name__ == "__main__":
    host_key = paramiko.RSAKey(filename="test_rsa.key")
    server = sys.argv[1]
    ssh_port = int(sys.argv[2])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(10)
        print("[+] Listening for connection...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-] Listen failed: " + str(e))
        sys.exit(1)
    print("[+] Got a connection")

    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()

        try:
            bhSession.start_server(server=server)
        except paramiko.SSHException:
            print("[-] SSH negotiation failed.")

        chan = bhSession.accept(20)
        if chan is None:
            print("[-] No channel received.")
            sys.exit(1)
        print("[+] Authenticated!")
        print(chan.recv(1024).decode())
        chan.send("Welcome to ft_ssh")

        while True:
            try:
                # Receive the command from the client and execute it
                cmd = chan.recv(1024).decode("utf-8").strip()
                if cmd == "exit":
                    chan.send("Exiting\n")
                    print("Exiting the session")
                    bhSession.close()
                    break
                elif cmd:
                    # Execute the command and return output
                    server.handle_command(cmd, chan)
                else:
                    chan.send("Empty command received.\n")
            except KeyboardInterrupt:
                bhSession.close()
                break
            except Exception as e:
                print("[-] Caught exception: " + str(e))
                bhSession.close()
                break
    finally:
        sys.exit(1)
