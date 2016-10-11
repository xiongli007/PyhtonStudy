#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import getpass      ###输入密码时不在屏幕上显示
INPUT ={}
# ##检查帐号是否加锁


def CheckLock(username):
    with open('lock.txt', 'r') as lock:                    ##读加锁帐号文件信息
        for i in lock:                                 ##循环读出的加锁信息
            if i.split() == username.split():           ##切片，踢掉换行符，进行内容比较，如果相等 返回True
                return True
    return False                                       ##否则返回False


def CheckErrorCount(username):
    if INPUT[username] >= 3:
        print("帐号或密码输入错误次数已达3次，帐号被锁定！")  ##如果大于等于3次，打印帐号锁定提示
        q = LockUser(username)  ##调用锁定帐号函数
        return True
    else:
        return False  ##如果帐号相等，密码不相等，赋值为N

###检查帐号/密码是否正确
def CheckUser(username,password):
    global INPUT
    with open('UserMsg.txt', 'r')  as  UserPass:         ##读帐号密码文件信息
        for i in UserPass:                                ##循环读帐号密码文件信息
            a = i.split('|')                              ##用分隔符为|进行切片，切片内容传给列表
            user = a[0]                                    ##取用户数据
            userpass = a[1]                                 ##取密码数据
            if username == user and password == userpass:   ##将入参与文件的帐号、密码进行等值判断
                rt1 = 'Y'                                   ##如果相等，赋值为Y
                break
            elif username == user and password != userpass:
                INPUT[username]=int(INPUT[username]) + 1                     ##该帐号信息锁定次数加1
                rt1 = 'N'
                break
            elif username != user :
                rt1 = 'None'                                ##如果帐号不相等，赋值为None
        if CheckErrorCount(username):
            rt1 = 'q'
        return rt1

###锁定帐号
def LockUser(username):
    with open("lock.txt",'a') as f:
        f.write('%s\n ' %username)
    return True

if __name__== '__main__':
    msg = '''
        ***********************************
        欢迎进入模拟登陆
        ***********************************
        '''
    print(msg)  ##打印欢迎信息

    while True:
        username = input("请输入登陆账号：")  ##打印登陆提示
        # password = getpass.getpass("请输入密码: ")      ##因getpass在pycharm 有BUG,为便于测试，用input替换
        password = input("请输入密码:")  ##测试时使用，替换getpass
        INPUT.setdefault(username, 0)
        if CheckLock(username):         ##检查录入帐号是否锁定
            print("该帐号已锁定！请联系管理员处理，谢谢！")  ###如果被锁，打印提示信息
            break
        else:
            UserPass = CheckUser(username, password)  ###如果未被锁，检查用户名和密码录入是否正确定
            if UserPass == 'Y':
                print("登陆成功！")  ###用户名和密码录入正确，打印成功信息
                break
            elif UserPass == 'N':
                  print("帐号或密码输入错误,请重新输入！")
                  continue  ###密码录入不正确，校验尝试次数
            elif UserPass == 'q':
                break
            elif UserPass == 'None':
                print("帐号未注册,Bye Bye ！")  ###用户名不正确，打印退出
                break
