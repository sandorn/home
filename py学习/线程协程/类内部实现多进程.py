# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-27 20:53:19
FilePath     : /py学习/线程协程/类内部实现多进程.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import multiprocessing
import time
from multiprocessing import Process

from xt_Time import fn_timer


class A(object):

    def __init__(self):
        self.a = None
        self.b = None
        # 初始化一个共享字典
        self.my_dict = multiprocessing.Manager().dict()

    def get_num_a(self, num):
        time.sleep(0.1)
        self.my_dict["a"] = num

    def get_num_b(self, num):
        time.sleep(0.1)
        self.my_dict["b"] = num

    def sum(self):
        self.a = self.my_dict["a"]
        self.b = self.my_dict["b"]
        print(f"a的值为:{self.a}")
        print(f"b的值为:{self.b}")
        return self.a + self.b

    def run(self, num):
        p1 = multiprocessing.Process(target=self.get_num_a, args=(num, ))
        p2 = multiprocessing.Process(target=self.get_num_b, args=(num, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print(self.sum())


@fn_timer
def main(num):
    a = A()
    a.run(num)


class MyProcess(Process):

    def __init__(self, index):
        super().__init__()
        self.index = index

    def run(self):
        for count in range(self.index):
            main(count)
            time.sleep(0.1)
            print(f'Pid: {self.pid} Count: {count}')


if __name__ == '__main__':
    for i in range(10):
        p = MyProcess(i)
        p.start()
