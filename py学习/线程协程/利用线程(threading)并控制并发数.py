# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-27 23:26:35
FilePath     : /py学习/线程协程/利用线程(threading)并控制并发数.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import random
import threading  # multiprocessing
from queue import Queue
from time import sleep


# 下面是利用线程和queue队列的实现方法
# 继承一个Thread类，在run方法中进行需要重复的单个函数操作
class Test(threading.Thread):

    def __init__(self, queue=None, lock=None, num=None):
        # 传递一个队列queue和线程锁，并行数
        threading.Thread.__init__(self)
        self.queue = queue or Queue()
        self.lock = lock or threading.Lock()
        self.num = num or threading.Semaphore(3)

    def run(self):
        with self.num:  # 同时并行指定的线程数量，执行完毕一个则死掉一个线程
            # 以下为需要重复的单次函数操作
            n = self.queue.get()  # 等待队列进入
            lock.acquire()  # 锁住线程，防止同时输出造成混乱
            print('开始一个线程self.name：', self.name, '模拟的执行时间：', n)
            print('队列剩余：', queue.qsize())
            print('###########执行中的线程：', threading.active_count())  # , threading.enumerate())
            lock.release()
            sleep(n // 2)  # 执行单次操作，这里sleep模拟执行过程
            self.queue.task_done()  # 发出此队列完成信号


threads = []
queue = Queue()
lock = threading.Lock()
num = threading.Semaphore(3)  # 设置同时执行的线程数为3，其他等待执行


def aaa():
    for _ in range(10):
        t = Test(queue, lock, num)
        t.start()
        threads.append(t)

    for _ in threads:
        n = random.randint(1, 10)
        queue.put(n)
    # for t in threads:
    #     t.join()
    queue.join()  # 等待队列执行完毕才继续执行，否则下面语句会在线程未接受就开始执行


def yyy():
    for _ in range(30):
        thread = Test(queue, lock, num)
        thread.start()
        threads.append(thread)
        queue.put(random.randint(1, 10))

    # 等待线程执行完毕
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    aaa()
    print('aaa所有执行完毕')
    # yyy()
    # print('yyy所有执行完毕')
    print(threading.active_count(), threading.enumerate())
