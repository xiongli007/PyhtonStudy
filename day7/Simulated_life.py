#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


class person(object):

    def __init__(self, name, sex, work, race, nationality, specialty, money):
        self.name = name
        self.sex = sex
        self.work = work
        self.race = race
        self.nationality = nationality
        self.specialty = specialty
        self.money = money

    def talk(self, info):
        print(self.name, info)


a = person('xx','x','ooxx','re1','123','python',100000)
a.talk('吊死')
