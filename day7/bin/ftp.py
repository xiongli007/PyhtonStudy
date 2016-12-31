#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import socket
import pickle


class Ftpserver(object):

    def __init__(self):
        self.login_type = False

    def login_in(self, user_name, pass_word):
        '''
        用户登录
        :param user_name:
        :param pass_word:
        :return:
        '''
        self.user_name = user_name
        login_dict = pickle.load(open('db\login.pkl', 'rb'))
        rs = ''
        if user_name in login_dict.keys():

            if login_dict[user_name]['password'] == pass_word:
                self.login_type = True
                rs = '登录成功'
            else:
                rs = '输入的帐号或密码错误'
        else:
            rs = '输入的帐号或密码错误'
        return self.login_type, rs


# login_dict ={
#     'ftp': {'name': 'ftp', 'password': '123', 'path': '/ftp'},
#     'xx': {'name': 'xx', 'password': '123', 'path': '/xx'}
# }
# with open('db/login.pkl', 'wb') as f:
#     pickle.dump(login_dict, f)

#
# ftpserver = Ftpserver()
# type, rsmsg = ftpserver.login_in('xx', '1234')
# print(type, rsmsg)
