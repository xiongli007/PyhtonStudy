#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import socket, os, json, hashlib, sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting


def progressbar(x, width=100):
    pointer = int(width * (x / 100.0))
    sys.stdout.write('\r%d%% [%s]' % (int(x), '#' * pointer + ' ' * (width - pointer)))
    sys.stdout.flush()
    if x == 100: print()

if __name__ == '__main__':
    for a in range(0, 101):
        progressbar(a)
        time.sleep(0.1)


class Ftp_client(object):
    def __init__(self):
        self.login_flag = False
        self.client = socket.socket()

    def __del__(self):
        self.client.close()

    def help(self):
        msg = '''请使用以下命令：
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
            self.client.send(json.dumps(msg).encode())
            data = self.client.recv(1024)
            if data.decode('utf-8') == '200':
                print('帐号：' + user_name + ' 登录成功!')
                self.login_flag = True
            else:
                print('帐号：' + user_name + ' 输入的帐号或密码错误!')
                err_cont += err_cont
            if err_cont > 3:
                break

    def cmd_ls(self, msg):
        '''
        查询文件
        :param msg:
        :return:
        '''
        msg_dic = {
            "action": "ls",
        }
        self.client.send(json.dumps(msg_dic).encode())    # 发送ls 查询命令
        msg_dic1 = json.loads(str(self.client.recv(1024).decode()))
        print(msg_dic1)
        if msg_dic1["size"] == 0:
            print("查无文件")
        else:
            self.client.send(b'200')
            received_size = 0
            cmd_res = b''
            while received_size != msg_dic1["size"]:  # 没收完,继续收
                data = self.client.recv(1024)
                received_size += len(data)
                cmd_res += data
            print(cmd_res.decode(msg_dic1["de_code"]))        # 打印接收结果

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
                    m = hashlib.md5()  # 生成md5文件完整码
                    f = open(msg[1], 'rb')
                    send_size = 0
                    for line in f:
                        self.client.send(line)
                        send_size += len(line)
                        progressbar(send_size/size*100)   # 调用进度条函数
                        m.update(line)
                    f.close()
                    data = self.client.recv(1024).decode()
                    print(data)
                    # 校验文件MD5值
                    md5sum = m.hexdigest()
                    self.client.send(md5sum.encode())
                    rec = int(self.client.recv(1024))
                    if rec == 200:
                        print('文件完整性校验成功！')
                    else:
                        print('文件完整性校验不成功，请检查！')
                else:
                    print('帐号磁盘配额不足！')
            else:
                print('%s文件未找到！' % msg[1])
        else:
            print("参数有误！")

    def cmd_get(self, *args):
        '''
        从服务器帐号HOME目录获取文件
        :param msg: get 文件名 获取到本地目录
        :return:
        '''

        msg = args[0].split()
        get_file = os.path.basename(msg[1])
        if len(msg) > 2:  # 判断是否存在重命名
            get_to_file = msg[2]
        else:
            get_to_file = get_file

        msg_dic = {
            "action": "get",
            "filename": get_file,
            "get_to_file": get_to_file,
            "size": 0,
            "md5": "",
        }
        self.client.send(json.dumps(msg_dic).encode())  # 发送get命令

        rec_dic = json.loads(self.client.recv(1024).decode())
        if not rec_dic["is_file"]:
            print("需要get的文件不存在")
        else:
            print("文件名为：{}, 文件大小为：{}".format(get_to_file, rec_dic["size"]))
            self.client.send(b'200')
            print('数据接收中....')
            file_size = 0
            m = hashlib.md5()
            with open(get_to_file, 'wb') as f:
                while file_size < rec_dic["size"]:
                    file = self.client.recv(1024)  # 接收文件
                    file_size += len(file)
                    f.write(file)
                    m.update(file)
                    progressbar(file_size/rec_dic["size"]*100)  # 调用进度条函数
            f_size = os.path.getsize(get_to_file)
            md5sum = m.hexdigest()
            if f_size == rec_dic["size"]:
                print('数据接收完成')
                self.client.send(b'200')
                data = self.client.recv(1024).decode()
                if md5sum == data:
                    print('文件完整性校验成功!')
                else:
                    print('文件完整性校验不成功，请检查！')
            else:
                print('数据接未收完成')


    def cmd_pwd(self, *args):
        msg_dic = {
            "action": "pwd",
        }
        self.client.send(json.dumps(msg_dic).encode())
        rec = self.client.recv(1024).decode()
        print(rec)

    def cmd_cd(self, *args):
        if args[0] == 'cd':
            path = 'HOME'
        else:
            path = args[0].split()[1]

        msg_dic = {
            "action": "cd",
            "path": path,
        }
        self.client.send(json.dumps(msg_dic).encode())
        rec_dic = json.loads(self.client.recv(1024).decode())
        if rec_dic["run_code"] != 200:
            print('输入的路径有误！')
        else:
            print('当前路径为：{}'.format(rec_dic["run_path"]))

    def cmd_quit(self, *args):
        msg_dic = {
            "action": "quit",
        }
        self.client.send(json.dumps(msg_dic).encode())
        quit('bye bye!')
        self.__del__()

    def run(self):
        self.connect(setting.SERVER_IP, setting.SERVER_PORT)
        self.login_in()
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
