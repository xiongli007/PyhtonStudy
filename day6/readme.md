###Author : xiongli

##需求描述：

**选课系统**

* 管理员：
* 创建老师：姓名、性别、年龄、资产
* 创建课程：课程名称、上课时间、课时费、关联老师
* 学生：用户名、密码、性别、年龄、选课列表[]、上课记录{课程1：【di,a,】}

1. 管理员设置课程信息和老师信息
2. 老师上课获得课时费
3. 学生上课，学到“上课内容”
4. 学生可自选课程
5. 学生可查看已选课程和上课记录
6. 学生可评价老师，差评老师要扣款
7. 使用pickle

##文档说明：
|项目   |内容   |路径 |
|-----  |-----  |------|
|使用说明书    |readme.md          |/day6/  |
|流程图        |选课系统.png        | /day6/  |
|主程序入口     |main.py             |/day6/bin/ |
|公共配置文件     |setting.py         |/day6/conf/ |
|管理员数据文件     |admin         |/day6/db/manager |
|用户数据文件     |xiongli         |/day6/db/student |
|课程数据文件     |course.pkl         |/day6/db/ |
|老师数据文件     |teacher.pkl        |/day6/db/ |
|学生数据文件     |student.pkl        |/day6/db/ |
|日志文件     |log.log        |/day6/log/ |
|日志模块程序     |log.py        |/day6/modules/ |
|功能模块程序     |manager.py        |/day6/modules/ |

##设计思路
    通过构建老师类、课程类、管理员类、学生类，
        把老师获得差评扣款、好评奖励方法写入老师类；
        把查看已选课程和上课记录、上课评价老师、可自选课程方法写入学生类；
        管理员类继承老师类、课程类，增加老师、删除老师、增加课程、登录等方法；
    然后，主程序再实例化以上类，通过菜单登录函数，进行功能实现；
        
##使用说明：
* 管理员入口：
```    
    管理员帐号/密码：admin/123 
    功能：【1】 新增老师
         【2】 查看老师信息
         【3】 删除老师
         【4】 增加课程
         【5】 返回上级 
```
* 学生入口：
```
    注册: 可自行根据提示输入相关信息，来新增学生帐号；
    登录:
    默认帐号/密码：xiongli/123，也可登陆注册帐号；
    功能：【1】 选课
         【2】 课程学习
         【3】 学习记录
         【4】 返回上级
```
    

##脚本执行方式：

* 调用python 执行 /day6/bin/main.py ，python /day6/bin/main.py
* 运行环境： python 3.x   