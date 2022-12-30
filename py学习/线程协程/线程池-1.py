# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-30 11:11:29
FilePath     : /py学习/线程协程/线程池-1.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import queue
import threading
from multiprocessing.dummy import Pool as ThreadPool  # 线程池

from xt_Thread import thread_print

que = queue.Queue()
que2 = queue.Queue()

for i in range(20, 30):
    que.put(i)

for i in range(40, 50):
    que2.put(i)


def job(*args):
    thread_print('args:', args, '\tthreading.current_thread:', threading.current_thread(), '\n')


if __name__ == '__main__':
    pool = ThreadPool(4)  # 创建一个包含4个线程的线程池
    #job_add_1 = partial(job, que.get())
    # while not que.empty():
    pool.map(job, zip(range(10), range(10, 20)))
    pool.close()  # 关闭线程池的写入
    pool.join()  # 阻塞，保证子线程运行完毕后再继续主进程
