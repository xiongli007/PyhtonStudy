#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import json

def ShowMenu(key):  ###解析字典，并展示
    chose = {}
    print('-----------------------')
    for num, item in enumerate(key):  ##遍历F中的元素和下标，并做输出展示
        print('%d| %s' % (num, item))
        chose.setdefault(num, item)
    print('b| back')
    print('q| quit')
    print('-----------------------')
    incode = input('请输入选择的编码:')
    return chose ,incode

with open('menu.json','r+',encoding='utf-8') as file:   ###读JSON文件
    f = json.loads(file.read())

count =1      ##初始化层级
value =''

while 1:
    if count ==1:                                                   ###层级1，展示字典的第一层
        chose,incode=ShowMenu(f.keys())
        if incode == 'b':                                           ###判断输入值
            print('--------------已是最顶层!---------------- ')  ##返回上一层
        elif incode == 'q':
            break                           ##退出
        else:
            count += 1
            value = chose.get(int(incode))                          ##得到选择的第二层级值
    elif count ==2:
        chose,incode = ShowMenu(f[value].keys())                     ##展示选择的第二级菜单
        if incode == 'b':                                           ###判断输入值
            count -= 1                       ##返回上一层
        elif incode == 'q':
            break                           ##退出
        else:
            count += 1
            key = chose.get(int(incode))                            ##得到选择的第三层级值
    else:
        chose,incode= ShowMenu(f[value][key])                       #展示选择的第三级菜单
        if incode == 'b':
            count -= 1  ##返回上一层
        elif incode == 'q':
            break  ##退出
        else:
            if count == 3:  ##记数器为3，打印最底层
                print('----------------已是最底层，请输入 b 返回!-------------- ')
