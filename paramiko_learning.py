import paramiko
import yaml
import time

def getServerInfo(ip, config_file):
    f = open(config_file, 'r')
    userinfo = yaml.load(f)
    for i in userinfo:
        if i['ip'] == ip:
            return i

    return i
    f.close()
userinfo_file = 'config/userinfo.yaml'
ServerInfo = getServerInfo('176.122.179,125', userinfo_file)
print(ServerInfo)

def ssh_connect(serverinfo, command):
    ip = serverinfo['ip']
    port = serverinfo['port']
    username = serverinfo['username']
    password = serverinfo['password']

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout
    ssh.close()

command = 'ls -l /'
print(ssh_connect(ServerInfo, command).readlines())