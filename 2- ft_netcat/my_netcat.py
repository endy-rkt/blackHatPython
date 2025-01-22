#!/bin/python3
import sys
import signal
import threading
import ft_parser, ft_client, ft_server

# Signal handler with debounce logic
shutdown_flag = threading.Event()

def signal_handler(sig, frame):
    if shutdown_flag.is_set():
        return  # Ignore repeated signals
    shutdown_flag.set()
    print("\n[!] SIGINT detected. Exiting gracefully...")
    # Clean up and exit
    sys.exit(0)

def execute(args):
    try:
        if args["LISTENNING"]:
            if args["IP"] == "":
                args["IP"] = "0.0.0.0"
            ft_server.serve(args)
        else:
            ft_client.link(args)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        print("[*] Cleaning up resources...")
        shutdown_flag.set()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	args = ft_parser.parse()
	ft_parser.checkArgs(args)
	# Execute the main logic
	try:
		execute(args)
	except KeyboardInterrupt:
        # Fallback if SIGINT wasn't handled earlier
		print("\n[!] KeyboardInterrupt detected in main. Exiting...")
	finally:
		print("[*] Program exited.")
