# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-21 17:54:35
LastEditTime : 2024-06-21 17:54:41
FilePath     : /CODE/py学习/线程协程/process测试.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import time
from multiprocessing import Process, Semaphore


class MyProcess(Process):
    def __init__(self, arg, sem):
        self.arg = arg
        self.sem = sem
        self.run()

    def run(self):
        """
        重构run函数
        """
        with self.sem:
            print('nMask', self.arg)
            time.sleep(1)


if __name__ == '__main__':
    sem = Semaphore(3)  # 限制同时运行的进程数量为3
    processes = []
    for i in range(10):
        processes.append(MyProcess(i, sem))
    for p in processes:
        p.join()
