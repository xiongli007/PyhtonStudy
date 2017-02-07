#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import socket, socketserver, pickle, sys, os, subprocess, hashlib, json, platform
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting
from modules import log
log = log.log(setting.PATH_LOGFILE)


class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
         while True:
            try:
                data = self.request.recv(1024).strip().decode()
                cmd_dic = json.loads(str(data))
                action = cmd_dic["action"]
                print("【{}】收到消息:{}".format(self.client_address[0], action))
                log.info("【{}】收到消息:{}".format(self.client_address[0], action))

                if hasattr(self, action):
                    function = getattr(self, action)
                    function(cmd_dic)
                    if action == 'quit': break
            except ConnectionResetError as e:
                print("error", e)
                log.info("【{}】error {}".format(self.client_address[0], e))
                break

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
                self.name = user_name
                self.path = login_dict[user_name]['user_path']
                self.home = login_dict[user_name]['home_path']
                rs = '200'
                log.info("【{}】帐号：{} 登录成功!".format(self.client_address[0], user_name))
            else:
                rs = '400'
                log.info("【{}】帐号：{} 登录失败!".format(self.client_address[0], user_name))
        else:
            rs = '400'
            log.info("【{}】帐号：{} 登录失败!".format(self.client_address[0], user_name))
        self.request.send(rs.encode())

    def quit(self, *args):
        self.login_type = False
        log.info("【{}】帐号：{} 退出登录!".format(self.client_address[0], self.user_name))

    def ls(self, msg):
        '''
        查询不同用户HOME目录下的文件
        :param msg:
        :return:
        '''
        osname = platform.system()
        cmd = ''
        de_code = ''
        if osname == 'Windows':
            cmd = 'dir'
            de_code = 'gbk'
        elif osname == 'Linux':
            cmd = 'ls -arlt'
            de_code = 'utf-8'
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, cwd=self.path)  # 查询当前目录下文件
        res_data = res.stdout.read()
        msg_dic = {
            "size": len(res_data),
            "de_code": de_code
        }
        self.request.send(json.dumps(msg_dic).encode())
        self.request.recv(1024)

        self.request.send(res_data)
        log.info("【{}】帐号：{} ls 查询".format(self.client_address[0], self.name))

    def put(self, msg):
        '''
        客户端的PUT命令，即服务器端获取数据
        :param msg:
        :return:
        '''
        m = hashlib.md5()
        USE_DICT = json.load(open(setting.PATH_USE, 'r'))
        # 配额检查
        if msg["size"] + os.stat(self.path).st_size > USE_DICT[self.user_name]["user_size"]:
            self.request.send(b'400')   # 用户配额不足
            log.info("【{}】帐号:{}  用户配额不足".format(self.client_address[0], self.name))
        else:
            self.request.send(b'200')  # 用户配额足
            file_size = 0
            with open(os.path.join(self.path, msg["filename"]), 'wb') as f:
                while file_size < msg["size"]:
                    file = self.request.recv(1024)           # 接收文件
                    f.write(file)
                    m.update(file)
                    file_size += len(file)
            md5sum = m.hexdigest()
            f_size = os.path.getsize(os.path.join(self.path, msg["filename"]))
            if f_size == msg["size"]:    # 校验是否下载完成
                self.request.send('服务端接受完毕'.encode())
                data = self.request.recv(1024).decode()
                if data == md5sum:
                    self.request.send(b'200')
                else:
                    self.request.send(b'400')
                log.info("【{}】帐号:{}  接受{}文件完成".format(self.client_address[0], self.name, msg["filename"]))

    def get(self, msg):
        '''
        客户端的get命令，即服务器端发送数据
        :param msg:
        :return:
        '''
        get_file = os.path.basename(msg["filename"])
        file_path = os.path.join(self.path, get_file)
        if not os.path.isfile(file_path):    # 参数不是文件

            msg_dic = {
                "filename": get_file,
                "is_file": False,
                "size": 0,
            }
            self.request.send(json.dumps(msg_dic).encode())
            log.info("【{}】帐号:{}  get {}不是文件".format(self.client_address[0], self.name, file_path))
        else:
            size = os.stat(file_path).st_size
            msg_dic = {
                "filename": get_file,
                "is_file": True,
                "size": size,
            }
            self.request.send(json.dumps(msg_dic).encode())  # 发送成功标示、文件大小
            data = self.request.recv(1024).decode()
            if data == '200':
                m = hashlib.md5()
                with open(file_path, 'rb') as f:
                    send_data = f.read()
                    m.update(send_data)
                    self.request.send(send_data)
                md5sum = m.hexdigest()
                self.request.recv(1024)  # 防止粘包
                self.request.send(md5sum.encode())
                log.info("【{}】帐号:{}  get {}文件发送完成".format(self.client_address[0], self.name, file_path))
            else:
                send_data = 0
                self.request.send(send_data)
                log.info("【{}】帐号:{}  get {}文件不存在".format(self.client_address[0], self.name, file_path))

    def pwd(self, *args):
        pwd_path = self.path
        self.request.send(pwd_path.encode())
        log.info("【{}】帐号:{}  执行pwd命令".format(self.client_address[0], self.name))

    def cd(self, msg):
        rec_path = msg["path"]
        send_code = 200
        if rec_path == 'HOME':
            self.path = self.home
            log.info("【{}】帐号:{}  执行cd命令，返回帐号目录".format(self.client_address[0], self.name))
            print(self.path)
        elif rec_path == '..':                  # 如果是'..' ，返回父目录
            self.path = os.path.dirname(os.path.abspath(self.path))
            log.info("【{}】帐号:{}  执行cd命令，返回父目录".format(self.client_address[0], self.name))
        else:
            print(os.path.join(self.path, rec_path))
            print(os.path.isabs(os.path.join(self.path, rec_path)))
            if os.path.isabs(os.path.join(self.path, rec_path)):    # 判断是否是正确目录
                self.path = os.path.join(self.path, rec_path)
                log.info("【{}】帐号:{}  执行cd命令，到{}目录".format(self.client_address[0], self.name, self.path))
            else:
                send_code = 400
                log.info("【{}】帐号:{}  执行cd命令，未找到目录".format(self.client_address[0], self.name))
        send_msg = {
            "run_code": send_code,
            "run_path": self.path,
        }
        self.request.send(json.dumps(send_msg).encode())
        log.info("【{}】帐号:{}  执行cd命令".format(self.client_address[0], self.name))


# a ={'x1': {'name': 'xx', 'password': '123', 'path': '/x1'}, 'ftp': {'name': 'ftp', 'password': '123', 'path': '/ftp'}}
# pickle.dump(a, open(os.path.join(setting.PATH_DB, 'login.pkl'), 'wb'))
