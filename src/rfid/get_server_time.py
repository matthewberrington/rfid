import paramiko

# host = "169.254.1.1"
# host = "speedwayr-12-36-0F"
host = "speedwayr-12-36-0F.local"
username = "root"
password = "impinj"
command = "show system summary"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command(command)
print(_stdout.read().decode())
client.close()