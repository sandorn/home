# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-29 10:37:30
#FilePath     : /asyncio学习/loop.run_in_executor在线程或者进程池中执行代码.py
#LastEditTime : 2020-06-29 10:52:00
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import asyncio
import concurrent.futures


def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('README.md', 'r', encoding='UTF-8') as f:
        return f.read()


def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10**7))


async def main():
    loop = asyncio.get_running_loop()

    # # Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print('default thread pool:\n', result)

    # 2. Run in a custom thread pool:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_io)
        print('custom thread pool:\n', result)

    # 3. Run in a custom process pool:
    # !此处出现错误
    # with concurrent.futures.ProcessPoolExecutor() as mypool:
    #     result = await loop.run_in_executor(mypool, cpu_bound)
    #     print('custom process pool:\n', result)


asyncio.run(main())
