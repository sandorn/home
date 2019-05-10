# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-09 17:05:09
@LastEditTime: 2019-05-09 17:06:56
'''


#使用装饰器计算函数运行时间
def trace(log_level):

    def impl_f(func):
        print(log_level, 'Implementing function: "{}"'.format(func.__name__))
        return func

    return impl_f


@trace('[INFO]')
def prg(*args, **kwargs):
    print(*args, **kwargs)


prg(2222222222222, 34, {1, 2, 3})
