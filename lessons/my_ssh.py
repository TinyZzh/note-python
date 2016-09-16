#!/usr/bin/python
# -*- coding: UTF-8 -*-


import paramiko
import sys

# sys.argv

host = '192.168.230.129'
port = 22

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(host, port, 'root', 'centos')
# stdin, stdout, stderr = client.exec_command('date -R')
stdin, stdout, stderr = client.exec_command('iostat')

while not stdout.channel.exit_status_ready():

    cmd_result = stdout.read(), stderr.read()
    for line in cmd_result:
        print line,
    pass

client.close()

print "endl"


