#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def show_world(name):
    cur_thread = threading.currentThread()

    print "Thread : " + cur_thread.name + " : " + name
    return


pool = ThreadPool(4)

names = ['xx', 'yy']

pool.map(show_world, names)
