#!/usr/bin/python
# -*- coding: UTF-8 -*-

#  python class example

class Person :

    totalCount = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.step = 0
        Person.totalCount += 1

    def speak(self, world):
        print "Speak : " + world

    def walk(self):
        self.step += 1



person = Person("Mine", 15);

person.speak("Shut up")
person.walk();


print person.name;




