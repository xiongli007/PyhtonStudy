#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf import setting
from modules import login_in
from modules import log

QUIT = True
log =log.log(setting.ATM_LOG)

def add_user():
    '''
    增加用户
    :return:
    '''
    flag = True
    creat_name = ''
    creat_path = ''
    power_info = input('''请选择创建用户类型 【0】普通用户；【1】管理用户 ;\n>>''')
    if not (power_info == '1' or power_info == '0'):
        print('输入非法字符！')
    else:
        if power_info == '1':
            while flag:
                creat_name = input('请自定义需要添加的管理员帐号：').strip()
                rq = login_in.chack_dir_file(setting.PATH_ADMIN, creat_name)
                if rq:
                    print('输入的帐号已存在，请重新输入！')
                else:
                    flag = rq
            creat_path = os.path.join(setting.PATH_ADMIN, creat_name)
        elif power_info == '0':
            while flag:
                # 帐号重复性检查
                creat_name = creat_username()
                rq = login_in.chack_dir_file(setting.PATH_USER, creat_name)
                flag = rq
            print('系统生成帐号为：%s' % creat_name)
            creat_path = os.path.join(setting.PATH_CLIENT, creat_name)
        info = input('''设置用户信息：
        依次输入：密码/权限(0：普通用户；1：管理员用户)/信用卡最大透支额度/本月可用额度/还款日期/储蓄金额
        格式:\033[33;0m 123/0/10000/10000/15/0/\033[0m\n
        >>''').strip()
        info_list = info.split('/')
        pass_word = login_in.md5(info_list[0])   # 密码
        power = info_list[1]            # 权限
        credit = int(info_list[2])           # 最大透支额度
        balance = int(info_list[3])          # 本月可用额度
        repay_date = info_list[4]            # 还款日期
        saving = int(info_list[5])           # 储蓄金额

        base_info = {
            'username': creat_name,     # 用户
            'password': pass_word,      # 密码
            'power': power,             # 权限
            'credit': credit,           # 最大透支额度
            'balance': balance,         # 本月可用额度
            'saving': saving,           # 储蓄金额
            'repay_date': repay_date,   # 还款日期
            'type': 'Y',    # 用户有效 ，Y 有效；N 无效；
            'debt': {},     # 欠费记录
        }
        os.mkdir(creat_path)
        json.dump(base_info, open(os.path.join(creat_path, creat_name), 'w'))
        print('帐号为：%s 创建完毕！' % creat_name)
        log.info('【%s】-->帐号为：%s 创建完毕！' % (login_in.USER_STATUS['username'], creat_name))


def freeze_user():
    '''
    冻结用户
    :param:user_name 帐号
    :return:
    '''
    file_dict = login_in.get_file_dir(setting.PATH_USER)
    user_name = input('请输入要冻结的用户: ').strip()
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        if user_dict['type'] == 'N':
            print('帐号:%s已冻结，不用处理！')
        else:
            user_dict['type'] = 'N'
            json.dump(user_dict, open(file_dict[user_name], 'w'))
            print('帐号:%s已冻结！' % user_name)
            log.info('【%s】-->帐号:%s已冻结！' % (login_in.USER_STATUS['username'], user_name))
    else:
        print('未查到%s帐号！' % user_name)


def creat_username():
    '''
    生成10位数帐号
    :return: 帐号
    '''
    import random
    check_code = ''
    for i in range(10):
        if i == 0:
            temp = 6
        elif 0 < i < 4:
            temp = random.randrange(0, 2)
        else:
            temp = random.randint(0, 9)
        check_code += str(temp)
    return check_code


def chg_credit():
    '''
    调整用户最大透支额度
    :return: 成功为True, 失败为False
    '''
    user_name = input('请输入要调整额度的用户: ').strip()
    file_dict = login_in.get_file_dir(setting.PATH_USER)
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        print('帐号:%s目前最大透支额度：%s' % (user_name, user_dict['credit']))
        inp_info = input('请输入要调整的最大透支额度：').strip()
        user_dict['credit'] = inp_info
        json.dump(user_dict, open(file_dict[user_name], 'w'))
        print('帐号:%s已调整最大透支额度！' % user_name)
        log.info('【%s】-->帐号:%s已调整最大透支额度！' % (login_in.USER_STATUS['username'], user_name))
    else:
        print('未查到%s帐号！' % user_name)


def unlock():
    '''
    解锁用户
    :return: 成功返回True,否则为False
    '''
    file_dict = login_in.get_file_dir(setting.PATH_USER)
    user_name = input('请输入要解锁的用户: ').strip()
    if user_name in file_dict.keys():
        user_dict = json.load(open(file_dict[user_name], 'r'))
        if user_dict['type'] == 'Y':
            print('帐号:%s未冻结，不用处理！')
        else:
            user_dict['type'] = 'Y'
            json.dump(user_dict, open(file_dict[user_name], 'w'))
            print('帐号:%s已解锁！' % user_name)
            log.info('【%s】-->帐号:%s已解锁！' % (login_in.USER_STATUS['username'], user_name))
    else:
        print('未查到%s帐号！' % user_name)


def qt():
    global QUIT
    QUIT = False


def manager_run():
    '''
    主程序,主要用于系统管理员登录后的操作
    :return:
    '''
    username, user_flag, admin_type = login_in.login_in()
    if user_flag:
        if admin_type:
            while QUIT:
                if admin_type and user_flag:
                    show = '''\n已进入后台管理模块：
                    【1】新增帐户
                    【2】调整最大透支额度
                    【3】冻结帐户
                    【4】解锁帐户
                    【5】修改密码
                    【6】退出后台管理'''
                    print(show)
                    inp = input('请选择您要进行的操作序列:\n>>').strip()
                    show_dist = {
                        '1': add_user,
                        '2': chg_credit,
                        '3': freeze_user,
                        '4': unlock,
                        '5': login_in.modify_password_adm,
                        '6': qt,
                    }
                    if inp in show_dist:
                        show_dist[inp]()
                    else:
                        print('输入非法字符！')
        else:
            print('不是管理员帐号，不能进入此模块！')
            input('按回车键继续')
    else:
        input('按回车键继续')
