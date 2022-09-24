#!/bin/python3

# OS Linux Debian 10
# Tested in Python 3.10
# Oracle Client Linux --Version: 21.4
# Instruções encontradas pelo mantenedor do pacote, mais informçaões no link:
# https://www.oracle.com/br/database/technologies/instant-client/linux-x86-64-downloads.html

import os

print('Criando Diretório Oracle...')

if os.path.isdir('/opt/oracle'):
          print("O diretório Oracle já existe!")
else:
      os.system('mkdir /opt/oracle')
      print('Realizando Download Client Oracle...')
      os.system('cd /opt/oracle && \
                 wget https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basic-linux.x64-21.4.0.0.0dbru.zip && \
                 unzip instantclient-basic-linux.x64-21.4.0.0.0dbru.zip')

print('instalando biblioteca libaio1...')

os.system('apt install libaio1')

print('Atualizando Diretório...')

os.system('sh -c "echo /opt/oracle/instantclient_21_4 > \
      /etc/ld.so.conf.d/oracle-instantclient.conf"')

os.system('ldconfig')

print('Adcionando as variaveis de ambiente...')

os.system('export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_4:$LD_LIBRARY_PATH')

os.system('export PATH=/opt/oracle/instantclient_21_4:$PATH')

print('Oracle Client instalado com sucesso!')