# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-02 00:48:57
LastEditTime : 2023-01-13 21:47:12
FilePath     : /CODE/py学习/线程协程/multiprocessing面相对象的写法.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import multiprocessing
import os
import random
import time


def worker(que, delay):
    print(f'Parent Pid:{os.getppid()} | Pid: {os.getpid()} | {multiprocessing.current_process()}')
    time.sleep(random.randint(0, 4))
    que.put(f'{delay * 100}worker done!')


class MyProcess(multiprocessing.Process):

    all_Process = []  # 类属性或类变量,实例公用

    def __init__(self, func, *args, **kwargs):
        super(MyProcess, self).__init__()
        self.daemon = True
        self.target = func
        self.args = args
        self.kwargs = kwargs
        self.start()
        self.all_Process.append(self)

    def run(self) -> None:
        self.Result = self.target(*self.args, **self.kwargs)
        return self.Result


if __name__ == '__main__':
    que = multiprocessing.Queue()
    for i in range(1, 9):
        process = MyProcess(worker, que, delay=i)

    for process in MyProcess.all_Process:
        process.join()
    print([que.get() for _ in MyProcess.all_Process])
