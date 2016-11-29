#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli

import os, sys, pickle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import log
from modules import manager
from conf import setting


def student_function(st):
    '''学生功能选择'''
    print(''.center(20, '*'))
    print('''【1】 选课\n【2】 课程学习\n【3】 学习记录\n【4】 返回上级''')
    menu_dict = {'1': st.chose_course,
                 '2': st.class_begin,
                 '3': st.show_study_history,
                 '4': back}
    inp = input('请输入编码：\n>>').strip()
    if inp in menu_dict and inp != '4':
        menu_dict[inp]()
    elif inp == '4':
        return 'q'
    else:
        print('输入非法字符，请输入【1-3】功能代码！')


def student_login():
    '''学生登陆'''
    flag = True
    while flag:
        if not setting.USER_STATUS['student']:
            name = input('学生登录账号：\n>>').strip()
            pass_word = input('密码：\n>>').strip()
            st = manager.Student(name)
            pass_word = st.md5(pass_word)
            if st.login(name, pass_word):
                setting.USER_STATUS['student'] = name
            else:
                flag = False
        else:
            # 实例化
            st = manager.Student(setting.USER_STATUS['student'])
            qt = student_function(st)
            if qt == 'q':
                flag = False


def student_register():
    '''学生注册'''
    manager.Student.register()


def qt():
    exit('退出选课系统，bye~bye!')


def back():
    pass


def student_chose():
    '''学生入口选择'''
    print('【1】 登录\n【2】  注册\n【3】  返回上级')
    menu_dict = {'1': student_login,
                 '2': student_register,
                 '3': qt}
    inp = input('请输入编码：\n>>').strip()
    if inp in menu_dict and inp != '3':
        menu_dict[inp]()
    elif inp == '3':
        pass
    else:
        print('输入非法字符，请输入【1-3】功能代码！')


def manager_function(st):
    '''管理员功能选择'''
    print(''.center(20, '*'))
    print('''【1】 新增老师\n【2】 查看老师信息\n【3】 删除老师\n【4】 增加课程\n【5】 返回上级 ''')
    menu_dict = {'1': st.add_teacher,
                 '2': st.show_teacher,
                 '3': st.del_teacher,
                 '4': st.add_course,
                 '5': back,
                 }
    inp = input('请输入编码：\n>>').strip()
    if inp in menu_dict and inp != '5':
        menu_dict[inp]()
    elif inp == '5':
        return 'q'
    else:
        print('输入非法字符，请输入【1-5】功能代码！')


def manager_login():
    '''管理员登陆'''
    flag = True
    while flag:
        if not setting.USER_STATUS['manager']:
            name = input('管理员登录账号：\n>>').strip()
            pass_word = input('密码：\n>>').strip()
            st = manager.Manager()
            pass_word = manager.Student.md5(pass_word)
            if st.login(name, pass_word):
                setting.USER_STATUS['manager'] = name
            else:
                flag = False
        else:
            # 实例化
            st = manager.Manager()
            qt = manager_function(st)
            if qt == 'q':
                flag = False


def manager_chose():
    '''管理员入口选择'''
    print('【1】 登录\n【2】  返回上级')
    menu_dict = {'1': manager_login,
                 '2': qt, }
    inp = input('请输入编码：\n>>').strip()
    if inp in menu_dict and inp != '2':
        menu_dict[inp]()
    elif inp == '2':
        pass
    else:
        print('输入非法字符，请输入【1-2】功能代码！')


def main():
    '''
    主函数
    :return:
    '''
    while True:
        print('选课系统'.center(20, '*'))
        print('【1】 学生入口\n【2】  管理员入口\n【3】  退出')
        print(''.center(24, '*'))
        menu_dict = {'1': student_chose,
                     '2': manager_chose,
                     '3': qt}
        inp = input('请输入编码：\n>>').strip()
        if inp in menu_dict:
            menu_dict[inp]()
        else:
            print('输入非法字符，请输入【1-3】功能代码！')


if __name__ == '__main__':
    # student_dict = pickle.load(open(os.path.join(setting.PATH_STUDENT, 'xiongli'), 'rb'))
    main()
