# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-13 08:02:30
@LastEditors: Even.Sand
@LastEditTime: 2019-05-13 09:37:37

'''
from multiprocessing.dummy import Pool as ThreadPool  # 线程池
import threading
from functools import partial

import queue
que = queue.Queue()
que2 = queue.Queue()
for i in range(12):
    que.put(i)

for i in range(10, 100, 10):
    que2.put(i)


def job(*args):
    print(args, '\n', threading.current_thread())


if __name__ == '__main__':
    pool = ThreadPool(4)  # 创建一个包含4个线程的线程池
    #job_add_1 = partial(job, que.get())
    #while not que.empty():
    pool.map(job, zip(range(10), range(10, 20)))
    pool.close()  # 关闭线程池的写入
    pool.join()  # 阻塞，保证子线程运行完毕后再继续主进程
