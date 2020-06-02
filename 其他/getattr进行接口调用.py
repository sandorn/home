# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 15:04:05
@LastEditors: Even.Sand
@LastEditTime: 2020-03-25 15:06:55
'''


from math import pi


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    def getArea(self):
        return round(pow(self.radius, 2) * pi, 2)


class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height


# 定义统一接口
def func_area(obj):
    # 获取接口的字符串
    for get_func in ['get_area', 'getArea']:
        # 通过反射进行取方法
        func = getattr(obj, get_func, None)
        if func:
            return func()


if __name__ == '__main__':
    c1 = Circle(5.0)
    r1 = Rectangle(4.0, 5.0)

    # 通过map高阶函数，返回一个可迭代对象
    erea = map(func_area, [c1, r1])
    print(list(erea))
