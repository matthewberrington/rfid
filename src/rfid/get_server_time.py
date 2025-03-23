import datetime
import paramiko

def send_command(host, username, password, command):
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(command)
    if not _stderr.read() == b'':
        print('Error!')
    else:
        ret = _stdout.read()
    client.close()
    return ret

def get_time_UTC(host, username, password):
    command = "show system summary"
    ret = send_command(host, username, password, command)
    response_list = ret.decode().split('\n')
    rfid_time_UTC = datetime.datetime.strptime(response_list[5][9:-1],  '%a %b %d %H:%M:%S %Z %Y')
    return rfid_time_UTC

def set_time_UTC(host, username, password):
    t = datetime.datetime.now(datetime.timezone.utc)
    command = "config system time " + t.strftime("%Y.%m.%d-%H:%M:%S")
    ret = send_command(host, username, password, command)
    return ret

if __name__ == '__main__':
    host = "speedwayr-12-36-0F.local"
    username = "root"
    password = "impinj"
    
    # set_time_UTC(host, username, password)

    print(get_time_UTC(host, username, password))
    print(datetime.datetime.now(datetime.timezone.utc))
