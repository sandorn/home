# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-31 11:52:27
FilePath     : /py学习/线程协程/multiprocessing.Process多进程.py
Github       : https://github.com/sandorn/home
==============================================================
Python爬虫进阶六之多进程的用法 - 周小董 - CSDN博客
https://blog.csdn.net/xc_zhou/article/details/80823878
另外你还可以通过 cpu_count() 方法还有 active_children() 方法获取当前机器的 CPU 核心数量以及得到目前所有的运行的进程。
'''
import multiprocessing
import time
from multiprocessing import Lock, Process


def process(num):
    time.sleep(num / 10)
    print('Process:', num)


def main():
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i, ))
        p.start()

    print(f'CPU number:{str(multiprocessing.cpu_count())}')
    for p in multiprocessing.active_children():
        print(f'Child process name: {p.name} id: {str(p.pid)}')

    print('Process Ended')


class MyPro(Process):

    def __init__(self, index, lock):
        Process.__init__(self)
        self.index = index
        self.lock = lock
        self.result_list = []

    def run(self):
        for count in range(self.index):
            time.sleep(0.1)
            self.lock.acquire()
            print(f'Pid: {str(self.pid)} LoopCount: {str(count)}')
            self.result_list.append(count)
            self.lock.release()


def main_daemon():
    lock = Lock()
    for index in range(5):
        p = MyPro(index, lock)
        p.daemon = True
        p.start()
        p.join()
    print(p.result_list)
    print('Main process Ended!')


if __name__ == '__main__':
    # main()
    main_daemon()
