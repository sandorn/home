# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-12 16:05:58
#FilePath     : /xjLib/test/class--test.py
#LastEditTime : 2020-06-18 16:20:14
#Github       : https://github.com/sandorn/home
#==============================================================
8.9 创建新的类或实例属性_w3cschool
https://www.w3cschool.cn/youshq/ciy5nozt.html
Python3.7 dataclass使用指南 - apocelipes - 博客园
https://www.cnblogs.com/apocelipes/p/10284346.html

'''

from dataclasses import dataclass
from functools import partial

from pysnooper import snoop

from xt_Class import readonly, typeassert, typed_property, Class_Meta, item_MixIn, attr_MixIn, iter_MixIn, repr_MixIn, dict_MixIn
from xt_Log import log
from xt_String import class_to_dict
log = log()
snooper = snoop(log.filename)
# print = log.debug

from dataclasses import dataclass


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,(list,tuple)):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def setparams(self, attr, value):
    # #设置参数，更新body_dict
    self.__setattr__(attr, value)

    if attr in self.body_dict.keys():
        self.body_dict[attr] = value


def example1():
    # String = partial(typed_property, expected_type=str)
    Integer = partial(typed_property, expected_type=int)

    class Person:
        name = typed_property('name', str)
        age = Integer('age')

        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return "Person [name={}, age={}]".format(self.name, self.age)

    a = Person('张三', 44)
    a.name = '二狗子'
    print(a)


def example2():
    '''只能限制类型'''
    @typeassert(name=str, shares=int, price=float)
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

        def __repr__(self):
            return f"{self.__class__.__name__}('name': '{self.name}', 'shares': '{self.shares}', 'price': '{self.price}')"

    zsy = Stock('中国石油', 600987, 4.02)
    print(zsy)
    zsy.shares = 260987
    zsy.price = 48.32
    zsy.name = '中国石化'
    print(zsy)
    print(zsy.__dict__)
    print(dir(zsy))


def example3():
    class Stock:
        __slots__ = ('__name', '__shares', 'price')
        name = readonly('_Stock__name')
        shares = readonly('_Stock__shares')

        def __init__(self, name, shares, price):
            self.__name = name
            self.__shares = shares
            self.price = price

        def __repr__(self):
            return f"{self.__class__.__name__}('name': '{self.name}', 'shares': '{self.shares}', 'price': '{self.price}')"

        def _change_name(self, value):
            self.__name = value

    zsy = Stock('中国石油', 600987, 4.02)
    print(zsy)
    zsy.shares = 260987
    zsy.price = 48.32
    zsy._change_name('中国石化')
    print(zsy)
    # print(zsy.__dict__)  # 报错,__slots__影响
    print(dir(zsy))


def example4():
    @dataclass
    class Stock:
        name = readonly('_Stock__name')
        shares = readonly('_Stock__shares')
        __name: str = ''
        __shares: int = 600987
        price: float = 8.72

        def _change_name(self, value):
            self.__name = value

    zsy = Stock('中国石油', 600987, 4.02)
    print(zsy)
    zsy.shares = 260987
    zsy.price = 48.32
    zsy._change_name('中国石化')
    print(zsy)
    # print(zsy.__dict__) # 报错
    print(dir(zsy))


def example5():
    # #正常类,使用@property设置为只读
    class Stock:
        def __init__(self, name, shares, price):
            self.__name = name
            self.__shares = shares
            self.price = price

        @property
        def name(self):
            return self.__name

        def _change_name(self, value):
            self.__name = value

        @property
        def shares(self):
            return self.__shares

        def __repr__(self):
            return f"{self.__class__.__name__}('name': '{self.name}', 'shares': '{self.shares}', 'price': '{self.price}')"

    zsy = Stock('中国石油', 600987, 4.02)
    print(zsy)
    # zsy.shares = 260987 #报错
    zsy.price = 48.32
    zsy._change_name('中国石化')
    print(zsy)
    print(zsy.__dict__)
    print(dir(zsy))


def type_make_class():
    # # Class_Meta, item_MixIn, attr_MixIn, iter_MixIn, repr_MixIn
    objclass = type('Trick', (iter_MixIn, repr_MixIn), {
        'name': readonly('_name'),
        '_name': 'liuxinjun',
        'pass': '123456',
    })
    obj = objclass()
    print(obj.__dict__)
    obj._name = 'xuhuayin'
    print(class_to_dict(obj))
    for item in obj:
        print(item)
    print(obj)
    # print(dir(obj))


@snooper
def alispeech():
    from xt_Alispeech.conf import Constant

    @dataclass(init=False)
    class SpeechArgs:
        '''默认参数'''
        appkey = readonly('_appkey')
        token = readonly('_token')

        _appkey: str = Constant().appKey
        _token: str = Constant().token
        format: str = 'wav'
        sample_rate: int = 16000
        voice: str = 'Aida'
        volume: int = 100
        speech_rate: int = 0
        pitch_rate: int = 0

    a = SpeechArgs()
    print(a)
    class_to_dict(a)
    print(a.__dict__)
    for k in a.__dict__.items():
        print(k)
    # print(SpeechArgs.__mro__)


# example1()
# example2()
# example3()
# example4()
# example5()
# type_make_class()
alispeech()
