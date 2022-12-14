# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software :   VSCode
@File     :   语法糖.py
@Time     :   2019/05/07 17:45:26
@Author   :   Even Sand
@Version  :   1.0
@Contact  :   sandorn@163.com
@License  :   (C)Copyright 2009-2019, NewSea
python @property，@staticmethod及@classmethod内置装饰器小结 - 大魔王的博客 - CSDN博客
https://blog.csdn.net/weixin_43533825/article/details/87866909


详解闭包与装饰器， 99%的人看了这篇文章后就懂了 - 贯穿真Sh的博客 - CSDN博客
https://blog.csdn.net/ljt735029684/article/details/80703649

python装饰器详解 - xiangxianghehe的博客 - CSDN博客
https://blog.csdn.net/xiangxianghehe/article/details/77170585

一句话说清楚多个装饰器的执行顺序 - feilzhang的博客 - CSDN博客
https://blog.csdn.net/feilzhang/article/details/80402157

python装饰器：有参数的装饰器、不定长参数的装饰器、装饰有返回值的函数、通用的装饰器 - 有塔耶奥多的专栏 - CSDN博客
https://blog.csdn.net/yanhuatangtang/article/details/75213972
'''


class user(object):

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value == "":
            raise ValueError(u"名字不能为空")
        self._username = value


class demo(object):
    name = "test"

    def __init__(self, name):
        self.name = name

    def func(self, value):
        print("func running: " + value)

    @staticmethod
    def static_func(value):
        print("static_func running: " + value)

    @classmethod
    def class_func(cls, value):
        print("classmethod: " + cls.name + " " + value)


def bread(func):

    def wrapper():
        print("</''''''\>")
        func()
        print("<\______/>")

    return wrapper


def ingredients(func):

    def wrapper():
        print("#tomatoes#")
        func()
        print("~salad~")

    return wrapper


@bread
@ingredients
def sandwich(food="--ham--"):
    print(food)


#带有不定参数的装饰器
import time


def deco01(func):

    def wrapper(*args, **kwargs):
        print("this is deco01")
        startTime = time.time()
        func(*args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime) * 1000
        print("time is %d ms" % msecs)
        print("deco01 end here")

    return wrapper


def deco02(func):

    def wrapper(*args, **kwargs):
        print("this is deco02")
        func(*args, **kwargs)

        print("deco02 end here")

    return wrapper


@deco01
@deco02
def func(a, b):
    print("hello，here is a func for add :")
    time.sleep(1)
    print("result is %d" % (a + b))


def dec1(func):
    print("1111")

    def one():
        print("2222")
        func()
        print("3333")

    return one


def dec2(func):
    print("aaaa")

    def two():
        print("bbbb")
        func()
        print("cccc")

    return two


@dec1
@dec2
def test():
    print("test test")


if __name__ == '__main__':
    test()
    f = func
    f(3, 4)
    sandwich()
    #类初始化
    a = demo("demotest")

    #实例调用方法
    a.static_func("实例调用方法statcimethod")
    a.class_func("实例调用方法classmethod")
    a.func("normalmethod")
    #类调用方法
    demo.static_func("类调用方法staticmethod")
    demo.class_func("类调用方法classmethod")

    #绑定对象
    print(a.func)
    print(a.static_func)
    print(a.class_func)

    print(demo.static_func)
    print(demo.class_func)

    demo1 = user()
    demo1.username = "新名字"
    print(demo1.username)
    demo1.username = ''
    print(demo1.username)
