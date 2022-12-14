# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : 关于metaclass，我原以为我是懂的 - xybaby - 博客园
https://www.cnblogs.com/xybaby/p/7927407.html
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-18 11:04:42
#FilePath     : /xjLib/test/metaclass-test-3.py
#LastEditTime : 2020-06-18 11:13:26
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import inspect


class RunImp(object):
    def run(self):
        print('just run')


class FlyImp(object):
    def fly(self):
        print('just fly')


class MetaMixin(type):
    def __init__(cls, name, bases, dic):
        super(MetaMixin, cls).__init__(name, bases, dic)
        member_list = (RunImp, FlyImp)

        for imp_member in member_list:
            if not imp_member:
                continue

            for method_name, fun in inspect.getmembers(imp_member,
                                                       inspect.ismethod):
                print('class %s get method %s from %s' %
                      (name, method_name, imp_member))
                assert not hasattr(cls, method_name), method_name
                setattr(cls, method_name, fun.im_func)


class Bird(metaclass=MetaMixin):
    pass


class Bird2(RunImp, FlyImp):
    pass


class DummyMetaIMixin(MetaMixin):
    def __init__(cls, name, bases, dic):
        type.__init__(cls, name, bases, dic)


class SpecialBird(Bird, metaclass=DummyMetaIMixin):
    def run(self):
        print('SpecialBird run')

    pass


a = Bird2()
print(dir(a))
a.run()
a.fly()

b = SpecialBird()
b.run()
b.fly()
