#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os

PATH = os.path.dirname(os.path.dirname(__file__))
PATH_DB = os.path.join(PATH, 'db')
PATH_modules = os.path.join(PATH, 'modules')
PATH_LOG = os.path.join(PATH, 'log')

PATH_STUDENT = os.path.join(PATH_DB, 'student')
PATH_MANAGER = os.path.join(PATH_DB, 'manager')
PATH_LOGFILE = os.path.join(PATH_LOG, 'log.log')


USER_STATUS = {'manager': False, 'student': False}

