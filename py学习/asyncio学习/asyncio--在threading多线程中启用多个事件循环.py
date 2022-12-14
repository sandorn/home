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
@LastEditTime: 2020-03-13 15:28:04
'''
import asyncio
import threading


def thread_loop_task(loop):

    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)

    async def work_4():
        i = 0
        while i < 4:
            print('work_2 on loop:%s' % id(loop))
            i += 1
            await asyncio.sleep(0.2)

    async def work_6():
        i = 0
        while i < 6:
            print('work_4 on loop:%s' % id(loop))
            i += 1
            await asyncio.sleep(0.2)

    future = asyncio.gather(work_4(), work_6())
    loop.run_until_complete(future)


def main():

    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()
    # 将thread_loop作为参数传递给子线程
    t = threading.Thread(target=thread_loop_task, args=(thread_loop,))
    t.daemon = True
    t.start()

    async def main_work(main_loop):
        t.join()
        print('main on loop:%s' % id(main_loop))
        await asyncio.sleep(0.2)

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main_work(main_loop))


if __name__ == '__main__':
    main()
