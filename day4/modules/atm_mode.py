#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import json
import os, sys, time, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conf import setting
from modules import login_in
from modules import atm_user
from modules import manager
from modules import shopping_mall


def qt():
    quit('退出ATM机程序！')


def diff_date(dict):
    '''
    日期差
    :param dict: 用户数据
    :return: diff_days 差异天数, bill_date 最后帐期
    '''
    date = '0'
    bill_date = ''
    struct_time = time.localtime()
    for j in dict['debt'].keys():
        if not j:
            pass
        else:
            date1 = time.strftime('%j', time.strptime(j, '%Y-%m-%d'))
            if date1 > date:
                date = date1
                bill_date = j
    date2 = time.strftime('%j', struct_time)
    diff_days = int(date2) - int(date)      # 当前时间与最后帐期差

    return diff_days, bill_date


def get_dir_file(path):
    '''
    检查目录下是否存在该文件
    :param path: 目录
    :param file_name: 检查文件
    :return: flag True：有该文件；False：无该文件；
    '''
    file_list = []
    for home, dirs, files in os.walk(path):
        for i in files:
            file_list.append(i)
    return file_list


def make_bill():
    file_list = get_dir_file(setting.PATH_CLIENT)
    for i in file_list:
        user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[i], 'r'))
        struct_time = time.localtime()
        diff_days, last_date = diff_date(user_dict)

        # 根据日期差创建账期
        if diff_days > 0 and last_date:   # 日期差大于0，说明当月未生成帐期数据 ;
            last_date_strp = time.strptime(last_date, '%Y-%m-%d')
            for j in range(math.ceil(diff_days/30)):
                curr_date = '%d-%d-%d' % (last_date_strp.tm_year, last_date_strp.tm_mon + 1 + j, int(user_dict['repay_date']))
                user_dict['debt'].setdefault(curr_date, [0, 0])
            user_dict['balance'] = user_dict['credit']
            json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[i], 'w'))
        elif not last_date:              # 无账单数据
            last_date_strp = struct_time
            for j in range(math.ceil(diff_days/30)):
                curr_date = '%d-%d-%d' % (last_date_strp.tm_year, last_date_strp.tm_mon, int(user_dict['repay_date']))
                user_dict['debt'].setdefault(curr_date, [0, 0])
            user_dict['balance'] = user_dict['credit']
            json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[i], 'w'))


def run():
    while True:
        msg = '欢迎进入ATM机程序'.center(50, '*')
        print(msg)
        make_bill()
        msg1 = '''
        请选择功能模块：
        【1】购物商城
        【2】ATM
        【3】后台管理
        【4】退出系统'''
        print(msg1)
        msg_dict = {
            '1': shopping_mall.main,
            '2': atm_user.atm_user,
            '3': manager.manager_run,
            '4': qt,
        }
        inp = input('请选择您要进行的操作序列:\n>>').strip()
        if inp in msg_dict:
            msg_dict[inp]()
        else:
            print('输入非法字符，请输入【1-4】功能代码！')


