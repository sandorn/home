# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 20:15:43
#FilePath     : /asyncio学习/asyncio_异步获取结果-test.py
#LastEditTime : 2020-06-28 18:27:26
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import asyncio


def mark_one(future):
    fr = 'mark_one运行结果!'
    print('in mark_one')
    future.set_result(fr)


def mark_two(future):
    fr = 'mark_two result'
    print('in mark_two')
    future.set_result(fr)


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.call_soon(mark_one, all_done)
    result = event_loop.run_until_complete(all_done)
    print('returned result: {!r}'.format(result))
    all_done1 = asyncio.Future()
    event_loop.call_soon(mark_two, all_done1)
    result = event_loop.run_until_complete(all_done1)

finally:
    print('closing event loop')
    event_loop.close()
print('future result: {!r}'.format(all_done1.result()))
