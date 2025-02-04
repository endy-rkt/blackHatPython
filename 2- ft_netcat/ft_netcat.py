#!/bin/python3
import argparse
import socket
import shlex
import textwrap
import threading
import sys
import subprocess

def execute_cmd(cmd):
	cmd = cmd.strip()
	if not cmd:
		return
	output =  subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
	return output.decode("utf-8")

class NetCat:
	def __init__(self, args, buffer=None):
		self.args = args
		self.buffer = buffer
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	def run(self):
		if self.args.listen:
			self.listen()
		else:
			self.send()
	
	def send(self):
		self.socket.connect((self.args.target, self.args.port))
		if self.buffer:
			self.socket.send(self.buffer)
			try:
				while True:
					recv_len = 1
					response = ""
					while recv_len:
						data = self.socket.recv(4096)
						recv_len = len(data)
						response += data.decode("utf-8")
						if (recv_len < 4096):
							break
						if response:
							print(response)
						buffer = input("> ")
						buffer += "\n"
						self.socket.send(buffer.encode("utf-8"))
			except KeyboardInterrupt:
				print("User terminated.")
				self.socket.close()
				sys.exit()
	
	def listen(self):
		self.socket.bind((self.args.target, self.args.port))
		self.socket.listen(5)
		while True:
			client_socket, _ = self.socket.accept()
			client_thread = threading.Thread(target=self.handle, args=(client_socket,))
			client_thread.start()
	
	def handle(self, client_socket):
		if self.args.execute:
			output = execute_cmd(self.args.execute)
			client_socket.send(output.encode("utf-8"))
		
		elif self.args.upload:
			file_buffer = b''
			while True:
				data = client_socket.recv(4096)
				if data:
					file_buffer += data
					print(len(file_buffer))
				else:
					break
			
			with open(self.args.upload, 'wb') as f:
				f.write(file_buffer)
			message = f"Saved file {self.args.upload}"
			client_socket.send(message.encode("utf-8"))
		
		elif self.args.command:
			cmd_buffer = b''
			while True:
				try:
					client_socket.send(b' #> ')
					while '\n' not in cmd_buffer.decode("utf-8"):
						respone = execute_cmd(cmd_buffer.decode("utf-8"))
						if respone:
							client_socket.send(respone.encode("utf-8"))
						cmd_buffer = b''
				except Exception as e:
					print(f'server killed {e}')
					self.socket.close()
					sys.exit()
						
if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description= "ft_netcat",
		formatter_class= argparse.RawDescriptionHelpFormatter,
		epilog=textwrap.dedent('''Example:
			ft_netcat.py -t 127.0.0.1 -p 5555 -l -c #command shell
			ft_netcat.py -t 127.0.0.1 -p 5555 -l -u=mytest.text #upload file
			ft_netcat.py -t 127.0.0.1 -p 5555 -l -e=\"cat /etc/passwd \" #execute command
			echo 'ABC' | ./ft_netcat.py -t 127.0.0.1 -p 135 #echo text to server port 135
			ft_netcat.py -t 127.0.0.1 -p 5555 #connect to server			
		''')
	)
	parser.add_argument('-c', '--command', action="store_true", help="command shell")
	parser.add_argument("-e", "--execute", help="execute specified command")
	parser.add_argument("-l", "--listen", action="store_true", help="listen")
	parser.add_argument("-p", "--port", type=int, default=5555, help="specified port")
	parser.add_argument("-t", "--target", default="127.0.0.1", help="specified IP")
	parser.add_argument("-u", "--upload", help="upload file")
	args = parser.parse_args()

	if args.listen:
		buffer = ""
	else:
		buffer = sys.stdin.read()
	
	nc = NetCat(args, buffer.encode("utf-8"))
	nc.run()