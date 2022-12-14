# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-30 22:17:14
FilePath     : /线程协程/python多线程限制并发数示例.py
LastEditTime : 2022-11-30 22:17:15
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading
import time
from queue import Queue

prolock = threading.Lock()

# 定义同时队列数
queue = Queue(maxsize=10)

# 定义任务初值值及最大值
taskidx = 0
maxidx = 2


# 生成任务列表
def taskList():
    task = []
    for i in range(10):
        task.append("task" + str(i))
    return task


# 把任务放入队列中
class Producer(threading.Thread):

    def __init__(self, name, queue):
        self.__name = name
        self.__queue = queue
        super(Producer, self).__init__()

    def run(self):
        while True:
            global taskidx, prolock, maxidx
            time.sleep(4)
            prolock.acquire()
            print('Producer name: %s' % (self.__name))
            if maxidx == taskidx:
                prolock.release()
                break
            ips = taskList()
            ip = ips[taskidx]
            self.__queue.put(ip)
            taskidx = taskidx + 1
            prolock.release()


# 线程处理任务
class Consumer(threading.Thread):

    def __init__(self, name, queue):
        self.__name = name
        self.__queue = queue
        super(Consumer, self).__init__()

    def run(self):
        while True:
            ip = self.__queue.get()
            print('Consumer name: %s' % (self.__name))
            consumer_process(ip)
            self.__queue.task_done()


def consumer_process(ip):
    time.sleep(1)
    print(ip)


def startProducer(thread_num):
    t_produce = []
    for i in range(thread_num):
        p = Producer("producer" + str(i), queue)
        p.setDaemon(True)
        p.start()
        t_produce.append(p)
    return t_produce


def startConsumer(thread_num):
    t_consumer = []
    for i in range(thread_num):
        c = Consumer("Consumer" + str(i), queue)
        c.setDaemon(True)
        c.start()
        t_consumer.append(c)
    return t_consumer


def main():
    t_produce = startProducer(3)
    t_consumer = startConsumer(5)

    # 确保所有的任务都生成
    for p in t_produce:
        p.join()

    # 等待处理完所有任务
    queue.join()


if __name__ == '__main__':
    main()
    print('------end-------')
