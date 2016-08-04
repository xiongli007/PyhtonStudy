#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import getpass      ###输入密码时不在屏幕上显示


###初始化帐号信息文件
###入参：无
###返回值：无
###作用：全部帐号信息输入失败次数初始化为 0
def Initialization():
    with open('UserMsg.txt', 'r') as r:        ###读模式打开帐号信息文件
        lines = r.readlines()
    with open('UserMsg.txt', 'w') as w:        ###写模式打开帐号信息文件
        for l in lines:
            w.write(l.replace(l[-3], '0'))  ###将倒数第三位（ “/n"算一位）替换为0


###检查帐号是否加锁
###入参：帐号信息
###返回值：加锁-->Y,未加锁-->N
def CheckLock(username):
    with open('lock.txt', 'r') as lock:                    ##读加锁帐号文件信息
        rt = 'N'                                        ###初始化为N
        for i in lock:                                 ##循环读出的加锁信息
            if i.split() == username.split():           ##切片，踢掉换行符，进行内容比较，如果相等，rt赋值为Y
                rt ='Y'                                 ##如果相等，rt赋值为Y，不相等，
                break                                   ##退出循环
    return rt                                       ##返回rt值

###检查帐号/密码是否正确
###入参：帐号信息，密码
###返回值：帐号/密码正确-->Y,帐号/密码不正确-->N
def CheckUser(username,password):
    with open('UserMsg.txt', 'r')  as  UserPass:         ##读帐号密码文件信息
        for i in UserPass:                                ##循环读帐号密码文件信息
            a = i.split('|')                              ##用分隔符为|进行切片，切片内容传给列表
            user = a[0]                                    ##取用户数据
            userpass = a[1]                                 ##取密码数据
            if username == user and password == userpass:   ##将入参与文件的帐号、密码进行等值判断
                rt1 = 'Y'                                   ##如果相等，赋值为Y
                break                                       ##退出循环
            elif username == user and password != userpass:
                rt1 = 'N'                                    ##如果帐号相等，密码不相等，赋值为N
                break
            else:
                rt1 = 'None'                                    ##如果都不相等，赋值为None
    return rt1                                               ##返回rt1值

###锁定帐号
###入参：帐号信息
###返回值：无
def LockUser(username):
    with open("lock.txt",'a') as f:
        f.write('%s\n' %username)

###错误次数加1
###入参：帐号信息
###返回值：无
def ErrorCount(username):
    with open('UserMsg.txt', 'r') as r:                 ###读模式打开帐号信息文件
        lines = r.readlines()                               ###读取所有数据
    with open('UserMsg.txt', 'w') as w:                 ###写模式打开帐号信息文件
        for l in lines:                                    ###逐行读取
            a = l.split('|')                                ###以‘|’切片
            if a[0] == username.split()[0]:                 ###取第1列数据进行相等判断，如果相等，则替换
                w.write(l.replace(l[-3], str(int(l[-3]) + 1)))  ###将倒数第三位（ “/n"算一位）错误次数加1
            else:
                w.write(l)                                   ###不相等则将原数据写回。


###读取错误数据
###入参：帐号信息
###返回值：错误数据
def ReadError(username):
    with open('UserMsg.txt', 'r') as r:
        lines = r.readlines()
        for l in lines:
            a = l.split('|')
            if a[0] ==  username.split()[0]:
                count = a[2]
    return count


###检查帐号错误次数
###入参：帐号信息
###返回值：帐号/密码正确-->Y,帐号/密码不正确-->N
def CheckErrorCount(username):
    ErrorCount(username)                                            ##该帐号信息锁定次数加1
    count = ReadError(username)                                     ##读取该帐号错误次数
    if count>='3':
        print("帐号或密码输入错误次数已达3次，帐号被锁定！")    ##如果大于等于3次，打印帐号锁定提示
        LockUser(username)                                          ##调用锁定帐号函数
    else:
        print("帐号或密码输入错误,请重新输入！")



if __name__== '__main__':
    msg = '''
        ***********************************
        欢迎进入模拟登陆
        ***********************************
        '''
    print(msg)  ##打印欢迎信息
    Initialization()  ##锁定帐号初始化
    while True:
        username = input("请输入登陆账号：")  ##打印登陆提示
        password = getpass.getpass("请输入密码: ")      ##因getpass在pycharm 有BUG,为便于测试，用input替换
        #password = input("请输入密码:")  ##测试时使用，替换getpass
        lock = CheckLock(username)  ##检查录入帐号是否锁定，返回值 Y ：已锁定；N:未锁定

        if lock == 'Y':
            print("该帐号已锁定！请联系管理员处理，谢谢！")  ###如果被锁，打印提示信息
        else:
            UserPass = CheckUser(username, password)  ###如果未被锁，检查用户名和密码录入是否正确定
            if UserPass == 'Y':
                print("登陆成功！")  ###用户名和密码录入正确，打印成功信息
                break
            elif UserPass == 'N':
                CheckErrorCount(username)  ###密码录入不正确，校验尝试次数
            else:
                print("帐号或密码输入错误,请重新输入！")  ###用户名不正确，打印请重新输入
