#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import socket, os
import subprocess

class Ftp_client(object):
    def __init__(self):
        self.login_flag = False
        self.client = socket.socket()
        self.client.connect(('localhost', 999))

    def __del__(self):
        self.client.close()

    def login_in(self):
        '''
        登录功能
        :return:
        '''
        while not self.login_flag:
            print('请输入登录名：')
            user_name = input('>>').strip()
            print('请输入登录密码：')
            pass_word = input('>>').strip()
            if len(user_name) == 0 or len(pass_word) == 0: continue
            msg = 'login_in|' + user_name + '|' + pass_word
            self.client.send(msg.encode('utf-8'))
            data = self.client.recv(1024)
            if data.decode('utf-8') == '1':
                print('帐号：' + user_name + ' 登录成功!')
                self.login_flag = True
            else:
                print('帐号：' + user_name + ' 输入的帐号或密码错误!')

    def cmd(self):
        '''
        命令解析
        :return:
        '''
        while self.login_flag:
            print('请输入操作命令(查看当前目录文件：ls \t上传：put+文件名 \t下载：get+文件名+本地目录)：')
            cmd_input = input('>>').strip()
            if len(cmd_input) == 0: continue
            cmd_list = cmd_input.split()

            if hasattr(self, cmd_list[0]):              # 通过反射找到输入的命令方法
                function = getattr(self, cmd_list[0])   # 得到方法名
                function(cmd_list)
            elif cmd_list[0] == 'quit':
                break
            else:
                print('输入命令有误！')

    def ls(self, msg):
        '''
        查询文件
        :param msg:
        :return:
        '''
        self.client.send('ls|0'.encode())    # 发送ls 查询命令
        data = self.client.recv(10240)
        print(data.decode())        # 打印接收结果

    def put(self, msg):
        '''
        发送文件到FTP
        :param msg:
        :return:
        '''
        if os.path.isfile(msg[1]):     # 判断文件是否存在
            self.client.send(('put|' + msg[1]).encode())  # 发送PUT命令
            # user_path = self.client.recv(10240).decode()    # 接收PUT路径
            data = self.client.recv(10240).decode()
            print("数据将存放至： {}".format(data))
            size = os.path.getsize(msg[1])
            self.client.send(str(size).encode())  # 发送文件大小
            data = self.client.recv(10240)
            print(data.decode())
            f = open(msg[1], 'rb')
            print('发送数据中....')
            self.client.sendall(f.read())       # 发送文件
            data = self.client.recv(10240).decode()
            print(data)
        else:
            print('%s文件未找到！' % msg[1])

    def get(self, msg):
        '''
        从服务器帐号HOME目录获取文件
        :param msg: get 文件名 获取到本地目录
        :return:
        '''
        get_file = os.path.basename(msg[1])
        get_to_file = os.path.isdir(msg[2])
        if get_to_file:
            self.client.send(('get|' + msg[1] + '|' + msg[2]).encode())  # 发送get命令
            size = self.client.recv(10240).decode().split('|')

            if size[0] != 'True':
                print("需要get的文件不存在")
            else:
                print("数据将存放至：{}, 文件大小为：{}".format(msg[2], size[1]))
                self.client.send('ready'.encode())
                print('数据接收中....')
                file = self.client.recv(10240)  # 接收文件
                with open(os.path.join(msg[2], get_file), 'wb') as f:
                    f.write(file)

                f_size = os.path.getsize(os.path.join(msg[2], get_file))
                if f_size == int(size[1]):
                    print('数据接收完成')
        else:
            print('get的目标文件不存在')
