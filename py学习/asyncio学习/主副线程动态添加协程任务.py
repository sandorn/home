# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:36:04
LastEditTime : 2022-12-14 23:45:26
FilePath     : /py学习/asyncio学习/主副线程动态添加协程任务.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
from threading import Thread


async def create_task(event_loop, maxi=10):
    # #非此处决定不停循环
    i = 0
    while i < maxi:
        # 每秒产生一个任务, 提交到线程里的循环中, event_loop作为参数
        print(f"[create_task] 第{i}个任务")
        asyncio.run_coroutine_threadsafe(production(i), event_loop)
        await asyncio.sleep(1)
        i += 1


async def production(i):
    print(f"[production] 第{i}个coroutine任务")
    await asyncio.sleep(1)


def start_loop(loop):
    #  运行事件循环， loop作为参数
    asyncio.set_event_loop(loop)
    loop.run_forever()


thread_loop = asyncio.new_event_loop()  # 创建事件循环
# 新起线程运行事件循环, 防止阻塞主线程
_loop_thread = Thread(target=start_loop, args=(thread_loop, ))
_loop_thread.start()  # 运行线程，即运行协程事件循环
main_loop = asyncio.new_event_loop()
main_loop.run_until_complete(create_task(thread_loop))
# thread_loop.stop()
# main_loop.close()
