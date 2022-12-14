# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : 动态添加协程任务
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-29 11:06:20
#FilePath     : /asyncio学习/主副线程动态添加协程任务.py
#LastEditTime : 2020-06-29 11:15:08
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import asyncio
from threading import Thread


async def create_task(event_loop, maxi=10):
    # #非此处决定不停循环
    i = 0
    while i < maxi:
        # 每秒产生一个任务, 提交到线程里的循环中, event_loop作为参数
        asyncio.run_coroutine_threadsafe(production(i), event_loop)
        await asyncio.sleep(1)
        i += 1


async def production(i):
    while True:
        print("第{}个coroutine任务".format(i))
        await asyncio.sleep(1)


def start_loop(loop):
    #  运行事件循环， loop作为参数
    asyncio.set_event_loop(loop)
    loop.run_forever()


thread_loop = asyncio.new_event_loop()  # 创建事件循环
# 新起线程运行事件循环, 防止阻塞主线程
run_loop_thread = Thread(target=start_loop, args=(thread_loop, ))
run_loop_thread.start()  # 运行线程，即运行协程事件循环

main_loop = asyncio.new_event_loop()
main_loop.run_until_complete(create_task(thread_loop))
# 主线程负责create coroutine object
