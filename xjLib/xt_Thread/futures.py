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

import multiprocessing
from concurrent.futures import ProcessPoolExecutor  # @进程池模块,可添加
from concurrent.futures import ThreadPoolExecutor  # @线程池模块,不可添加
from concurrent.futures import as_completed

CPUNUM = multiprocessing.cpu_count()

# #futuresMap, futuresSub, futuresPool
# #T_Map, T_Sub, T_Pool,P_Map,P_Sub,P_Pool
# #使用类工厂,动态生成基于线程或进程的类


def futuresMap(_cls):

    class Class_Wrapper(_cls):

        def __init__(self, func, args_iter, MaxSem=66):
            if _cls.__name__ == "ProcessPoolExecutor": MaxSem = min(MaxSem, CPUNUM)
            super().__init__(max_workers=MaxSem)
            self.future_generator = self.map(func, args_iter)

        def wait_completed(self):
            '''等待线程池结束,返回全部结果,有序'''
            result_list = []
            for resp in self.future_generator:  # 此时将阻塞 , 直到线程完成或异常
                result_list.append(resp)
            return result_list

        def getAllResult(self):
            '''等待线程池结束,返回全部结果,有序'''
            return self.wait_completed()

    Class_Wrapper.__name__ = _cls.__name__  # 保留原类的名字
    return Class_Wrapper


def futuresSub(_cls):

    class Class_Wrapper(_cls):

        def __init__(self, func, args_iter, callback=None, MaxSem=66):
            if _cls.__name__ == "ProcessPoolExecutor": MaxSem = min(MaxSem, CPUNUM)
            super().__init__(max_workers=MaxSem)
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

    Class_Wrapper.__name__ = _cls.__name__  # 保留原类的名字
    return Class_Wrapper


def futuresPool(_cls):

    class class_wrapper(_cls):

        def __init__(self, MaxSem=66):
            if _cls.__name__ == "ProcessPoolExecutor": MaxSem = min(MaxSem, CPUNUM)
            # if MaxSem > 61 and _cls.__name__ == "ProcessPoolExecutor": MaxSem = CPUNUM
            super().__init__(max_workers=MaxSem)
            self.future_tasks = []

        def add_map(self, func, args_iter):
            self.future_generator = self.map(func, args_iter)

        def add_sub(self, func, args_iter, callback=None):
            for item in args_iter:
                task = self.submit(func, *item)
                self.future_tasks.append(task)
                if callback: task.add_done_callback(callback)

        def wait_completed(self):
            '''返回结果,有序'''
            if self.future_tasks: return self.wait_sub_completed()
            else: return self.wait_map_completed()

        def wait_map_completed(self):
            '''返回结果,有序'''
            result_list = []
            for resp in self.future_generator:  # 此时将阻塞 , 直到线程完成或异常
                result_list.append(resp)
            return result_list

        def wait_sub_completed(self):
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

    class_wrapper.__name__ = _cls.__name__  # 保留原类的名字
    return class_wrapper


T_Map = futuresMap(ThreadPoolExecutor)
P_Map = futuresMap(ProcessPoolExecutor)
T_Sub = futuresSub(ThreadPoolExecutor)
P_Sub = futuresSub(ProcessPoolExecutor)
ThreadPool = futuresPool(ThreadPoolExecutor)
ProcessPool = futuresPool(ProcessPoolExecutor)
