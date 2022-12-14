# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-26 12:33:37
#FilePath     : \CODE\py\其他\Python中的XOR异或符号^运用.py
#LastEditTime : 2020-04-26 13:22:35
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

a = 1
b = 3
print(a ^ b)


def singleNumber2(nums):
    r = 0
    for i in nums:
        print(i)
        r ^= i
        print(r)
    return r


# singleNumber2([1, 2, 3, 4, 7, 9, 20])
