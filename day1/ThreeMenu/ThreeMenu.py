#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import codecs

PRAENT_ID ='0'

def ReadMenu(class_id_new, parent,class_hie):
    global PRAENT_ID
    if class_hie =='u' :   ###如果向上展示，变更父结点
        with codecs.open('MenuInfo.txt', 'r', 'utf-8') as r2:      ###读层级关系文件
            lines2 = r2.readlines()
            for i2 in lines2:
                t2 = i2.split('|')
                if t2[0] == str(parent) and t2[2] == '1':               #读父节点上一层的唯一编码
                    PRAENT_ID= t2[3]                                     ##并赋值给全局变量PRAENT_ID
                    break

    with codecs.open('MenuInfo.txt', 'r', 'utf-8') as r2:         ###读层级关系文件，把父节点是PRAENT_ID的渠道编码写入列表group2
        lines2 = r2.readlines()
        for i2 in lines2:
            t2 = i2.split('|')                                        ##切片
            if t2[3] == PRAENT_ID and t2[2] == '1':                     ##把父节点是PRAENT_ID所对应的渠道编码写入列表group2，即把选中的渠道下一层级写入列表
                group2.append(t2[0])

        with codecs.open('MenuMsg.txt', 'r', 'utf-8') as r1:        ###读渠道信息文件
            lines1 = r1.readlines()
            for g in range(len(group2)):                                ##以列表的元素个数来生成数列
                g = group2.pop()                                         ##取内容
                for i1 in lines1:
                    t1 = i1.split('|')
                    if t1[2] == str(class_id) and t1[0] == g:           ##将列表group2的编码和解析出的名字写入字典group
                        group.setdefault(t1[0], t1[1])

if __name__== '__main__':
    class_id = 1
    class_hie = 'd'    ### u -->向上  d -->向下
    group_id = 0
    group = {}
    group2 = []
    show = {}
    showMenu = {}
    while True:
        ReadMenu(class_id,PRAENT_ID,class_hie)
        print('------------------')
        for num, item in enumerate(group.items()):  ##遍历group中的元素和下标，并做输出展示
            print(num, item[1])
            show.setdefault(num, item[0])            ##保存下标和编码的键/值对，以做输入判断用
        print('------------------')
        print('b : back')
        print('q : quit')
        print('-----------------------------')
        chose = input('请输入对应编号：')           ##提示输入信息
        if chose =='q':                              ##如果是q，则退出！
            print('Bye Bye!!')
            break
        elif chose =='b':                           #如果是b，则展示上级菜单！
            class_id -= 1
            if class_id==0 :
                print('已是最顶层！')
            class_hie='u'                           #改变菜单执行状态,U 为向上展示
            group.clear()                           ##清空展示字典
            show.clear()
        else:                                       ##如果是数字，这里没学正则表达式，无法判断输入是否为数据，后期修改此BUG
            class_hie = 'd'                         ###改变菜单执行状态,D为向下展示
            PRAENT_ID=show.get(int(chose))          ##用get方法将输入的键对应的渠道编码作为向下展示的父节点
            class_id +=1                            ##展示层级加1
            group.clear()                           ##清空展示字典
            show.clear()


