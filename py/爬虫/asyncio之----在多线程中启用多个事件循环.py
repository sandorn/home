# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 22:46:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-06 09:59:52
'''
import asyncio
import threading


def thread_loop_task(loop):

    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)

    async def work_2():
        i = 0
        while i < 20:
            print('work_2 on loop:%s' % id(loop))
            i += 2
            await asyncio.sleep(2)

    async def work_4():
        i = 0
        while i < 20:
            print('work_4 on loop:%s' % id(loop))
            i += 2
            await asyncio.sleep(4)

    future = asyncio.gather(work_2(), work_4())
    loop.run_until_complete(future)


if __name__ == '__main__':

    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()

    # 将thread_loop作为参数传递给子线程
    t = threading.Thread(target=thread_loop_task, args=(thread_loop,))
    t.daemon = True
    t.start()

    main_loop = asyncio.get_event_loop()

    async def main_work():
        t.join()
        print('main on loop:%s' % id(main_loop))
        await asyncio.sleep(4)

    main_loop.run_until_complete(main_work())
