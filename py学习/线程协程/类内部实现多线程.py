# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-27 23:20:54
LastEditTime : 2022-12-27 23:20:55
FilePath     : /py学习/线程协程/类内部实现多线程.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading
import time
from threading import Thread

from xt_Time import fn_timer


class A(object):

    def __init__(self):
        self.a = 0
        self.b = 0

    def get_num_a(self, num):
        time.sleep(0.1)
        self.a = num

    def get_num_b(self, num):
        time.sleep(0.1)
        self.b = num

    def sum(self):
        print(f"a的值为:{self.a},b的值为:{self.b}")
        return self.a + self.b

    def run(self, num):
        print(f'第2次层Thread:{num}')
        p1 = Thread(target=self.get_num_a, args=(num, ))
        p2 = Thread(target=self.get_num_b, args=(num, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print(f"合计：{self.sum()}")


class MyThread(Thread):

    def __init__(self, index):
        super().__init__()
        self.index = index

    def run(self):
        print(f'第1次层Thread:{ self.index}')
        for count in range(self.index):
            a = A()
            a.run(count)
            time.sleep(0.1)
            print(f'ident: {self.ident} Count: {count}')


if __name__ == '__main__':
    for i in range(10):
        p = MyThread(i)
        p.start()
