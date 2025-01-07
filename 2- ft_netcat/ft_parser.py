import sys

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

def	parse():
	argLen = len(sys.argv)
	if argLen < 3:
		print("Error: insufficient number of arguments")
		sys.exit(1)
	args = {
		"LISTENNING":False,
		"VERBOSE":False,
		"PORT":-1,
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
				if args["PORT"] != -1:
					print("Error: repetitive argument")
					sys.exit(1)
				if i + 1 >= argLen:
					print("Error: Insufficient number of argument")
					sys.exit(1)
				args["PORT"] = int(sys.argv[i + 1])
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
			updateIp = 0
			if args["IP"] == "":
				args["IP"] = arg
				updateIp = 1
			if args["PORT"] == -1 and not updateIp:
				args["PORT"] = int(arg)
		i += 1
	return (args)

def checkArgs(args):
	if args["PORT"] == -1 and args["IP"] == "":
		print("Error: No port and IP")
		sys.exit(1)
	if args["LISTENNING"] and args["PORT"] == -1:
		print("Error: no port to listen on")
		sys.exit(1)