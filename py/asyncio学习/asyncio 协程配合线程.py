# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-01 16:53:55
@LastEditors: Even.Sand
@LastEditTime: 2020-03-02 16:33:12
'''
import inspect
import ctypes
import time
import asyncio
from threading import Thread


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def do_some_work(x):
    print(f'do_some_work Waiting {x}')
    await asyncio.sleep(x)
    print(f'do_some_work Done after {x}s')


def more_work(x):
    print(f'More work {x}')
    time.sleep(x)
    print('Finished more work {x}')


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


start = time.time()
# 主线程中创建一个 new_loop
new_loop = asyncio.get_event_loop()
# 创建子线程 在其中开启无限事件循环
t = Thread(target=start_loop, args=(new_loop,))
t.start()
print(f'TIME: {time.time() - start}')

# 在主线程中新注册协程对象
# 这样即可在子线程中进行事件循环的并发操作 同时主线程又不会被 block
# 一共执行的时间大概在 6 s 左右
asyncio.run_coroutine_threadsafe(do_some_work(6), new_loop)
asyncio.run_coroutine_threadsafe(do_some_work(4), new_loop)
time.sleep(7)
stop_thread(t)
# @不会停止，典型另开巡视协程
