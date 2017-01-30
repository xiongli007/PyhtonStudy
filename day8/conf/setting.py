#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

# 环境变量，路径设置

import os

PATH = os.path.dirname(os.path.dirname(__file__))
PATH_DB = os.path.join(PATH, 'db')
PATH_modules = os.path.join(PATH, 'modules')
PATH_LOG = os.path.join(PATH, 'log')
PATH_USE = os.path.join(PATH_DB, 'usercfg.json')

SERVER_IP = 'localhost'
SERVER_PORT = 9999

