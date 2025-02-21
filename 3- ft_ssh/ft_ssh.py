#!/bin/python3

import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname="bandit.labs.overthewire.org", username="bandit0", password="bandit0", port=2220)
stdin, stdout, stderr = ssh_client.exec_command("cat readme")
print(stdout.read().decode())
ssh_client.close()