#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import socket, os, json, hashlib, sys
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting


class Ftp_client(object):
    def __init__(self):
        self.login_flag = False
        self.client = socket.socket()

    def __del__(self):
        self.client.close()

    def help(self):
        msg = '''
        ls
        pwd
        cd
        get filename
        put filename
        '''
        print(msg)

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def login_in(self):
        '''
        登录功能
        :return:
        '''
        err_cont = 0
        while not self.login_flag:
            print('请输入登录名：')
            user_name = input('>>').strip()
            print('请输入登录密码：')
            pass_word = input('>>').strip()
            if len(user_name) == 0 or len(pass_word) == 0: continue
            pass_word_md5 = hashlib.md5(bytes('xx', encoding='utf8'))
            pass_word_md5.update(bytes(pass_word, encoding='utf8'))
            msg = {
                "action": "login_in",
                "username": user_name,
                "pass_word": pass_word_md5.hexdigest()
            }
            print(msg)
            self.client.send(json.dumps(msg).encode())
            data = self.client.recv(1024)
            if data.decode('utf-8') == '1':
                print('帐号：' + user_name + ' 登录成功!')
                self.login_flag = True
            else:
                print('帐号：' + user_name + ' 输入的帐号或密码错误!')
                err_cont += err_cont
            if err_cont > 3:
                break

    def ls(self, msg):
        '''
        查询文件
        :param msg:
        :return:
        '''
        self.client.send('ls|0'.encode())    # 发送ls 查询命令
        data = self.client.recv(10240)
        print(data.decode())        # 打印接收结果

    def cmd_put(self, *args):
        '''
        发送文件到FTP
        :param msg:
        :return:
        '''
        msg = args[0].split()
        if len(args[0].split()) > 1:
            filename = msg[1]
            if os.path.isfile(filename):     # 判断文件是否存在
                size = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename": filename,
                    "size": size,
                }
                self.client.send(json.dumps(msg_dic).encode())  # 发送文件大小
                data = self.client.recv(1024).decode()    # 服务器进行配额检测
                # 200 正常 400 配额不足
                if data == '200':
                    print(data.decode())
                f = open(msg[1], 'rb')
                print('发送数据中....')
                for line in f:
                    self.client.send(line)       # 发送文件
                print('数据发送完成！')
                f.close()
                data = self.client.recv(10240).decode()
                print(data)
            else:
                print('%s文件未找到！' % msg[1])
        else:
            print("参数有误！")

    def cmd_get(self, msg):
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

    def run(self):
        self.connect(setting.SERVER_IP, setting.SERVER_PORT)
        # self.login_in()
        self.login_flag = True
        if self.login_flag:
            print('请输入操作命令：')
            while True:
                cmd = input(">>").strip()
                if len(cmd) == 0:
                    continue
                cmd_str = cmd.split()[0]
                if hasattr(self, "cmd_%s" % cmd_str):          # 通过反射找到输入的命令方法
                    func = getattr(self, "cmd_%s" % cmd_str)   # 得到方法名
                    func(cmd)
                else:
                    self.help()
