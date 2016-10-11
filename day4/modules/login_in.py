#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import os, sys
import hashlib
import json
import time, datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf import setting
from modules import log


INPUT = {}
USER_STATUS = {'power': None, 'username': None, 'type': False}  # type 用户登陆状态，power：权限；username： 用户
log =log.log(setting.ATM_LOG)


def check_lock(user_name):
    '''
    检查帐号是否加锁
    :param user_name:帐号
    :return:null
    '''
    file_dict = get_file_dir(setting.PATH_USER)
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        if user_dict['type'] == 'N':
            return True
        else:
            return False
    else:
        return False


def modify_password(user_name):
    '''
    修改密码
    :return:
    '''
    file_dict = get_file_dir(setting.PATH_USER)
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        pas_word1 = input('请输入需要修改的密码：').strip()
        pas_word2 = input('请再次输入需要修改的密码：').strip()
        if pas_word1 == pas_word2:
            pasword_md5 = md5(pas_word2)
            user_dict['password'] = pasword_md5
            json.dump(user_dict, open(file_dict[user_name], 'w'))
            print('帐号:%s密码已修改！' % user_name)
            log.info('【%s】-->帐号:%s密码已修改！' % (USER_STATUS['username'], user_name))
        else:
            print('两次输入的密码不一致！')
    else:
        print('未查到%s帐号！' % user_name)
    input('按回车键继续\n')


def modify_password1():
    modify_password(USER_STATUS['username'])


def modify_password_adm():
    username = input('输入需修改帐号：')
    modify_password(username)


def lock_user(user_name):
    '''
    锁定帐号
    :param user_name:
    :return:
    '''
    file_dict = get_file_dir(setting.PATH_USER)
    user_dict = json.load(open(file_dict[user_name], 'r'))
    user_dict['type'] = 'N'
    json.dump(user_dict, open(file_dict[user_name], 'w'))
    print('帐号:%s已冻结！' % user_name)
    log.info('帐号:%s已冻结！' % user_name)
    return True


def check_error_count(user_name):
    '''
    输入错误检查
    :param user_name:帐号
    :return:null
    '''
    global INPUT
    if INPUT[user_name] >= 2:
        print("帐号或密码输入错误次数已达3次，帐号被锁定！")  # #如果大于等于3次，打印帐号锁定提示
        q = lock_user(user_name)  # #调用锁定帐号函数
        return True
    else:
        return False  # #如果帐号相等，密码不相等，赋值为N


def md5(password):
    '''
    md5加密
    :param password: 明文密码
    :return: MD5密码
    '''
    password_md5 = hashlib.md5(bytes('ooxx', encoding='utf-8'))
    password_md5.update(bytes(password, encoding='utf-8'))
    return password_md5.hexdigest()


def get_file_dir(path):
    '''
    得到文件目录
    :param path: 目录
    :return: file_dict 文件字典
    '''
    file_dict = {}
    for home, dirs, files in os.walk(path):
        for f in files:
            file_dict.setdefault(f, os.path.join(home, f))
    return file_dict


def chack_dir_file(path, file_name):
    '''
    检查目录下是否存在该文件
    :param path: 目录
    :param file_name: 检查文件
    :return: flag True：有该文件；False：无该文件；
    '''
    file_list = []
    flag = False
    for home, dirs, files in os.walk(path):
        for i in files:
            file_list.append(i)
    if file_name in file_list:
        flag = True
    return flag


def select_user_msg(user_name):
    '''
    查询用户信息
    :param user_name:
    :return:
    '''
    file_dict = get_file_dir(setting.PATH_USER)
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        print('帐号：%s 的信息如下：' % user_dict['username'])
        print('权限 (0：普通用户；1：管理员用户)：%s' % user_dict['power'])
        print('最大透支额度 ：%s' % user_dict['credit'])
        print('本月可用额度：%s' % user_dict['balance'])
        print('储蓄金额：%s' % user_dict['saving'])
        print('还款日期：%s' % user_dict['repay_date'])
        print('用户有效（Y 有效；N 无效；）：%s' % user_dict['type'])
        print('欠费记录：%s' % user_dict['debt'])

    else:
        print('未查到%s帐号！' % user_name)


def check_user(user_name, pass_word):  # ##检查帐号/密码是否正确
    '''
    检查输入用户/密码
    :param user_name:帐号
    :param pass_word:密码
    :return: rt1
    '''
    global INPUT
    pass_word_md5 = md5(pass_word)  # 加密
    if chack_dir_file(setting.PATH_USER, user_name):
        # 如果有目录，帐号存在
        file_dict = get_file_dir(setting.PATH_USER)
        user_dict = json.load(open(file_dict[user_name], 'r'))
        if user_dict['password'] == pass_word_md5:
            rt1 = 'Y'
            power = user_dict['power']
        else:
            rt1 = 'N'
            power = None
    else:
        rt1 = 'None'
        power = None
    return rt1, power


def login_in():
    '''
    用户登录运行程序
    :return:username, flag, admin_type
    '''
    global USER_STATUS
    flag = False
    admin_type = False
    username = input("请输入登陆账号：")  # 打印登陆提示
    # password = getpass.getpass("请输入密码: ")      # 因getpass在pycharm 有BUG,为便于测试，用input替换
    password = input("请输入密码:")  # 测试时使用，替换getpass
    INPUT.setdefault(username, 0)
    if check_lock(username):  # 检查录入帐号是否锁定
        exit("该帐号已锁定！请联系管理员处理，谢谢！")
    else:
        user_pass, power = check_user(username, password)  # 如果未被锁，检查用户名和密码录入是否正确定
        if user_pass == 'Y':
            print("帐号：%s登陆成功！" % username)  # 用户名和密码录入正确，返回用户信息
            USER_STATUS['username'] = username
            USER_STATUS['power'] = power
            USER_STATUS['type'] = True
            if power == '1':
                admin_type = True
                flag = True
            else:
                flag = True
                admin_type = False
                log.info("【%s】-->帐号：%s登陆成功！" % (username, username))
            return username, flag, admin_type
        elif user_pass == 'N':
            check_error_count(username)
            INPUT[username] += 1
            print("帐号或密码输入错误,请重新输入！")
            log.info("【%s】-->帐号或密码输入错误,请重新输入！" % username)
            return username, flag, admin_type  # 密码录入不正确，校验尝试次数
        elif user_pass == 'q':
            return username, flag, admin_type
        elif user_pass == 'None':
            print('无此用户，请登录admin帐号添加!'.center(30, '*'))
            log.info("【%s】-->无此用户，请登录admin帐号添加!" % username)
            print("帐号未注册,Bye Bye ！")  # ##用户名不正确，打印退出
            return username, flag, admin_type

