# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-24 08:58:48
LastEditTime : 2022-12-24 08:58:49
FilePath     : /py学习/PY编程模式/回调1.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from xt_Time import fn_timer


#回调函数1
def double(x):
    return x * 2


#回调函数2
def quadruple(x):
    return x * 4


#中间函数
def getOddNumber(k, getEvenNumber):
    return 1 + getEvenNumber(k)


#起始函数，主函数
@fn_timer
def main():
    k = 1
    #当需要生成一个2k+1形式的奇数时
    i = getOddNumber(k, double)
    print(i)
    #当需要一个4k+1形式的奇数时
    i = getOddNumber(k, quadruple)
    print(i)
    #当需要一个8k+1形式的奇数时
    i = getOddNumber(k, lambda x: x * 8)
    print(i)


def apply_async(func, args, callback):
    """
    func 函数的是处理的函数
    args 表示的参数
    callback 表示的函数处理完成后的 该执行的动作
    """
    result = func(*args)
    callback(result)


def add(x, y):
    return x + y


def print_result(result):
    print(result)


class 回调类(object):

    def __init__(self):
        self.sequence = 0

    def handle(self, result):
        self.sequence += 1
        print("[{}] 类   Got:{}".format(self.sequence, result))


def 闭包():
    sequence = 0

    def handler(result):
        nonlocal sequence
        sequence += 1
        print("[{}] 闭包 Got:{}".format(sequence, result))

    return handler


def 协程():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print("[{}] 协程 Got:{}".format(sequence, result))


# 定义类
class Demo():

    def foo(self, num):
        return self.callback_func(num)

    # 定义修饰器
    def callback(self, func):
        self.callback_func = func


demo = Demo()
demo2 = Demo()


# 注册回调函数1
@demo.callback
def double(x):
    print("double", 2 * x)
    return 2 * x


# 注册回调函数2
@demo2.callback
def inserve(x):
    print('inserve', -x)
    return -x


if __name__ == "__main__":
    # main()
    #############################################################
    # apply_async(add, (123, 456), callback=print_result)
    #############################################################
    # resultHandler = 回调类()
    # apply_async(add, (123, 456), callback=resultHandler.handle)
    #############################################################
    # handler = 闭包()
    # apply_async(add, (123, 456), callback=handler)
    #############################################################
    # handle = 协程()
    # next(handle)
    # apply_async(add, (123, 456), callback=handle.send)
    # apply_async(add, (77, 2631), callback=handle.send)
    #############################################################
    # demo.foo(3)  # 6
    # demo2.foo(3)  # -3
