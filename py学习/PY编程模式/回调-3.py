# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-25 21:10:49
LastEditTime : 2022-12-25 21:10:50
FilePath     : /py学习/PY编程模式/回调-3.py
Github       : https://github.com/sandorn/home
==============================================================
'''

# 验证 call back 回调函数
import random
from functools import reduce


def clean_data(input_list):
    # 对列表元素四舍五入
    xlist = list(map(lambda x: round(x), input_list))
    # 对列表元素过滤
    xlist = list(filter(lambda x: x > 10 and x < 65535, xlist))
    print("回调函数处理后列表长度:", len(xlist))
    return xlist


def total(data, cb):
    # 调用回调函数
    cb_data = cb(data)
    return reduce(lambda x, y: x + y, cb_data)


demo_data = [random.uniform(1, 70000) for i in range(0, 100)]
print("原始列表长度:", len(demo_data))
print("列表数值总和： ", total(demo_data, clean_data))
