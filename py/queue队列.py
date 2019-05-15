# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-13 08:46:17
@LastEditors: Even.Sand
@LastEditTime: 2019-05-13 09:36:25
'''

import queue
import threading


class Job(object):

    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('Job:', description)
        return

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)


que = queue.PriorityQueue()

que.put(Job(3, 'level 3 job'))
que.put(Job(10, 'level 10 job'))
que.put(Job(1, 'level 1 job'))


def process_job(que):
    while True:
        next_job = que.get()
        print('for:', next_job.description)
        que.task_done()


workers = [
    threading.Thread(target=process_job, args=(que,)),
    threading.Thread(target=process_job, args=(que,))
]

for w in workers:
    w.setDaemon(True)
    w.start()

#que.join()
'''python队列Queue - gxyz - 博客园
https://www.cnblogs.com/itogo/p/5635629.html'''
