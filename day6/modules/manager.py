#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : xiongli


import pickle, sys, os, hashlib, time, re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import setting
from modules import log
log = log.log(setting.PATH_LOGFILE)


class Teacher:
    '''
    老师类
    '''
    def __init__(self, name):
        teacher_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'rb'))
        self.favor = teacher_dict[name]['teacher_favor']
        self.name = teacher_dict[name]['teacher_name']
        self.age = teacher_dict[name]['teacher_age']
        self.asset = teacher_dict[name]['teacher_asset']

    def accident(self, value):
        '''
        事故
        :param value:金额
        :return:
        '''
        self.asset -= value

    def gain(self, value):
        '''
        教学获得
        :param value:金额
        :return:
        '''
        self.asset += value


class Course:
    '''
    课程类
    '''
    def __get_dir_file(self, path):
        '''检查目录下是否存在该文件'''
        file_list = []
        for home, dirs, files in os.walk(path):
            for i in files:
                file_list.append(i)
        return file_list

    def show_course(self):
        chose = {}
        if 'course.pkl' not in self.__get_dir_file(setting.PATH_DB):
            print('无课程配置文件，请联系管理员新增后查询.')
            input('按回车键继续')
        else:
            course_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'course.pkl'), 'rb'))
            print('老师信息'.center(46, '*'))
            print('序号     课程名称     课时     代课老师')
            for i, j in enumerate(course_dict.keys(), start=1):
                number = i
                name = course_dict[j]['name']
                time = course_dict[j]['time']
                teacher = course_dict[j]['teacher']
                print('{}          {}       {}       {}'.format(number, name, time, teacher))
                chose.setdefault(i, j)
            print(''.center(50, '*'))
        return chose


class Student:
    '''
    学生类
    '''
    student_dict = {}

    def __init__(self, name):
        self.name = name
        self.pass_word = ''
        self.age = ''
        self.sex = ''
        self.course = []
        self.class_record = {}
        self.log = {}
        self.read_data()

    def read_data(self):
        if self.name in self.__get_dir_file(setting.PATH_STUDENT):
            student_dict = pickle.load(open(os.path.join(setting.PATH_STUDENT, self.name), 'rb'))
            self.name = student_dict[self.name]['name']
            self.pass_word = student_dict[self.name]['pass_word']
            self.age = student_dict[self.name]['age']
            self.sex = student_dict[self.name]['sex']
            self.course = student_dict[self.name]['course']
            self.class_record = student_dict[self.name]['class_record']
            self.log = student_dict[self.name]['log']
        else:
            self.name = ''
            self.pass_word = ''
            self.age = ''
            self.sex = ''
            self.course = []
            self.class_record = {}
            self.log = {}

    # def __del__(self):
    #     self.save_data(self.name)

    def save_data(self):
        Student.student_dict[self.name] = {'name': self.name,
                                           'pass_word': self.pass_word,
                                           'age': self.age,
                                           'sex': self.sex,
                                           'course': self.course,
                                           'class_record': self.class_record,
                                           'log': self.log}
        pickle.dump(Student.student_dict, open(os.path.join(setting.PATH_STUDENT, self.name), 'wb'))

    def __get_dir_file(self, path):
        '''检查目录下是否存在该文件'''
        file_list = []
        for home, dirs, files in os.walk(path):
            for i in files:
                file_list.append(i)
        return file_list

    def show_course(self):
        chose = {}
        course_dict = {}
        if 'course.pkl' not in self.__get_dir_file(setting.PATH_DB):
            print('无课程配置文件，请联系管理员新增后查询.')
            input('按回车键继续')
        else:
            course_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'course.pkl'), 'rb'))
            print('课程信息'.center(46, '*'))
            print('序号     课程名称     课时     代课老师')
            for i, j in enumerate(course_dict.keys(), start=1):
                number = i
                name = course_dict[j]['name']
                times = course_dict[j]['time']
                teacher = course_dict[j]['teacher']
                print('{}          {}       {}       {}'.format(number, name, times, teacher))
                chose.setdefault(i, j)
            print(''.center(50, '*'))
        return chose, course_dict

    def chose_course(self):
        chose, course_dict = self.show_course()
        self.read_data()
        flag = True
        while flag:
            course_course_no = input('请选择课程序号：\n>>')
            if not course_course_no.isdigit():
                print('只能输入数字，请核实后再输入.')
                input('按回车键继续...')
                continue
            if int(course_course_no) not in chose:
                print('输入序号不在范围内')
                input('按回车键继续...')
            else:
                course_course_name = chose[int(course_course_no)]
                self.course.append(course_course_name)
                self.class_record[course_course_name] = {'course': course_course_name, 'speed': 0,
                                                         'teacher': course_dict[course_course_name]['teacher']}
                flag = False
                print('学生：【{}】已选择课程：【{}】'.format(self.name, course_course_name))
                log.info('【{}】-->已选择课程：【{}】！'.format(self.name, course_course_name))
                self.save_data()

    def evaluation_teacher(self, teacher_name):
        print('对老师进行评价'.center(20, '*'))
        print('\n1: 好评;\n2:中评；\n3:差评；')
        t = Teacher(teacher_name)
        evaluation = input('请输入编号：')
        if evaluation == '1':
            t.gain(2)
            print('已对老师做出好评！')
        elif evaluation == '2':
            t.gain(1)
            print('已对老师做出中评！')
        elif evaluation == '3':
            t.accident(1)
            print('已对老师做出差评！')
        else:
            print('输入错误，只能输入1、2、3')
            input('按回车键继续')

    def class_begin(self):
        teacher = ''
        if not self.class_record.keys():
            print('无课程信息，无法学习...')
            input('按回车键继续...')
        else:
            chose = {}
            print('学习信息'.center(46, '*'))
            print('序号     课程名称     学习进度     代课老师')
            for i, j in enumerate(self.class_record, start=1):
                number = i
                course = self.class_record[j]['course']
                speed = self.class_record[j]['speed']
                teacher = self.class_record[j]['teacher']
                print('{}       {}          {}%         {}'.format(number, course, speed, teacher))
                chose.setdefault(i, [course, speed])
            print(''.center(50, '*'))

            flag = True
            while flag:
                course_course_no = input('请选择学习课程序号：\n>>')
                if not course_course_no.isdigit():
                    print('只能输入数字，请核实后再输入.')
                    input('按回车键继续...')
                    continue
                if int(course_course_no) not in chose:
                    print('输入序号不在范围内')
                    input('按回车键继续...')
                elif int(chose[int(course_course_no)][1]) == 100:
                    print('本课程已学习完成...')
                    input('按回车键继续...')
                else:
                    course_course_name = chose[int(course_course_no)][0]
                    print('学生：【{}】开始学习【{}】'.format(self.name, course_course_name))
                    course_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'course.pkl'), 'rb'))
                    print('正在学习...\n{}'.format(course_dict[course_course_name]['info']))
                    time.sleep(2)
                    print('本节课程已经学习完成...')
                    # 进度增加为： 1/总课时
                    self.class_record[course_course_name]['speed'] += 1/int(course_dict[course_course_name]['time']) * 100
                    self.log.setdefault(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), course_course_name)
                    log.info('【{}】-->已完成学习：【{}】,学习时间：【{}】！'.format(self.name,
                                                                   course_course_name,
                                                                   time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                 time.localtime())))
                    # 评价
                    self.evaluation_teacher(teacher)
                    flag = False
                    self.save_data()
                    input('按回车键继续...')

    def login(self, name, password):
        if not os.path.exists(os.path.join(setting.PATH_STUDENT, name)):
            print('用户不存在!')
            return False
        else:
            student_dict = pickle.load(open(os.path.join(setting.PATH_STUDENT, name), 'rb'))
            if name == student_dict[name]['name'] and password == student_dict[name]['pass_word']:
                print('【{}】登录成功!'.format(name))
                setting.USER_STATUS['student'] = name
                return True
            else:
                print('用户名或者密码错误!')
                return False

    @classmethod
    def md5(cls, password):
        '''
        md5加密
        :param password: 明文密码
        :return: MD5密码
        '''
        password_md5 = hashlib.md5(bytes('ooxx', encoding='utf-8'))
        password_md5.update(bytes(password, encoding='utf-8'))
        return password_md5.hexdigest()

    @staticmethod
    def register():
        student_dict = {}
        flag = True
        name = ''
        while flag:
            name = input('请输入增加学生名字：\n>>')
            if os.path.exists(os.path.join(setting.PATH_STUDENT, name)):
                print('\033[31;1m 用户已经存在!\033[0m')
                input('按回车键继续...')
                return False
            else:
                flag = False

        flag = True
        pass_word = ''
        while flag:
            pass_word1 = input('密码：\n>>')
            pass_word2 = input('请再次输入密码：\n>>')
            if pass_word2 != pass_word1:
                print('两次输入的密码不一致，请重新输入')
                input('按回车键继续...')
            else:
                pass_word = Student.md5(pass_word2)
                flag = False

        flag = True
        age = 0
        while flag:
            age = input('学生年龄(仅数字)：\n>>')
            if not age.isdigit():
                print('只能输入数字，请核实后再输入.')
                input('按回车键继续...')
            else:
                flag = False

        sex = input('学生性别：\n>>')

        course = []
        class_record = {}
        log = {}
        student_dict[name] = {'name': name,
                              'pass_word': pass_word,
                              'age': age,
                              'sex': sex,
                              'course': course,
                              'class_record': class_record,
                              'log': log}
        pickle.dump(student_dict, open(os.path.join(setting.PATH_STUDENT, name), 'wb'))
        print('注册成功!')

    def show_study_history(self):
        '''查看用户上课记录'''
        print('学习记录'.center(46, '*'))
        print('序号     课程名称     学习时间')
        for i, j in enumerate(self.log, start=1):
            number = i
            study_name = self.log[j]
            print('{}       {}          {}'.format(number, study_name, j))


class Manager(Teacher, Course):
    '''
    管理员类
    '''
    def __init__(self):
        pass

    def __get_dir_file(self, path):
        '''检查目录下是否存在该文件'''
        file_list = []
        for home, dirs, files in os.walk(path):
            for i in files:
                file_list.append(i)
        return file_list

    def add_teacher(self):
        '''增加老师'''

        if 'teacher.pkl' in self.__get_dir_file(setting.PATH_DB):
            teacher_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'rb'))
        else:
            teacher_dict = {}
        flag = True
        teacher_name = ''
        while flag:
            teacher_name = input('请输入增加老师名字：\n>>')
            if teacher_dict.get(teacher_name):
                print('老师已存在，请核实后再输入.')
                input('按回车键继续...')
            else:
                flag = False
        teacher_favor = input('老师爱好：\n>>')
        flag = True
        teacher_age = 0
        while flag:
            teacher_age = input('老师年龄(仅数字)：\n>>')
            if not teacher_age.isdigit():
                print('只能输入数字，请核实后再输入.')
                input('按回车键继续...')
            else:
                flag = False
        teacher_asset = 0
        teacher_dict[teacher_name] = {'teacher_name': teacher_name,
                                      'teacher_favor': teacher_favor,
                                      'teacher_age': teacher_age,
                                      'teacher_asset': teacher_asset}
        pickle.dump(teacher_dict, open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'wb'))

    def show_teacher(self):
        '''老师信息'''
        chose = {}
        if 'teacher.pkl' not in self.__get_dir_file(setting.PATH_DB):
            print('无老师配置文件，请先新增后查询.')
            input('按回车键继续')
        else:
            teacher_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'rb'))
            print('老师信息'.center(46, '*'))
            print('序号     姓名     年龄     资产')
            for i, j in enumerate(teacher_dict.keys(), start=1):
                number = i
                name = teacher_dict[j]['teacher_name']
                age = teacher_dict[j]['teacher_age']
                asset = teacher_dict[j]['teacher_asset']
                print('{}          {}       {}       {}'.format(number, name, age, asset))
                chose.setdefault(i, j)
            print(''.center(50, '*'))
        return chose

    def del_teacher(self):
        '''删除老师'''
        self.show_teacher()
        name = input('输入需要删除的老师姓名：\n>>').strip()
        teacher_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'rb'))
        if teacher_dict.get(name):
            del teacher_dict[name]
            print('老师：【{}】已删除！'.format(name))
            pickle.dump(teacher_dict, open(os.path.join(setting.PATH_DB, 'teacher.pkl'), 'wb'))
        else:
            print('输入老师姓名错误！')

    def add_course(self):
        '''增加课程'''
        if 'course.pkl' in self.__get_dir_file(setting.PATH_DB):
            course_dict = pickle.load(open(os.path.join(setting.PATH_DB, 'course.pkl'), 'rb'))
        else:
            course_dict = {}

        flag = True
        course_name = ''
        while flag:
            course_name = input('请输入需要添加的课程：\n>>')
            if course_dict.get(course_name):
                print('课程已存在，请核实后再输入.')
                input('按回车键继续...')
            else:
                flag = False

        flag2 = True
        course_time = ''
        while flag2:
            course_time = input('请输入总课时（仅数字)：\n>>')
            if not course_time.isdigit():
                print('只能输入数字，请核实后再输入.')
                input('按回车键继续...')
            else:
                flag2 = False
        chose = self.show_teacher()

        course_info = input('请输入课程内容：\n>>')

        flag3 = True
        course_teacher = ''
        while flag3:
            course_teacher_no = input('请选择代课老师序号：\n>>')
            if not course_teacher_no.isdigit():
                print('只能输入数字，请核实后再输入.')
                input('按回车键继续...')
                continue
            if int(course_teacher_no) not in chose:
                print('输入序号不在范围内')
                input('按回车键继续...')
            else:
                course_teacher = chose[int(course_teacher_no)]
                flag3 = False

        course_dict[course_name] = {'name': course_name,
                                    'time': course_time,
                                    'teacher': course_teacher,
                                    'info': course_info}
        pickle.dump(course_dict, open(os.path.join(setting.PATH_DB, 'course.pkl'), 'wb'))
        print('已添加新课程：【{}】'.format(course_name))

    def login(self, name, password):
        if not os.path.exists(os.path.join(setting.PATH_MANAGER, name)):
            print('用户不存在!')
            return False
        else:
            student_dict = pickle.load(open(os.path.join(setting.PATH_MANAGER, name), 'rb'))
            if name == student_dict[name]['name'] and password == student_dict[name]['pass_word']:
                print('【{}】登录成功!'.format(name))
                setting.USER_STATUS['student'] = name
                return True
            else:
                print('用户名或者密码错误!')
                return False

