#!/bin/python3

import os
from getpass import getpass
try:
    from tqdm import tqdm
except:
    os.system('pip3 install tqdm')
    from tqdm import tqdm

_host = input('Endereço do Banco: ')
_string = input('String de conexão: ')
_user = getpass('User: ')
_pass = getpass('Pass: ')

with open('/opt/Projeto_OS/software/ora.conf', 'w+') as file:
    file.write(f"""host={_host}
string={_string}
user={_user}
pass={_pass}""")


def exec(_command):
    os.system(_command)


commands = ['apt install unzip',
            '/opt/Projeto_OS/ora_install.py',
            'cp /opt/Projeto_OS/eunix_os.service /etc/systemd/system/',
            'chmod -R 770 /opt/Projeto_OS',
            'systemctl enable eunix_os && systemctl start eunix_os']

for x in tqdm(commands):
    exec(x)
