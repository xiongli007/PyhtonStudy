###Author : xiongli

##需求描述：

**配置文件修改：**

* 公司有haproxy配置文件，希望通过python程序可以对ha配置文件进行增删改，不再是以往的打开文件进行直接操作了。
*   输出：
*       1、获取ha记录
        2、增加ha记录
        3、删除ha记录
*    如果用户输入: 1:

        让用户输入backed: 如果用户输入: www.oldboy.org
        将配置文件中的backed www.oldboy.org节点下的所有记录全部取到,并打印出来;

*    如果用户输入backed 2:
 
        提示用户输入要增加的backed信息,如{"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}

*    如果用户输入序列: 3:

        提示用户输入要删除的backed, 如 {"backend": "test.oldboy.org","record":{"server": "100.1.7.9","weight": 20,"maxconn": 30}}

* （可选）如果backend下所有的记录都已经被删除，那么将当前 backend test.oldboy.org 也删除掉。


##脚本执行方式：

* 调用python 执行 haproxy.py ，python haproxy.py
* 运行环境： python 3.x


##文档说明：
|项目   |内容   |路径 |
|-----  |-----  |------|
|使用说明书    |readme.md          |/day3/  |
|流程图        |haproxy.pdf        | /day3/  |
|主程序        |haproxy.py         |/day3/ |
|python数据文件 |ha.conf           |/day3/ |

##设计思路
功能描述/思路整理:
    首先循环打印一个选择菜单,供用户选择:
*       1、获取ha记录
            提示用户输入一个backend, 而后遍历整个文件,从用户输入的backend开始到下一个backend结束循环,
            或是文件结束循环（即目标backend位于最后）,而后把值放入一个列表，判断列表个数和标示，把列表、
            有无backend信息和有无配置内容return给主函数, 在主函数里判断后打印相应情况。
        
        2、增加ha记录
            提示用户输入一个字典类型的值,用json转换类型,而后分别赋给不同的变量,调用第1点函数，获取输入信
            息情况；先进行文件备份；循环遍历整个配置文件,同时打开新文件；
            
            1）配置文件中无backend信息：在循环完整个配置文件后，新文件再插入输入的backend服务及配置信息；
            
            2）配置文件中有backend信息：当用户输入的backend开始到下一个backend结束循环或是文件结束循环
              （即目标backend位于最后），把用户输入的配置信息插入新文件中；
            
            以上完成后，新文件重命名为ha.conf。
            
        3、删除ha记录
            提示用户输入一个字典类型的值,用json转换类型,而后分别赋给不同的变量,调用第1点函数，获取输入信
            息情况；先进行文件备份；校验需删除的配置是否为该backend服务唯一配置，并设置del_backend；循
            环遍历整个配置文件,同时打开新文件；
            
            1）配置文件中无backend信息：不做操作；

            2）配置文件中有backend信息：当用户输入的backend开始，del_backend=True，则该条数据(包含backend)
            不写入新文件; 不是唯一配置时，匹配输入配置时，不写入新文件；代表删除此记录。 
            
            以上完成后，新文件重命名为ha.conf。
            

##使用说明：

*   选择新增/删除操作时，输入格式需按{"backend": "buy.oldboy.org","record":{"server": "100.1.7.90","weight": 20,"maxconn": 3000}}
    输入。
