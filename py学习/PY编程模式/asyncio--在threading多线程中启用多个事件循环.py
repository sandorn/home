# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-16 14:12:34
FilePath     : /CODE/py学习/asyncio--在threading多线程中启用多个事件循环.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
import threading


def thread_loop_task(loop):

    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)

    async def work_1():
        i = 0
        while i < 4:
            print(f'work_1 on loop:{id(loop)}')
            i += 1
            await asyncio.sleep(0.01)

    async def work_2():
        i = 0
        while i < 6:
            print(f'work_2 on loop:{id(loop)}')
            i += 1
            await asyncio.sleep(0.01)

    future = asyncio.gather(work_1(), work_2())
    loop.run_until_complete(future)


def main():

    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()
    # 将thread_loop作为参数传递给子线程
    t = threading.Thread(target=thread_loop_task, args=(thread_loop, ))
    t.daemon = True
    t.start()

    async def main_work(main_loop):
        t.join()
        print(f'main on loop:{id(main_loop)}')
        await asyncio.sleep(0.2)

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main_work(main_loop))


if __name__ == '__main__':
    main()
