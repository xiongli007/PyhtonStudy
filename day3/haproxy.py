#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


def select_backend():
    pass


def main():
    mag = '''
        1.获取backend记录；
        2.增加backend记录;
        3.删除backend记录;
        '''
    print(mag)
    put = input("请输入操作序号：")
    if put == '1':
        read = input('请输入backend：')

    elif put == '2':
        pass
    elif put == '3':
        pass
    else:
        print("输入非法字符,请输入正确信息！ ")
