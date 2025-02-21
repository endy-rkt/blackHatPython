#!/bin/python3

import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname="bandit.labs.overthewire.org", username="bandit0", password="bandit0", port=2220)
ssh_client.connect(hostname="localhost", username="debian", password="debian", port=22)
sftp = ssh_client.open_sftp()

#uploading file
sftp.put("/home/debian/Downloads/wp.zip", "/home/debian/wp.zip")


#downloading file
sftp.get("./wp.zip", "/home/debian/wp.zip")

stdin, stdout, stderr = ssh_client.exec_command("pwd")
print(stdout.read().decode())
ssh_client.close()