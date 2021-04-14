# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
symbol_custom_string_obkoro1: ==============================================================
Descripttion : None
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2021-04-14 16:26:25
FilePath     : /脚本/大漠版本号查询--1.py
LastEditTime : 2021-04-14 18:07:48
Github       : https://github.com/sandorn/home
#==============================================================
'''

import win32com.client

dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件,获取大漠对象


print(dm.ver())  # 输出版本号
