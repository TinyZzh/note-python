#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb

config = {'host': '127.0.0.1', 'db': 'fps_ins_master', 'user': 'root', 'passwd': 'wooduan'}

try:

    conn = MySQLdb.connect(host=config['host'], db=config['db'], user=config['user'], passwd=config['passwd'])
    conn.set_character_set('utf8')

    cur = conn.cursor()

    cur.execute("show databases;")
    # select
    cur.execute("SELECT * FROM `t_character` LIMIT 0,1;")
    rows = cur.fetchall()
    for row in rows:
        print row

    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

print "endl"
