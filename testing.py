import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="10.139.128.15", username="pinisi", password="royal32")

conn = ssh.invoke_shell()

#time.sleep(1) --> Hilangkan komentar

output = conn.recv(65535)
print(output.decode("ascii"))

ssh.close()