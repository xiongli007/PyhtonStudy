#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import json

name = json.loads(open('phone1.db', 'r'))
print(name)
# #
# with open('phone1.db', 'w', encoding='utf-8') as name:
# a = input('in...')
# print(type(a))
# # n = json.dumps(a)
# # print(type(n))
# json.dump(a, open('phone1.db', 'w', encoding='utf-8'))
