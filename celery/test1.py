# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-20 13:43:59
@LastEditors: Even.Sand
@LastEditTime: 2020-03-20 14:21:59
'''


from tasks import add  # 导入tasks模块

re = add.delay(10, 20)
print(re.result)  # 获取结果
print(re.ready)  # 是否处理
print(re.get(timeout=1))  # 获取结果
print(re.status)  # 是否处理
