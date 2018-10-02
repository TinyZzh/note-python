#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import sshtunnel


def test(ssh_host, bind_host, ssh_user, ssh_psw, db_user, db_psw, db_name, bind_address=('127.0.0.1', 3306)):
    return _query(ssh_host, bind_host, ssh_user, ssh_psw, db_user, db_psw, db_name, bind_address)


def _query(ssh_host, bind_host, ssh_user, ssh_psw, db_user, db_psw, db_name, bind_address):
    with sshtunnel.open_tunnel(
            (ssh_host, 22),
            ssh_username=ssh_user,
            ssh_password=ssh_psw,
            # ssh_pkey="/var/ssh/rsa_key",
            # ssh_private_key_password="secret",
            # allow_agent=False,
            # ssh_proxy_enabled=False,
            # remote_bind_address=(global_bind_host, 3306)
            remote_bind_address=bind_address
    ) as tunnel:
        try:
            conn = MySQLdb.connect(host=tunnel.local_bind_host, db=db_name, user=db_user, passwd=db_psw)
            conn.set_character_set('utf8')

            cur = conn.cursor()

            cur.execute('show tables;')
            _rows = cur.fetchall()
            print _rows

            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return
