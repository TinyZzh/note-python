#!/usr/bin/python
# -*- coding: UTF-8 -*-

print "你好，世界"

flag = 1

if ( flag == 1 ) :
    print "flag=1"
else :
    print "flag exlse"

print "endl"

print max(1, 10)
print min(1, 10)

def max(a, b) :
    return a < b and a or b

def min(a,b):
    if a > b :
        return a
    else :
        return b