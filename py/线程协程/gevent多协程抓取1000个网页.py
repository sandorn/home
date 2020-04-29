# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-12 10:23:19
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 10:27:14
'''
import time

import gevent
import requests
from gevent import monkey
from gevent.queue import Queue

monkey.patch_all()

link_list = []
with open('alexa.txt', 'r', encoding='utf-8') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n', '')
        link_list.append(link)

start = time.time()


def crawler(index):
    Process_id = 'Process-' + str(index)
    while not workQueue.empty():
        url = workQueue.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print(Process_id, workQueue.qsize(), r.status_code, url)
        except Exception as e:
            print(Process_id, workQueue.qsize(), url, 'Error:', e)


def boss():
    for url in link_list:
        workQueue.put_nowait(url)


if __name__ == '__main__':
    workQueue = Queue(100)

    gevent.spawn(boss).join()
    jobs = []
    for i in range(10):
        jobs.append(gevent.spawn(crawler, i))
    gevent.joinall(jobs)

    end = time.time()
    print('gevent + Queue :', end - start)
    print('Main Ended!')
