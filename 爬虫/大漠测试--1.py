# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2021-04-14 16:26:25
FilePath     : /脚本/大漠测试--1.py
LastEditTime : 2021-04-21 12:27:57
Github       : https://github.com/sandorn/home
==============================================================
'''

import win32com.client

# dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件,获取大漠对象
# print(dm.ver())  # 输出版本号

import xt_Dm

dm = xt_Dm.dmobject().dm
print(dm.ver())  # 输出版本号
