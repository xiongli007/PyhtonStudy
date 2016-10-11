#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os

PATH = os.path.dirname(os.path.dirname(__file__))
PATH_DB = os.path.join(PATH, 'db')
PATH_LOCK = os.path.join(PATH, 'db', 'lock.txt')
PATH_LOCK_NEW = os.path.join(PATH, 'db', 'locknew.txt')
PATH_USER = os.path.join(PATH, 'db')
PATH_ADMIN = os.path.join(PATH, 'db', 'admin')  # 管理员权限目录
PATH_CLIENT = os.path.join(PATH, 'db', 'client')     # 普通用户权限目录

PATH_SHOP_LOCK = os.path.join(PATH, 'db', 'shop_lock.txt')
PATH_SHOP_USER = os.path.join(PATH, 'db', 'UserMsg.txt')
PATH_SHOP_DATA = os.path.join(PATH, 'db', 'data.pkl')

ATM_LOG = os.path.join(PATH, 'log', 'atm.log')
SHOP_LOG = os.path.join(PATH, 'log', 'shop.log')

