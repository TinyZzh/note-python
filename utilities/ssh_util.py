#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paramiko


# # #
#  创建连接
# # #
def ssh_client_by_psw(host, port, user, psw):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(host, port, user, psw)
    return client


# # #
#  执行命令
# # #
def ssh_exec_cmd(client, cmd):
    if client is None or cmd is None:
        return None
    try:
        _std_in, _std_out, _std_err = client.exec_command(cmd)
        while not _std_out.channel.exit_status_ready():
            _tup_result = _std_out.read(), _std_err.read()
            for line in _tup_result:
                print line
            return _tup_result
    except Exception, e:
        print e
    finally:
        client.close()
    return None
