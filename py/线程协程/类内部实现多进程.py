# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-02 00:32:29
@LastEditors: Even.Sand
@LastEditTime: 2020-04-02 00:38:27
python类内部实现多进程_Python_Damon_duanlei的博客-CSDN博客
https://blog.csdn.net/Damon_duanlei/article/details/88676632?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
'''


import multiprocessing
import time
from multiprocessing import Process


class A(object):
    def __init__(self):
        self.a = None
        self.b = None
        # 初始化一个共享字典
        self.my_dict = multiprocessing.Manager().dict()

    def get_num_a(self):
        time.sleep(3)
        self.my_dict["a"] = 10

    def get_num_b(self):
        time.sleep(5)
        self.my_dict["b"] = 6

    def sum(self):
        self.a = self.my_dict["a"]
        self.b = self.my_dict["b"]
        print("a的值为:{}".format(self.a))
        print("b的值为:{}".format(self.b))
        ret = self.a + self.b
        return ret

    def run(self):
        p1 = multiprocessing.Process(target=self.get_num_a)
        p2 = multiprocessing.Process(target=self.get_num_b)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print(self.sum())


def main1():
    t1 = time.time()
    a = A()
    a.run()
    t2 = time.time()
    print("cost time :{}".format(t2 - t1))


class MyProcess(Process):
    def __init__(self, loop):
        Process.__init__(self)
        self.loop = loop

    def run(self):
        for count in range(self.loop):
            time.sleep(1)
            print('Pid: ' + str(self.pid) + ' LoopCount: ' + str(count))


if __name__ == '__main__':
    for i in range(2, 5):
        p = MyProcess(i)
        p.start()
