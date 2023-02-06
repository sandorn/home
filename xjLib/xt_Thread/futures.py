# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-12-08 11:35:18
FilePath     : /xjLib/xt_Thread/futures.py
LastEditTime : 2022-10-22 11:07:45
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
from concurrent.futures import (ProcessPoolExecutor, ThreadPoolExecutor, as_completed)


def futuresMap(_cls):
    '''停用'''

    class FuturesMapCls(_cls):

        def __init__(self, func, *args_iter):
            super().__init__()
            self.future_generator = self.map(func, *args_iter)

        def wait_completed(self):
            '''等待线程池结束,返回全部结果,有序'''
            return list(self.future_generator)

        def getAllResult(self):
            '''等待线程池结束,返回全部结果,有序'''
            return self.wait_completed()

    FuturesMapCls.__name__ = _cls.__name__  # 保留原类的名字
    return FuturesMapCls


def futuresSub(_cls):
    '''停用'''

    class FuturesSubCls(_cls):

        def __init__(self, func, args_iter, callback=None, MaxSem=66):
            super().__init__()
            self.future_tasks = []

            for item in args_iter:
                task = self.submit(func, *item)
                self.future_tasks.append(task)
                if callback:
                    task.add_done_callback(callback)

        def getAllResult(self):
            '''as_completed等待线程池结束,返回全部结果,无序'''
            self.shutdown(wait=True)
            result_list = []
            for future in as_completed(self.future_tasks):  # 迭代生成器,统一结束'
                try:
                    resp = future.result()
                    result_list.append(resp)
                except Exception as err:
                    print('exception :', err)

            return result_list

        def wait_completed(self):
            '''等待线程池结束,返回全部有序结果'''
            self.shutdown(wait=True)
            result_list = []
            for future in self.future_tasks:
                try:
                    res = future.result()
                    result_list.append(res)
                except Exception as err:
                    print('exception :', err)
            return result_list

    FuturesSubCls.__name__ = _cls.__name__  # 保留原类的名字
    return FuturesSubCls


def futuresPool(_cls):

    class FuturesPoolCls(_cls):

        def __init__(self):
            super().__init__()
            self.future_tasks = []

        def add_map(self, func, *args_iter):
            self.future_generator = self.map(func, *args_iter)

        def add_sub(self, func, *args_iter, callback=None):
            for item in args_iter:
                task = self.submit(func, *item)
                self.future_tasks.append(task)
                if callback: task.add_done_callback(callback)

        def wait_completed(self):
            '''返回结果,有序'''
            if self.future_tasks: return self._wait_sub_completed()
            else: return self._wait_map_completed()

        def _wait_map_completed(self):
            '''返回结果,有序'''
            self.shutdown(wait=True)  # 新增
            return list(self.future_generator)

        def _wait_sub_completed(self):
            '''等待线程池结束,返回全部结果,有序'''
            self.shutdown(wait=True)
            result_list = []
            for future in self.future_tasks:
                try:
                    res = future.result()
                    result_list.append(res)
                except Exception as err:
                    print('exception :', err)
            return result_list

        def get_sub_result(self):
            '''获取结果,无序'''
            self.shutdown(wait=True)
            result_list = []
            for future in as_completed(self.future_tasks):  # 迭代生成器,统一结束'
                try:
                    resp = future.result()
                    result_list.append(resp)
                except Exception as err:
                    print('exception :', err)

            return result_list

    FuturesPoolCls.__name__ = _cls.__name__  # 保留原类的名字
    return FuturesPoolCls


# #使用类工厂,动态生成基于线程或进程的类

T_Map = futuresMap(ThreadPoolExecutor)  # 停用
P_Map = futuresMap(ProcessPoolExecutor)  # 停用
T_Sub = futuresSub(ThreadPoolExecutor)  # 停用
P_Sub = futuresSub(ProcessPoolExecutor)  # 停用
ThreadPool = futuresPool(ThreadPoolExecutor)
ProcessPool = futuresPool(ProcessPoolExecutor)


class FuncInThreadPool:
    '''将程序放到ThreadPoolExecutor中异步运行,返回结果'''

    def __init__(self, func, *args, **kwargs):
        self.future_list = self.result = []
        self.executor = ThreadPoolExecutor(32)
        self.func, self.args, self.kwargs = func, args, kwargs
        self.start()

    async def __work(self):
        __args = list(zip(*self.args))
        for arg in __args:
            task = self.loop.run_in_executor(self.executor, self.func, *arg, **self.kwargs)
            self.future_list.append(task)
        await asyncio.gather(*self.future_list)

        self.result = [fu.result() for fu in self.future_list]
        return self.result

    def start(self):
        self.loop = asyncio.get_event_loop()
        return self.loop.run_until_complete(self.__work())


if __name__ == '__main__':

    from xt_Requests import get_tretry

    res = FuncInThreadPool(get_tretry, ["http://httpbin.org/get"] * 3)
    print(res.result)
