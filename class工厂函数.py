# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-04 17:46:39
@LastEditors: Even.Sand
@LastEditTime: 2020-04-04 18:36:52
'''
from xjLib.db.sqlHelper import SqlHelper


def createClass(cls):
    class CustomizedClass(cls):
        pass
    return CustomizedClass


ClassList = createClass(list)
print(ClassList.__bases__)  # prints the parent class names for ClassList
instanceClassList = ClassList([1, 2, 3])  # object of ClassList created
print(instanceClassList)

ClassDict = createClass(dict)
print(ClassDict.__bases__)  # prints the parent class names for ClassDict
instanceClassDict = ClassDict({'a': 1, 'b': 2})  # object of ClassDict created
print(instanceClassDict)

ClassSql = createClass(SqlHelper)
print(ClassSql.__bases__)  # prints the parent class names for ClassList


'''
要动态创建一个class对象,type()函数依次传入3个参数：
1、class的名称，字符串形式；
2、继承的父类集合，注意Python支持多重继承，如果只有一个父类，注意tuple的单元素写法；
3、class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。
'''


def fn(self, name="world"):
    print("Hello,%s" % name)


Hello = type('Hello', (object,), dict(hello=fn))
h = Hello()
h.hello()
print(type(Hello))
print(type(h))


h2 = type('Hello', (object,), dict(hello=fn))()  # @简化
h2.hello()
print(type(h2))
