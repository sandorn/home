# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-25 15:07:21
FilePath     : /py学习/PY编程模式/metaclass.py
Github       : https://github.com/sandorn/home
==============================================================
'''


class MyMeta(type):

    def __new__(cls, *args, **kwargs):
        print(1)
        print(cls)
        print('===>MyMeta.__new__')
        print(cls.__name__)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, classname, superclasses, attributedict):
        super().__init__(classname, superclasses, attributedict)
        print(self)
        print('===>MyMeta.__init__')
        print(self.__name__)
        print(classname)
        print(superclasses)
        print(attributedict)
        print(self.tag)
        print(2)

    def __call__(self, *args, **kwargs):
        print('===>MyMeta.__call__')
        print(self)
        obj = self.__new__(self, *args, **kwargs)
        self.__init__(self, *args, **kwargs)
        print(3)
        return obj

    def aaa(self):
        print('aaa')
        print(self)
        print(4)


class Foo(object, metaclass=MyMeta):
    tag = '!Foo'
    print(5)

    def __new__(cls, *args, **kwargs):
        print('===>Foo.__new__')
        print(6)
        print(cls)
        return super().__new__(cls)

    def __init__(self, name):
        print(self)
        print('===>Foo.__init__')
        self.name = name
        print(7)


print('test start')
foo = Foo('test')
foo.aaa()  # 'Foo' object has no attribute 'aaa'
print('test end')
