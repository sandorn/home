# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-06 21:43:59
LastEditTime : 2023-02-06 21:44:19
FilePath     : /CODE/py学习/廖雪峰python教程/切片习题.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def trim(s):
    if len(s) == 0: return s
    if s[0] == ' ': return trim(s[1:])
    return trim(s[:-1]) if s[-1] == ' ' else s


if trim('hello  ') != 'hello':
    print('1测试失败!')
elif trim('  hello') != 'hello':
    print('2测试失败!')
elif trim('  hello  ') != 'hello':
    print('3测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('4测试失败!')
elif trim('') != '':
    print('5测试失败!')
elif trim('    ') != '':
    print('6测试失败!')
else:
    print('测试成功!')
