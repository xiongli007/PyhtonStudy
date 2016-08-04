**Author :** xiongli

**需求描述：**

三级菜单：
1. 运行程序输出第一级菜单
2. 选择一级菜单某项，输出二级菜单，同理输出三级菜单
3. 菜单数据保存在文件中


**脚本执行方式：**

调用python 执行 ThreeMenuv2.py ，python ThreeMenuv2.py

**文档说明：**

- 流程图： 三级菜单流程图v2.png
- 主程序：ThreeMenuv2.py
- 菜单信息：menu.json
- 运行环境： Python3.x


**维护方法**：

1、增加菜单名字信息到文件 test.json 中；
    格式为：
    {'省'：
            {'市':
                ['县']
            }
        }
    
