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
from modules import login_in

QUIT = True
log =log.log(setting.ATM_LOG)


def bill_date():
    '''
    帐单日期
    :return:curr_date 帐单日期
    '''
    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    days = time.localtime().tm_mday
    user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'r'))  # 取用户还款日期
    repay_date = int(user_dict['repay_date'])
    if days >= repay_date:
        days = repay_date
        curr_date = '%d-%d-%d' % (year, month + 1, days)
        return curr_date
    else:
        days = repay_date
        curr_date = '%d-%d-%d' % (year, month, days)
        return curr_date


def withdraw_money_base(flag):
    '''
    取款/转帐/消费基础函数
    :param flag: 处理类型
    :return: int(inp) 提取/转帐/消费的金额, succ_no 完成类型
    '''
    succ_no = False
    inp = '0'
    user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'r'))
    balance = int(user_dict['balance'])  # 可取本月额度一半
    if balance > 0:
        if flag == '消费':
            inp = input('您的账户最高可%s【%.2f】元, 请输入你要%s的金额:' % (flag, int(balance) + user_dict['saving'], flag)).strip()
        else:
            inp = input('您的账户最高可%s【%.2f】元, 请输入你要%s的金额:' % (flag, int(balance / 2) + user_dict['saving'], flag)).strip()
        if inp.isdigit():
            if flag == '消费':
                a = int(inp) * 0  # 消费类型无手续费
            else:
                a = int(inp) * 0.05
            counter_fee = float("%.2f" % a)  # 手续费 5%
            if int(inp) <= balance / 2 + user_dict['saving'] and flag != '消费':  # 输入金额小于等于可取款金额的1/2，扣减可取金额

                if int(inp) <= user_dict['saving']:
                    user_dict['saving'] -= int(inp)
                    counter_fee = 0
                elif int(inp) > user_dict['saving']:
                    user_dict['balance'] = balance - int(inp) - counter_fee - user_dict['saving']
                    user_dict['saving'] = 0

                    # 写入当前帐期欠款数据
                    curr_time = bill_date()
                    # 有帐期数据
                    if user_dict['debt'].get(curr_time):
                        user_dict['debt'][curr_time][0] -= int(inp) + counter_fee   # 提现数据写入记录

                    # 无帐期数据
                    else:
                        user_dict['debt'].setdefault(curr_time, [-(int(inp)-counter_fee), 0])
                json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'w'))
                print('%s【%d】 元，手续费：【%.2f】元,正在处理，请稍后...' % (flag, int(inp), counter_fee))
                log.info("【%s】-->%s【%d】 元，手续费：【%.2f】元" % (login_in.USER_STATUS['username'], flag, int(inp), counter_fee))
                succ_no = True

            elif int(inp) <= balance + user_dict['saving'] and flag == '消费':

                if int(inp) <= user_dict['saving']:
                    user_dict['saving'] -= int(inp)
                    counter_fee = 0
                elif int(inp) > user_dict['saving']:
                    user_dict['balance'] = balance - int(inp) - counter_fee - user_dict['saving']
                    user_dict['saving'] = 0

                    # 写入当前帐期欠款数据
                    curr_time = bill_date()
                    # 有帐期数据
                    if user_dict['debt'].get(curr_time):
                        user_dict['debt'][curr_time][0] -= int(inp) - counter_fee   # 提现数据写入记录

                    # 无帐期数据
                    else:
                        user_dict['debt'].setdefault(curr_time, [-(int(inp)-counter_fee), 0])
                json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'w'))
                print('%s【%d】 元，手续费：【%.2f】元,正在处理，请稍后...' % (flag, int(inp), counter_fee))
                log.info("【%s】-->%s【%d】 元，手续费：【%.2f】元" % (login_in.USER_STATUS['username'], flag, int(inp), counter_fee))
                succ_no = True
            else:
                print('输入金额应该小于等于%.2f！' % (balance / 2))
        else:
            print('输入金额有误！')
    else:
        print('本月无可%s额度！' % flag)
        inp = 0
        succ_no = False
    return float(inp), succ_no


def withdraw_money():
    money, succ_no = withdraw_money_base('取款')
    if succ_no:
        time.sleep(1)
        print('取款成功...')
    input('按回车键继续\n')


def repay_money():
    '''还款'''
    chose = {}
    user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'r'))

    if not user_dict['debt']:  # 如果无帐单信息
        print('帐号：%s无帐单数据！' % login_in.USER_STATUS['username'])
    else:

        flag = True
        while flag:  # 遍历并做输出展示
            print('选择仍需还款的帐期：')
            print('编码 \t 帐期 \t 需还款金额')
            for num, item in enumerate(user_dict['debt']):  # 遍历并做输出展示
                bill_value = user_dict['debt'][item][0]
                pay_value = user_dict['debt'][item][1]
                if bill_value + pay_value != 0:
                    print('【%d】\t 【%s】\t 【%s】' % (num, item, float(-bill_value) - float(pay_value)))
                    chose.setdefault(num, item)
            print('【q】 \t 退出')
            inp = input('请输入选择的帐期序列:').strip()

            if inp == 'q' or inp == 'Q':
                flag = False
                break

            chose_bill_date = chose.get(int(inp))
            repay_fee = input('还款金额：\n>>').strip()
            user_dict['debt'][chose_bill_date][1] += int(repay_fee)
            curr_date = bill_date()
            if chose_bill_date == curr_date:     # 当前帐期则增加可用额度
                user_dict['balance'] += int(repay_fee)

            print('帐期：【%s】已完成还款【%s】元' % (chose_bill_date, repay_fee))
            json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'w'))
            log.info("【%s】-->帐期：【%s】已完成还款【%s】元" % (login_in.USER_STATUS['username'], chose_bill_date, repay_fee))
            input('按回车键继续')


def save_money():
    '''
    存款
    :return:
    '''
    user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'r'))
    save_fee = input('请输入存款金额：').strip()
    user_dict['saving'] += int(save_fee)
    json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'w'))
    time.sleep(1)
    print('已存入【%s】元到帐户中...' % int(save_fee))
    log.info("【%s】-->帐期：存入【%s】元到帐户中" % (login_in.USER_STATUS['username'], int(save_fee)))
    input('按回车键继续\n')


def show_bill():
    '''
    帐单展示
    :return:
    '''
    chose = {}
    struct_time = time.localtime()  # struct_time时间
    user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[login_in.USER_STATUS['username']], 'r'))
    balance = user_dict['balance']  # 可用额度
    credit = user_dict['credit']  # 最大额度额度
    repay_date = int(user_dict['repay_date'])  # 还款日期

    curr_time = bill_date()  # 取出账单日期
    if not user_dict['debt']:  # 如果无帐单信息
        print('帐号：%s无帐单数据！' % login_in.USER_STATUS['username'])

    else:
        flag = True
        while flag:  # 遍历并做输出展示
            print('编码 \t 帐期')
            for num, item in enumerate(user_dict['debt']):  # 遍历并做输出展示
                print('【%d】\t %s' % (num, item))
                chose.setdefault(num, item)
            print('【q】 \t 退出')

            inp = input('请输入选择的帐期序列:').strip()
            if inp == 'q' or inp == 'Q':
                flag = False
                break
            chose_bill_date = chose.get(int(inp))

            bill_value = user_dict['debt'][chose_bill_date][0]
            pay_value = user_dict['debt'][chose_bill_date][1]
            debt = float(-bill_value) - float(pay_value)  # 欠款金额
            # 计算延期手续费
            struct_bill_date = time.strptime(chose_bill_date, '%Y-%m-%d')
            repay_date1 = '%d-%d-%d' % (struct_bill_date.tm_year, struct_bill_date.tm_mon, repay_date)
            chose_bill = '%d-%d' % (struct_bill_date.tm_year, struct_bill_date.tm_mon)
            date1 = time.strftime('%j', time.strptime(repay_date1, '%Y-%m-%d'))  # 还款日
            date2 = time.strftime('%j', struct_time)  # 当前时间
            diff_days = int(date2) - int(date1)  # 差

            cost = (-bill_value) * 0.0005 * int(diff_days) if int(diff_days) > 0 else 0
            cost = ("%.2f" % cost)
            if struct_time.tm_mday >= repay_date and chose_bill_date == curr_time:
                print('\n 个人信用卡未出帐账单:\n{}'.format('*' * 60))
            else:
                print('\n 个人信用卡账单:\n{}'.format('*' * 60))
            print('''
                账号:\t\t【{}】
                账期:\t\t【{}】
                账单金额:\t\t【{}】
                已还金额:\t\t【{}】
                欠款金额:\t\t【{}】
                到期还款日:\t\t【{}】
                延期手续费:\t\t【{}】\n{}
            '''.format(login_in.USER_STATUS['username'],
                       chose_bill,
                       -bill_value,
                       pay_value,
                       debt,
                       repay_date1,
                       cost,
                       '*' * 60))
            log.info("【%s】-->查询%s帐期帐单" % (login_in.USER_STATUS['username'], chose_bill))
            input('按回车键继续')

        return flag


def transfer():
    '''
    转帐
    :return:
    '''
    user_id1 = input('请输入转帐帐号：').strip()
    user_id2 = input('请再次输入转帐帐号：').strip()
    if user_id1 == user_id2:
        if login_in.chack_dir_file(setting.PATH_USER, user_id2):
            # 如果有目录，帐号存在
            user_dict = json.load(open(login_in.get_file_dir(setting.PATH_USER)[user_id2], 'r'))
            transfer_fee, succ_no = withdraw_money_base('转帐')
            if succ_no:
                user_dict['saving'] += transfer_fee
                json.dump(user_dict, open(login_in.get_file_dir(setting.PATH_USER)[user_id2], 'w'))
                time.sleep(1)
                print('转帐成功！帐号：【%s】 已收到此笔转帐汇款！' % user_id2)
        else:
            print('输入帐号不存在！')
    else:
        print('两次输入信息不一致，请重新输入！')
    input('按回车键继续')


def pay_fee():
    '''
    消费
    :return: pay_money 消费的金额 ,succ_no 执行结果
    '''
    pay_money, succ_no = withdraw_money_base('消费')
    return pay_money, succ_no


def qt():
    global QUIT
    QUIT = False
    login_in.USER_STATUS = {'power': None, 'username': None, 'type': False}


def atm_user():
    flag = False
    while not flag:
        user_name, flag, adm_flag = login_in.login_in()
    if flag:
        if login_in.USER_STATUS['type']:
            while QUIT:
                show = '''\n已进入ATM机操作模块：
                            【1】取款
                            【2】还款
                            【3】存款
                            【4】查询帐单
                            【5】转帐
                            【6】修改密码
                            【7】退出'''
                print(show)
                inp = input('请选择您要进行的操作序列:\n>>').strip()

                show_dict = {
                    '1': withdraw_money,
                    '2': repay_money,
                    '3': save_money,
                    '4': show_bill,
                    '5': transfer,
                    '6': login_in.modify_password1,
                    '7': qt,
                }
                if inp in show_dict:
                    show_dict[inp]()
                else:
                    print('\033[31;1m非法操作!\033[0m')
                    continue

        else:
            print('管理权限帐号无取款、还款、存款、查询帐单、转帐功能')
            input('按回车键继续')
    else:
        input('按回车键继续')
