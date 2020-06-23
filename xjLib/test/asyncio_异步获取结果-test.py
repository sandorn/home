# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 20:15:43
#FilePath     : /xjLib/test/asyncio_异步获取结果-test.py
#LastEditTime : 2020-06-22 20:23:41
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import asyncio


def mark_done(future):
    fr = '程序运行结果!'
    print('in mark_done')
    future.set_result(fr)


def event(future):
    fr = 'event finished! '
    print('in event')
    future.set_result(fr)


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.call_soon(mark_done, all_done)
    result = event_loop.run_until_complete(all_done)
    print('returned result: {!r}'.format(result))
    all_done1 = asyncio.Future()
    event_loop.call_soon(event, all_done1)
    result = event_loop.run_until_complete(all_done1)

finally:
    print('closing event loop')
    event_loop.close()
print('future result: {!r}'.format(all_done1.result()))
