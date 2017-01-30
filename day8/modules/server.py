#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import socket, socketserver, pickle, sys, os, subprocess, hashlib, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
         while True:
            try:
                self.data = self.request.recv(1024).strip().decode()
                print("{}收到消息:{}".format(self.client_address[0], self.data))
                cmd_dic = json.loads(str(self.data))
                action = cmd_dic["action"]
                if hasattr(self, action):
                    function = getattr(self, action)
                    function(cmd_dic)
            except ConnectionResetError as e:
                print("error", e)
                break


# class Ftpserver(object):
#
#     def __init__(self):
#         self.login_type = False
#
#         self.server = socketserver.socket()
#         self.server.bind(('localhost', 999))
#         self.server.listen(5)
#
#     def __del__(self):
#         self.server.close()
#
#     def run(self):
#         '''
#         执行命令解析,以"|"为分隔符
#         :return:
#         '''
#         print("等待客户端的连接...")
#         self.conn, addr = self.server.accept()
#         print("新连接:", addr)
#         while True:
#             data = self.conn.recv(1024)
#             print("收到消息:", data)
#             cmd = data.decode().split('|')
#             if hasattr(self, cmd[0]):
#                 function = getattr(self, cmd[0])
#                 function(cmd)

    def login_in(self, msg):
        '''
        用户登录
        :param user_name:
        :param pass_word:
        :return:
        '''
        user_name = msg["username"]
        pass_word = msg["pass_word"]
        self.user_name = user_name
        login_dict = json.load(open(setting.PATH_USE, 'r'))
        rs = ''
        if user_name in login_dict.keys():

            if login_dict[user_name]['password'] == pass_word:
                self.login_type = True
                self.path = login_dict[user_name]['user_path']
                rs = '200'
            else:
                rs = '400'
        else:
            rs = '400'
        self.request.send(rs.encode())

    def ls(self, msg):
        '''
        查询不同用户HOME目录下的文件
        :param msg:
        :return:
        '''
        res = subprocess.Popen('ls -rlt', shell=True, stdout=subprocess.PIPE, cwd=self.path)  # 查询当前目录下文件
        res_data = res.stdout.read()
        msg_dic = {
            "size": len(res_data),
        }
        self.request.send(json.dumps(msg_dic).encode())
        self.request.recv(1024)
        self.request.send(res_data)

    def put(self, msg):
        '''
        客户端的PUT命令，即服务器端获取数据
        :param msg:
        :return:
        '''

        # 配额检查
        if msg["size"] + os.stat(self.path).st_size > setting.PATH_USE[self.user_name]["user_size"]:
            self.request.send(b'400')   # 用户配额不足
        else:
            self.request.send(b'200')  # 用户配额足
            file = self.request.recv(1024)           # 接收文件
            with open(os.path.join(self.path, msg["filename"]), 'wb') as f:
                f.write(file)

            f_size = os.path.getsize(os.path.join(self.path, msg["filename"]))
            if f_size == msg["size"]:    # 校验是否下载完成
                self.request.send('数据发送完成'.encode())

    def get(self, msg):
        '''
        客户端的get命令，即服务器端发送数据
        :param msg:
        :return:
        '''
        get_file = os.path.basename(msg[1])
        file_path = os.path.join(self.path, get_file)
        if not os.path.isfile(file_path):
            self.request.send('False|0'.encode())
        else:
            size = os.path.getsize(file_path)
            self.request.send(('True|' + str(size)).encode())  # 发送成功标示、文件大小
            data = self.request.recv(10240).decode()
            if data == 'ready':
                with open(file_path, 'rb') as f:
                    send_data = f.read()
            else:
                send_data = 0
            self.request.send(send_data)

# a ={'x1': {'name': 'xx', 'password': '123', 'path': '/x1'}, 'ftp': {'name': 'ftp', 'password': '123', 'path': '/ftp'}}
# pickle.dump(a, open(os.path.join(setting.PATH_DB, 'login.pkl'), 'wb'))
