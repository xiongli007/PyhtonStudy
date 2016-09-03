#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import json

IP_ADDR = ''
WEIGHT = 0
MAXCONN = 0


def type_chg(inp):
    '''
    输入配置格式转化  字符串转化为字典
    入参：字符串
    返回值 ： 字典类型
    '''
    global IP_ADDR
    global WEIGHT
    global MAXCONN
    read_dict = json.loads(inp)
    read_backend = read_dict['backend']
    read_record = 'server ' \
                  + read_dict['record']['server'] \
                  + " " \
                  + read_dict['record']['server'] \
                  + " weight " \
                  + str(read_dict['record']['weight']) \
                  + ' maxconn ' \
                  + str(read_dict['record']['maxconn'])
    IP_ADDR = read_dict['record']['server']
    WEIGHT = read_dict['record']['weight']
    MAXCONN = read_dict['record']['maxconn']
    return read_backend, read_record


def select_backend(backend):
    '''
    查配置文件
    入参：输入需要查找的服务地址
    返回值：查询结果,有无backend，有无配置信息
    '''
    result = []
    with open('ha.conf', 'r', encoding='utf-8') as f:
        flag = False
        has_cfg = True
        for line in f:
            if line.strip().startswith("backend") and line.strip() == "backend " + backend:
                flag = True
                continue
            if flag and line.strip().startswith("backend"):
                break
            if flag and line.strip():
                result.append(line.strip())

    if len(result) == 0 and flag:      # 有backend服务器信息，无配置内容
        # print('指定的backend信息无配置内容')
        has_cfg = False

    if len(result) == 0 and not flag:      # 无backend服务器信息，无配置内容
        # print('未找到backend信息')
        has_cfg = False

    return result, flag, has_cfg


def insert_backend(backend, record):
    '''
    插入配置文件
    入参：输入需要插入的配置信息
    返回值：无
    '''
    global IP_ADDR
    ip_addr =False
    rq, chack_backend, has_cfg = select_backend(backend)
    if IP_ADDR in str(rq):
        ip_addr = True
    with open('ha.conf', 'r', encoding='utf-8') as old, open('newha.conf', 'w') as new:
        in_backend = False          # 是否在backend标签范围内标示
        has_backend = False         # 是否存在增加服务器配置backend标示
        has_record = False          # 是否与输入配置一致标示
        for line in old:

            # 如果成功匹配输入内容，打开in_backend标示，把原内容写入新文档
            if line.strip().startswith('backend') and line.strip() == 'backend ' + backend:
                in_backend = True
                has_backend = True
                new.write(line)
                continue

            # 在目标backend标签范围内，再次找到backend，在其前一行插入输入配置记录 ; IP地址不一样时
            if line.strip().startswith('backend') and in_backend and not ip_addr:
                if not has_record:
                    new.write(' '*8 + record + '\n')
                new.write(line)
                in_backend = False
                continue

            # 在目标backend标签范围内，找到与输入配置一致信息
            if in_backend and line.strip() == record and not ip_addr:
                has_record = True
                new.write(line)
                continue

            # 在目标backend标签范围内，找到包含输入配置信息,即替换同一IP配置
            if in_backend and IP_ADDR in line.strip() and ip_addr:
                has_record = True
                ip_addr = False
                new.write(' ' * 8 + record + '\n')
                continue

            # ha.conf 不为空则写入新文件
            if line.strip():
                new.write(line)

        # 如果不存在增加服务器配置backend标示
        if not has_backend:
            new.write('\nbackend ' + backend + '\n')
            new.write(' '*8 + record + '\n')

        # 如果backend标签范围内标示未正常结束，表示backend目标服务为最后一个backend
        if in_backend and not has_record:
            new.write('\n' + ' '*8 + record + '\n')

        if not chack_backend:
            print('创建backend完毕！'.center(50, '*'))
        else:
            print('配置插入完毕！'.center(50, '*'))
    rename_file('ha.conf', 'newha.conf')


def delete_backend(backend, record):
    '''
    删除配置文件
    入参：输入需要删除的配置信息
    返回值：无
    '''
    del_backend = False                     # 是否删除backend标签标示
    in_backend = False                      # 是否在backend标签范围内标示
    rq, chack_backend, has_cfg = select_backend(backend)
    if chack_backend:
        if record in rq and len(rq) == 1 and chack_backend and has_cfg:       # 有backend服务器信息，并且只有删除配置内容
            del_backend = True

        if chack_backend or has_cfg:
            with open('ha.conf', 'r', encoding='utf-8') as old, open('newha.conf', 'w') as new:
                for line in old:
                    # 如果成功匹配输入内容，且只有删除配置内容，不写新文件
                    if line.strip().startswith('backend') and line.strip() == 'backend ' + backend and del_backend:
                        in_backend = True
                        # has_backend = True
                        print('删除%s操作成功！' % backend)
                        continue

                    # 如果成功匹配输入内容，打开in_backend标示，把原内容写入新文档
                    if line.strip().startswith('backend') and line.strip() == 'backend ' + backend and not del_backend:
                        in_backend = True
                        new.write(line)
                        continue

                    # 在目标backend标签范围内，找到与输入配置一致信息,不写新文件
                    if in_backend and line.strip() == record:
                        # has_record = True
                        print('删除%s操作成功！' % record)
                        continue

                    # ha.conf 不为空则写入新文件
                    if line.strip():
                        new.write(line)
            rename_file('ha.conf', 'newha.conf')
    if record not in str(rq) or not chack_backend or not has_cfg:
        print('无删除数据！')


def copy_file():
    '''备份文件
    入参：文件名
    返回值：无
    '''
    import time
    import shutil
    shutil.copyfile('ha.conf', time.strftime('%Y%m%d') + 'ha.conf')
    print('配置文件备份为：' + time.strftime('%Y%m%d') + 'ha.conf')


def rename_file(old_name, new_name):
    '''配置文件重命名
    入参：旧名称，新名称
    返回值： 无
    '''
    import os
    os.rename(old_name, old_name+'bak')
    os.rename(new_name, old_name)


def main():
    copy_file()
    while True:
        mag = '''
    1.获取backend记录;
    2.增加backend记录;
    3.删除backend记录;
    q:退出; '''
        print(''.center(50, '*'))
        print(mag)
        print(''.center(50, '*'))
        put = input("请输入操作序号：")
        if put == '1':
            inp_backend = input('请输入backend：')
            request, flag, has_cfg = select_backend(inp_backend)
            if len(request) == 0 and flag:  # 有backend服务器信息，无配置内容
                print('指定的backend信息无配置内容')
            elif len(request) == 0 and not flag:  # 无backend服务器信息，无配置内容
                print('未找到backend信息')
            if flag and has_cfg:
                print('获取的数据为：')
                for i in request:
                    print(i)
        elif put == '2':
            inp = input('''格式:\033[33;0m{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}\033[0m
请输入要新加的记录：''')
            read_backend, read_record = type_chg(inp)
            insert_backend(read_backend, read_record)
        elif put == '3':
            inp = input('''输入格式:\033[33;0m{"backend": "buy.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}\033[0m
请输入要删除的记录：''')
            read_backend, read_record = type_chg(inp)
            delete_backend(read_backend, read_record)
        elif put =='q' or put == 'Q':
            print('退出程序,bye bye !')
            break
        else:
            print("输入非法字符,请输入正确信息！ ")

main()
