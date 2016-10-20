#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import re


def base_mul(num):
    '''
    乘除处理
    :param num: 计算表达式
    :return: 递归乘除处理
    '''
    value = re.search(r'(-?\d+\.*\d*)[*/]([+-]?\d+\.*\d*)', num)
    if not value:
        return num
    if num.count('*') + num.count('/') >= 1:
        a = re.search(r'(-?\d+\.*\d*)[*/]([+-]?\d+\.*\d*)', num).group()
        if len(a.split('*')) > 1:
            n1, n2 = a.split('*')
            v = str(float(n1) * float(n2))
        else:
            n1, n2 = a.split('/')
            v = str(float(n1) / float(n2))
        num = num.replace(a, v)
        return base_mul(num)


def base_add(num):
    '''
    加减处理
    :param num:计算表达式
    :return:计算结果
    '''
    value = re.search(r'(-?\d+\.*\d*)[+-]([+-]?\d+\.*\d*)', num)
    if not value:
        return num
    if num.count('+-') + num.count('--') + num.count('*-') + num.count('/-') >= 1:
        if num.count('*-') >= 1:
            num = num.replace(re.search(r'(-?\d*\.*\d*)?\*-(-?\d*\.*\d*)', num).group(),
                              '-'+re.search(r'(-?\d*\.*\d*)?\*-(-?\d*\.*\d*)', num).group().replace('*-', '*'))
        if num.count('/-') >= 1:
            num = num.replace(re.search(r'(-?\d*\.*\d*)?\/-(-?\d*\.*\d*)', num).group(),
                              '-'+re.search(r'(-?\d*\.*\d*)?\/-(-?\d*\.*\d*)', num).group().replace('/-', '*'))
        num = num.replace('--', '+')
        num = num.replace('+-', '-')
    a = re.search(r'(-?\d+\.*\d*)[+-]([+-]?\d+\.*\d*)', num).group()
    if len(a.split('+')) > 1:
        n1, n2 = a.split('+')
        v = str(float(n1) + float(n2))
    else:
        n1, n2 = a.split('-')
        v = str(float(n1) - float(n2))
    num = num.replace(a, v)
    return base_add(num)


def calculate(num):
    '''
    计算处理
    :param num: 计算表达式
    :return: 计算结果
    '''
    value = base_mul(num)
    if not value.count('+') + value.count('-') >= 1:
        return value
    else:
        value_add = base_add(value)
        return value_add


def remove_par(num):
    '''
    去括号，并计算括号内容
    :param num: 计算表达式
    :return: 计算结果
    '''
    if num.count('(') >= 1:  # 有括号
        a = re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)', num).group()
        num = num.replace(a, calculate(a[1:-1]))  # 去两头扩号
        print(num)
        return remove_par(num)
    else:       # 无括号
        return calculate(num)


def main():
    flag = True
    print('计算器'.center(20, '*'))
    while flag:
        info = input('\n请输入计算内容(q:退出)：\n>>')
        if info == 'q' or info == 'Q':
            flag = False
        else:
            print('计算中，请稍后...')
            a = remove_par(info)
            print('计算结果为：\033[32;1m[ %s ]\033[0m' % a)
            input('按回车键继续')
    exit('计算器已退出！')

if __name__ == '__main__':
    main()
