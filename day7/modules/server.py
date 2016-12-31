#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import socket, pickle, sys, os, subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting


class Ftpserver(object):

    def __init__(self):
        self.login_type = False

        self.server = socket.socket()
        self.server.bind(('localhost', 999))
        self.server.listen(5)

    def __del__(self):
        self.server.close()

    def run(self):
        '''
        执行命令解析,以"|"为分隔符
        :return:
        '''
        print("等待客户端的连接...")
        self.conn, addr = self.server.accept()
        print("新连接:", addr)
        while True:
            data = self.conn.recv(1024)
            print("收到消息:", data)
            cmd = data.decode().split('|')
            if hasattr(self, cmd[0]):
                function = getattr(self, cmd[0])
                function(cmd)

    def login_in(self, msg):
        '''
        用户登录
        :param user_name:
        :param pass_word:
        :return:
        '''
        user_name = msg[1]
        pass_word = msg[2]
        self.user_name = user_name
        login_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'login.pkl'), 'rb'))
        print(login_dict)
        rs = ''
        if user_name in login_dict.keys():

            if login_dict[user_name]['password'] == pass_word:
                self.login_type = True
                self.path = login_dict[user_name]['path']
                rs = '1'
            else:
                rs = '2'
        else:
            rs = '2'
        self.conn.send(rs.encode('utf-8'))

    def ls(self, msg):
        '''
        查询不同用户HOME目录下的文件
        :param msg:
        :return:
        '''
        res = subprocess.Popen('ls -rlt', shell=True, stdout=subprocess.PIPE, cwd=self.path)  # 查询当前目录下文件
        self.conn.send(res.stdout.read())

    def put(self, msg):
        '''
        客户端的PUT命令，即服务器端获取数据
        :param msg:
        :return:
        '''
        put_file = os.path.basename(msg[1])
        self.conn.send(self.path.encode())
        file_size = self.conn.recv(1024).decode()      # 接收文件大小
        self.conn.send(('文件大小已接收: %s' % file_size).encode())
        file = self.conn.recv(10240)           # 接收文件
        with open(os.path.join(self.path, put_file), 'wb') as f:
            f.write(file)

        f_size = os.path.getsize(os.path.join(self.path, put_file))
        if f_size == int(file_size):
            self.conn.send('数据发送完成'.encode())

    def get(self, msg):
        '''
        客户端的get命令，即服务器端发送数据
        :param msg:
        :return:
        '''
        get_file = os.path.basename(msg[1])
        file_path = os.path.join(self.path, get_file)
        if not os.path.isfile(file_path):
            self.conn.send('False|0'.encode())
        else:
            size = os.path.getsize(file_path)
            self.conn.send(('True|' + str(size)).encode())  # 发送成功标示、文件大小
            data = self.conn.recv(10240).decode()
            if data == 'ready':
                with open(file_path, 'rb') as f:
                    send_data = f.read()
            else:
                send_data = 0
            self.conn.send(send_data)

# server_ftp = Ftpserver()
#
# while True:
#     server_ftp.run()

# a ={'x1': {'name': 'xx', 'password': '123', 'path': 'C:/x1'}, 'ftp': {'name': 'ftp', 'password': '123', 'path': '/ftp'}}
# pickle.dump(a, open(os.path.join(setting.PATH_DB, 'login.pkl'), 'wb'))
