from os import cpu_count
import paramiko
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import Future
'''
By MIKA / SKIDSEC PH
'''
usableCPU = cpu_count()
procnum = 0
commandos  = [
    'sudo rm -r anti_ddos.py',
    'wget https://raw.githubusercontent.com/RENAME/RENAME/main/anti_ddos.py',
    'sudo apt update -y',
    'sudo apt install python3 -y',
    'sudo apt install curl -y',
    'chmod +x anti_ddos.py && sudo python3 anti_ddos.py'
]

try:
    host = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
except:
    print(f'Usage:\npython3 {__file__} host port username pass\n\nExample usage:\npython3 {__file__} 123.123.123.123 22 root root')
    sys.exit(0)

def Server(**cmd):
    global procnum
    procnum += 1
    print("\033[35mProcess: \033[32m{} \033[36mstarted\033[0m".format(procnum))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        sys.exit('\033[31mERROR: \033[35mInvalid host port username password\033[0m')
    stdin, stdout, stderr = ssh.exec_command(cmd['shellexec'])
    return stdout

def Main():
    with ThreadPoolExecutor(max_workers=(usableCPU-1)*2) as executor:
        ftrs = [executor.submit(Server,shellexec=cmd) for cmd in commandos]
        for fr in as_completed(ftrs):
            with open("logs.txt","a+")as f:
                f.write(f"{fr.result()}\n")
    print("\033[32m\033[1mInstalled Successfully Iptables Ruleset\033[0m")

if __name__ == '__main__':
    Main()
