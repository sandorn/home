# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-02 00:39:11
LastEditTime : 2023-01-02 00:39:12
FilePath     : /py学习/线程协程/thread.local 类.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading
import time

from xt_Log import mylog

a = threading.local()


def worker():
    a.x = 0
    for _ in range(100):
        time.sleep(0.00001)
        a.x += 1

    mylog.print(f"{threading.current_thread()}, {a.x}")


for _ in range(3):
    threading.Thread(target=worker).start()
