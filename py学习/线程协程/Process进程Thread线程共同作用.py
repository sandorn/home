# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-31 19:46:27
LastEditTime : 2022-12-31 19:46:28
FilePath     : /py学习/线程协程/Process进程Thread线程共同作用.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import multiprocessing
import os
import threading


# worker function
def worker(sign=None, t_lock=None):
    if t_lock is None: t_lock = threading.Lock()
    with t_lock:
        print(sign, os.getpid())


def thread_main():
    # Main
    print('Main:', os.getpid())

    # Multi-thread
    record = []
    threading_lock = threading.Lock()
    for _ in range(5):
        thread = threading.Thread(target=worker, args=('thread', threading_lock))
        thread.start()
        record.append(thread)

    for thread in record:
        thread.join()


def process_main():
    # Multi-process
    record = []
    process_lock = multiprocessing.Lock()
    for _ in range(5):
        process = multiprocessing.Process(target=worker, args=('process', process_lock))
        process.start()
        record.append(process)

    for process in record:
        process.join()


if __name__ == '__main__':
    thread_main()
    process_main()
