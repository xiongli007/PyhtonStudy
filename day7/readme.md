###Author : xiongli

##需求描述：

**开发简单的FTP**

* 用户登陆
* 上传/下载文件
* 不同用户家目录不同
* 查看当前目录下文件
* 充分使用面向对象知识


##文档说明：

|项目   |内容   |路径 |
|-----  |-----  |------|
|使用说明书    |readme.md          |/day7/  |
|流程图        |ftp.png        | /day7/  |
|客户端主程序入口  |ftp.py         |/day7/bin |
|服务端主程序入口  |ftp_server.py  |/day7/bin |
|配置信息         |setting.py         |/day7/conf |
|商城消费数据     |login.pkl         |/day7/db |
|客户端模块     |client.py        |/day7/modules |
|服务端模块     |server.py        |/day7/modules |

##使用说明：
基于socket 实现简易FTP功能
* FTP帐号：
```
帐号/密码： 
        x1/123；
        ftp/123；
```
* FTP支持命令：
```
   查看当前目录下文件：ls
   上传文件：put 文件名（支持绝对路径）
   下载文件：get 文件名（支持绝对路径） 下载目标目录
   
```

##脚本执行方式：

客户端主程序：
```
* 执行 /day7/bin/ftp.py ，python /day7/bin/ftp.py
```
服务端主程序：
```
* 执行 /day7/bin/server.py.py ，python /day4/bin/server.py.py
```
运行环境： python 3.x
