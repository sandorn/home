# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-12 23:09:13
LastEditTime : 2022-12-12 23:09:14
FilePath     : /线程协程/基于Python3单进程+多线程(伪)+多协程的生产者-消费者模型示例代码.py
Github       : https://github.com/sandorn/home
==============================================================
基于Python3单进程+多线程(伪)+多协程的生产者-消费者模型示例代码_micromicrofat的博客-CSDN博客_python3协程 生产者消费者
https://blog.csdn.net/MacwinWin/article/details/113276604
'''
import asyncio
import time
from threading import Thread


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def create(timestamp, worker_pool, worker_loop):
    worker_pool[timestamp] = {}
    consumer_task = asyncio.run_coroutine_threadsafe(consumer(worker_pool, timestamp), worker_loop)
    timeout_task = asyncio.run_coroutine_threadsafe(timeout(worker_pool, timestamp), worker_loop)
    worker_pool[timestamp]['consumer'] = consumer_task
    worker_pool[timestamp]['timeout'] = timeout_task
    asyncio.run_coroutine_threadsafe(producer(worker_pool, timestamp), worker_loop)


async def producer(worker_pool, timestamp):
    await worker_pool[timestamp]['mq'].put(timestamp)


async def consumer(worker_pool, timestamp):
    worker_pool[timestamp]['mq'] = asyncio.Queue()
    while True:
        await worker_pool[timestamp]['mq'].get()
        worker_pool[timestamp]['timeout'].cancel()
        worker_pool.pop(timestamp)
        break


async def timeout(worker_pool, timestamp):
    await asyncio.sleep(10)
    worker_pool[timestamp]['consumer'].cancel()
    worker_pool.pop(timestamp)


if __name__ == "__main__":
    worker_loop = asyncio.new_event_loop()
    loop_thread = Thread(target=start_loop, args=(worker_loop, ))
    loop_thread.daemon = True
    loop_thread.start()
    worker_pool = {}

    count = 0
    start = time.time()
    while True:
        if time.time() - start > 1:
            start = time.time()
            print(count)
            count = 0
        count += 1
        timestamp = str(time.time())
        create(timestamp, worker_pool, worker_loop)
        print(f'-------- {len(worker_pool)}', end='\r', flush=True)
