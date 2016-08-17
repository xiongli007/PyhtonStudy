Author : xiongli

需求描述：
     模拟登陆：

1. 用户输入帐号密码进行登陆
2. 用户信息保存在文件内
3. 用户密码输入错误三次后锁定用户


文档说明：
1、流程图： SimulatedLoginIn.png
2、主程序：SimulatedLoginIn.py
3、用户和密码文件：UserMsg.txt 
4、帐号加锁文件：lock.txt
5、运行环境： Python3.x

脚本执行方式：
调用SimulatedLoginIn.py执行 ，python SimulatedLoginIn.py


账号：
	文件UserMsg.txt以“|”符号做分隔符，分别为：帐号、密码、锁定次数(每次运行初始化为0)；
	默认账号有：xiongli,oldboy,xx,aa
	如需添加帐号，请按以上格式添加相关信息；

