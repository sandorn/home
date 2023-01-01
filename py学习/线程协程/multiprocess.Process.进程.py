# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-01 00:25:18
FilePath     : /py学习/线程协程/multiprocess.Process.进程.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import multiprocess


def do(n):
    # 获取当前线程的名字
    print("worker ", n)
    return print(n, "Process end.")


if __name__ == '__main__':
    numList = []
    for i in range(20):
        p = multiprocess.Process(target=do, args=(i, ))
        numList.append(p)
        p.start()
        p.join()
    print("All Process end.")
