# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:47
FilePath     : /py学习/print格式化.py
LastEditTime : 2022-11-13 18:28:03
Github       : https://github.com/sandorn/home
==============================================================
'''

import sys

print(sys.path)
"""
$ mkdir /home/miracle/libtest  # 建自己的库目录
$ gedit /home/miracle/libtest/test.py   # 编写库文件，内容如下

def testPrint():
    print("导入成功！")

######################### 写入*.pth文件
$ sudo gedit /usr/local/lib/python2.7/dist-packages/test.pth # 在默认的库路径中建立一个x.pth文件，写入内容如下:
/home/miracle/libtest

# 保存退出
######################### 查看目前的python库路径
$ python
>>> import sys
>>> sys.path

######################### 测试
$ python
>>> import test
>>> test.testPrint()

"""
