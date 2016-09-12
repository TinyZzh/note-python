#!/usr/bin/python
# -*- coding: UTF-8 -*-


import thread
import threading


def show_world(name):
    cur_thread = threading.currentThread()

    print "Thread : " + cur_thread.name + "print : " + name
    return


try:
    thd1 = thread.start_new_thread(show_world, ("xx",))
    thd2 = thread.start_new_thread(show_world, ("yy",))



except:
    print "Error: unable to start thread"

print "endl"

while 1:
    pass
