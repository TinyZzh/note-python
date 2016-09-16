#!/usr/bin/python
# -*- coding: UTF-8 -*-


import thread
import threading


def show_world(name):
    cur_thread = threading.currentThread()

    print "Thread : " + cur_thread.name + " : " + name
    return


try:
    thd1 = threading.Thread(target=show_world, name="Thread-xx", args=("xx",))
    thd2 = threading.Thread(target=show_world, name="Thread-yy", args=("yy",))

    thd1.start()
    thd2.start()

    thd1.join()
    thd2.join()

except Exception, e:
    print "Error: unable to start thread : " + e

print "endl"
