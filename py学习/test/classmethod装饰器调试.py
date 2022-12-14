# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-26 11:03:28
#FilePath     : \CODE\py\其他\classmethod装饰器调试.py
#LastEditTime : 2020-04-26 14:58:42
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#!list dict对象不赋值，改变其中的元素，可以用self、cls调用同一个类变量
#!数值型不可用，会生成新对象,需要@classmethod装饰
#!为其赋值，其实是创建了一个实例变量
#==============================================================
'''


class Something(object):
    a = []
    b = {}
    c = 1

    def __init__(self):
        # Something.b += 1
        print('init Something a:', Something.a, id(Something.a))
        print('init Something b:', self.b, id(self.b))

    def do(self):
        self.c += 1
        self.a.append(self.c)
        print('do self a:', self.a, id(self.a))

    @classmethod
    def dob(cls):
        cls.c += 1
        cls.b['doc' + str(cls.c)] = cls.c
        print('doc cls b:', cls.b, id(cls.b))

    def doc(self):
        self.c += 1
        print('doc self c:', self.c, id(self.c))


if __name__ == '__main__':
    something = Something()
    something.do()
    something.dob()
    something2 = Something()
    something2.do()
    something2.dob()
    something3 = Something()
    something3.do()
    something3.dob()
    something.dob()
    something2.dob()
    something3.dob()
    something.do()
    something2.do()
    something3.do()
    something.doc()
    something2.doc()
    something3.doc()
