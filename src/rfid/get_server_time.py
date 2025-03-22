import paramiko
from datetime import datetime

def send_command(host, username, password, command):
	client = paramiko.client.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, username=username, password=password)
	_stdin, _stdout,_stderr = client.exec_command(command)
	client.close()
	return _stdout.read().decode()

def get_time_UTC(host, username, password):
	command = "show system summary"
	ret = send_command(host, username, password, command)
	print(ret)

def set_time_UTC(host, username, password):
	t = datetime.utcnow()
	command = "config system time " + t.strftime("%Y.%m.%d-%H:%M:%S")
	ret = send_command(host, username, password, command)
	print(ret)

if __name__ == '__main__':
	# host = "169.254.1.1"
	# host = "speedwayr-12-36-0F"
	host = "speedwayr-12-36-0F.local"
	username = "root"
	password = "impinj"