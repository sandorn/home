# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-05 17:05:13
LastEditTime : 2023-01-05 17:05:51
FilePath     : /py学习/PY编程模式/Untitled-1类装饰器.py
Github       : https://github.com/sandorn/home
==============================================================
'''


# 定义一个类装饰器,装饰函数,默认调用__call__方法
class Decrator_call(object):

    def __init__(self, func):  # 传送的是test方法
        self.func = func

    def __call__(self, *args, **kwargs):  # 接受任意参数
        print('函数调用CALL')
        return self.func(*args, **kwargs)  # 适应test的任意参数


@Decrator_call  # 如果带参数,init中的func是此参数。
def test(hh):
    print('this is the test of the function !', hh)


test('hh')


# 定义一个类装饰器,装饰类中的函数,默认调用__get__方法
#    实际上把类方法变成属性了,类似：@property
class Decrator_get(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        '''
        instance:代表实例,sum中的self
        owner：代表类本身,Test类
        '''
        print('调用的是get函数')
        return self.func(instance)  # instance就是Test类的self


class Test(object):

    def __init__(self):
        self.result = 0

    @Decrator_get
    def sum(self):
        print('There is the Func in the Class !')


t = Test()
print(t.sum)  # 众所周知,属性是不加括号的,sum真的变成了属性
