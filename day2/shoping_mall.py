#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author :  xiong li

import pickle


# ####################用户登陆############################
INPUT = {}
user_salary = 0                     # 用户余额
shopping_car_his = {}               # 历史数据


def check_lock(user_name):                               # ##检查帐号是否加锁
    with open('db/lock.txt', 'r') as lock:                    # #读加锁帐号文件信息
        for i in lock:                                 # #循环读出的加锁信息
            if i.split() == user_name.split():           # #切片，踢掉换行符，进行内容比较，如果相等 返回True
                return True
    return False                                       # #否则返回False


def check_error_count(user_name):
    if INPUT[user_name] >= 3:
        print("帐号或密码输入错误次数已达3次，帐号被锁定！")  # #如果大于等于3次，打印帐号锁定提示
        q = lock_user(user_name)  # #调用锁定帐号函数
        return True
    else:
        return False  # #如果帐号相等，密码不相等，赋值为N


def check_user(user_name, pass_word):               # ##检查帐号/密码是否正确
    global INPUT
    with open('db/UserMsg.txt', 'r') as User_Pass:         # #读帐号密码文件信息
        for i in User_Pass:                                # #循环读帐号密码文件信息
            a = i.split('|')                              # #用分隔符为|进行切片，切片内容传给列表
            user = a[0]                                    # #取用户数据
            user_pass_word = a[1]                                 # #取密码数据
            if user_name == user and pass_word == user_pass_word:   # #将入参与文件的帐号、密码进行等值判断
                rt1 = 'Y'                                   # #如果相等，赋值为Y
                break
            elif user_name == user and pass_word != user_pass_word:
                INPUT[user_name] = int(INPUT[user_name]) + 1                     # #该帐号信息锁定次数加1
                rt1 = 'N'
                break
            elif user_name != user:
                rt1 = 'None'                                # #如果帐号不相等，赋值为None
        if check_error_count(user_name):
            rt1 = 'q'
        return rt1


def lock_user(user_name):                 # ##锁定帐号
    with open("db/lock.txt", 'a') as f:
        f.write('%s\n ' % user_name)
    return True


def login_in():               # ##用户登陆
    msg = '''
***********************************
        欢迎进入屌丝购物中心
***********************************
        '''
    print(msg)  # 打印欢迎信息

    while True:
        username = input("请输入登陆账号：")  # 打印登陆提示
        # password = getpass.getpass("请输入密码: ")      # 因getpass在pycharm 有BUG,为便于测试，用input替换
        password = input("请输入密码:")  # 测试时使用，替换getpass
        INPUT.setdefault(username, 0)
        if check_lock(username):         # 检查录入帐号是否锁定
            exit("该帐号已锁定！请联系管理员处理，谢谢！")
        else:
            user_pass = check_user(username, password)   # 如果未被锁，检查用户名和密码录入是否正确定
            if user_pass == 'Y':
                print("登陆成功！")    # 用户名和密码录入正确，返回用户信息
                return username
            elif user_pass == 'N':
                print("帐号或密码输入错误,请重新输入！")
                continue                # 密码录入不正确，校验尝试次数
            elif user_pass == 'q':
                break
            elif user_pass == 'None':
                print("帐号未注册,Bye Bye ！")  # ##用户名不正确，打印退出
                exit("帐号未注册！")


# 保存购物信息和余额
def save_shopping_data(shopping_car, username, salary):
    if len(shopping_car) < 1:                    # 购物车无宝贝,不做保存
        pass
    else:
        shopping_car_his[username].setdefault('salary', salary)  # 插入余额

        with open('db\data.pkl', 'wb') as f:                            # 保存文件
            pickle.dump(shopping_car_his, f)


def pay_money(salary):    # 余额充值
    pay = input("需要充值多少元？ ")
    if pay.isdigit():
        salary += int(pay)              # 充值
        return salary
    else:
        print("输入非法字符,请输入正确信息！ ")


def show_shopping_car(shopping_car, username, salary):
    global user_salary
    if not shopping_car.get(username):
        print('本次未购买宝贝，购物车空空的~~~')
    else:
        if 'salary' in shopping_car[username]:      # 如果字典有余额，则删除
            shopping_car[username].pop('salary')
            print("上次购买的宝贝为：".center(50, '*'))
        else:
            print("本次购买的宝贝为：".center(50, '*'))
        print('编号\t宝贝\t单价\t数量\t小计 ')
        shopping_money = 0
        for index_car, item_car in enumerate(shopping_car[username]):
            print('%d\t %s\t %d\t %d\t %d\t'
                  % (index_car,
                     item_car,
                     shopping_car[username][item_car][0],
                     shopping_car[username][item_car][1],
                     shopping_car[username][item_car][0] * shopping_car[username][item_car][1])
                  )
            shopping_money += shopping_car[username][item_car][0] * shopping_car[username][item_car][1]

        print('总共消费(元)：%d' % shopping_money)
        print("end".center(60, '*'))
    print("你的余额为： \033[31;1m[%s]元\033[0m" % salary)
    user_salary = salary


# 加载历史购买记录
def read_his_msg(username):
    global shopping_car_his
    with open('db\data.pkl', 'rb') as f:  # 读文件
        if len(f.read()) < 1:
            print('无历史购买记录'.center(50, '-'))
        else:
            shopping_car_his = pickle.load(open('db\data.pkl', 'rb'))
            if username in shopping_car_his.keys():     # 帐号有历史数据
                show_shopping_car(shopping_car_his, username, shopping_car_his[username]['salary'])   # 展示历史购买记录
            else:
                print("无历史购买记录".center(50, '-'))


product_list = {
    "家电类": {
        '冰箱': 6000,
        '三星电视': 4888,
        '海尔洗衣机': 3999,
    },
    "衣服类": {
        'jack': 600,
        'k-boxing': 688,
        '海南之家': 399,
    },
    "手机类": {
        'Iphone 6S': 6000,
        '三星 S7': 6888,
        '小米5': 2599,
    },
    "汽车类": {
        '大众 ': 13000,
        '奥迪A6': 800000,
        'BMW x5': 60000,
    },
}


def main():
    exit_flag = False
    username = login_in()            # 用户登陆
    read_his_msg(username)           # 加载历史信息
    welcome_msg = '欢迎来到屌丝购物中心 '.center(50, '-')
    print(welcome_msg)
    salary = int(user_salary)
    shopping_car = {}
    while exit_flag is not True:
        chose = {}
        chose2 = {}
        salary_flag = False
        print("购物菜单：".center(50, '-'))
        for item in enumerate(product_list):   # 一级菜单
            index = item[0]
            p_name = item[1]
            chose.setdefault(index, p_name)
            print(index, '.', p_name)
        user_choice = input("[q=退出, c=购物车 ] 请选择购物大类 :")
        if user_choice.isdigit() and int(user_choice) < len(product_list):   # 选择大类 且在输入边界
            p_item = chose[int(user_choice)]
            for item2 in enumerate(product_list[p_item]):    # 二级菜单
                index2 = item2[0]
                p_name2 = item2[1]
                p_price2 = product_list[p_item][item2[1]]
                chose2.setdefault(index2, [p_name2, p_price2])
                print('%s \t%s\t%s ' % (index2, p_name2, p_price2))
            user_choice = input("[q=退出, c=购物车, b=返回 ] 请选择需要购买宝贝 :")

            if user_choice.isdigit() and int(user_choice) < len(product_list[p_item]):  # 选择宝贝 且在输入边界
                p_item = chose2[int(user_choice)][0]                         # 名字
                price = int(chose2[int(user_choice)][1])                     # 单价
                print('选择宝贝\033[32;1m[ %s ]\033[0m, 宝贝单价(元):\033[32;1m[ %s ]\033[0m' % (p_item, price))
                num = input('请输入购买数量：')

                if num.isdigit():
                    price_sum = int(num) * int(price)                                    # 计算金额：单价 * 购买数据量

                    # 检测余额
                    while salary_flag is not True:                                         # 余额不足，一直循环检查余额
                        if price_sum > int(salary):                                       # 余额不足
                            choice_pay = input('\033[31;1m余额不足，是否需要充值继续购买？(Y/N)：\033[0m')

                            if choice_pay == 'Y' or choice_pay == 'y':             # 充值调用充值函数
                                salary = pay_money(salary)
                                print('当前余额为：%d 宝贝价格为：%d' % (salary, price_sum))
                            elif choice_pay == 'N' or choice_pay == 'n':
                                print('\033[31;1m余额不足，本次购买失败！\033[0m')
                                break
                            else:
                                print('输入非法字符，请输入正确信息.！')

                        else:                                                    # 余额足

                            if not shopping_car.get(username):                    # 如果购物车中无数据，则赋值
                                shopping_car[username] = {p_item: [price, int(num), ]}
                            else:
                                shopping_car[username].setdefault(p_item, [price, int(num), ])  # 选择宝贝放入购物车 宝贝 ：【单价，数量，】
                                if not shopping_car_his.get(username):              # 如果无此帐号历史数据
                                    shopping_car_his.setdefault(username, {p_item: [price, int(num)]})
                                elif not shopping_car_his[username].get(p_item):  # 无此宝贝记录
                                    shopping_car_his[username].setdefault(p_item, [price, int(num), ])  # 购买宝贝数据插入
                                else:  # 如果存在购物车中,更新现有信息
                                    num1 = shopping_car_his[username][p_item][1] + int(num)  # 累加宝贝数量
                                    shopping_car_his[username][p_item][1] = num1  # 重新修改历史信息中的值
                                salary -= price_sum  # 扣款
                                salary_flag = True
                                print('宝贝\033[32;1m[%s]\033[0m ,单价:\033[32;1m[%d]\033[0m 数量:\033[32;1m[%d]\033[0m已加入购物车！'
                                      % (p_item, price, int(num)))
                                print('消费:\033[31;1m[%d]元\033[0m 余额为：\033[31;1m[%d]元\033[0m' % (price_sum, salary))

            elif user_choice == 'q' or user_choice == 'Q' or user_choice == 'quit':  # 退出
                show_shopping_car(shopping_car, username, salary)
                save_shopping_data(shopping_car, username, salary)
                print('Bye Bye!')
                exit_flag = True

            elif user_choice == 'c' or user_choice == 'C' or user_choice == 'check':  # 查看
                show_shopping_car(shopping_car, username, salary)

            elif user_choice == 'b' or user_choice == 'B':  # 返回
                pass

            else:
                print('输入非法字符,请输入正确信息！')

        elif user_choice == 'q' or user_choice == 'Q' or user_choice == 'quit':  # 退出
            show_shopping_car(shopping_car, username, salary)
            save_shopping_data(shopping_car, username, salary)
            print('Bye Bye!')
            exit_flag = True

        elif user_choice == 'c' or user_choice == 'C' or user_choice == 'check':      # 查看购物车
            show_shopping_car(shopping_car, username, salary)

        else:
            print('输入非法字符,请输入正确信息！')


if __name__ == '__main__':
    main()
