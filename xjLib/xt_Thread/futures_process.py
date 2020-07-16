# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-25 22:57:00
#FilePath     : /xjLib/xt_Thread/futures_process.py
#LastEditTime : 2020-07-16 12:14:28
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from concurrent.futures import ProcessPoolExecutor  # 进程池模块
from concurrent.futures import as_completed


class ProcessPoolMap(ProcessPoolExecutor):
    def __init__(self, func, args_iter, MaxSem=6):
        super().__init__(max_workers=MaxSem)
        self.future_generator = self.map(func, args_iter)

    def wait_completed(self):
        '''等待线程池结束，返回全部结果，有序'''
        result_list = []
        for resp in self.future_generator:  # 此时将阻塞 , 直到线程完成或异常
            result_list.append(resp)
        return result_list

    def getAllResult(self):
        '''等待线程池结束，返回全部结果，有序'''
        return self.wait_completed()


class ProcessPoolSub(ProcessPoolExecutor):
    def __init__(self, func, args_iter, callback=None, MaxSem=6):
        super().__init__(max_workers=MaxSem)
        self.future_tasks = []

        for item in args_iter:
            task = self.submit(func, *item)
            self.future_tasks.append(task)
            if callback:
                task.add_done_callback(callback)

    def wait_completed(self):
        '''as_completed等待线程池结束，返回全部结果，无序'''
        self.shutdown(wait=True)
        result_list = []
        for future in as_completed(self.future_tasks):  # 迭代生成器,统一结束'
            try:
                resp = future.result()
                result_list.append(resp)
            except Exception as err:
                print('exception :', err)

        return result_list

    def getAllResult(self):
        '''等待线程池结束，返回全部有序结果'''
        self.shutdown(wait=True)
        result_list = []
        for future in self.future_tasks:
            try:
                res = future.result()
                result_list.append(res)
            except Exception as err:
                print('exception :', err)
        return result_list


class ExProcesPool(ProcessPoolExecutor):
    def __init__(self, MaxSem=6):
        super().__init__(max_workers=MaxSem)
        self.future_tasks = []

    def add_map(self, func, args_iter):
        self.future_generator = self.map(func, args_iter)

    def add_sub(self, func, args_iter, callback=None):
        '''submit方式添加任务，wait_completed结果无序'''
        for item in args_iter:
            task = self.submit(func, *item)
            self.future_tasks.append(task)
            if callback:
                task.add_done_callback(callback)

    def getAllResult(self):
        '''add_map返回结果，有序'''
        result_list = []
        for resp in self.future_generator:  # 此时将阻塞 , 直到线程完成或异常
            result_list.append(resp)
        return result_list

    def wait_completed(self):
        '''add_sub方式获取结果，无序'''
        self.shutdown(wait=True)
        result_list = []
        for future in as_completed(self.future_tasks):  # 迭代生成器,统一结束'
            # for future in self.future_tasks:
            try:
                resp = future.result()
                result_list.append(resp)
            except Exception as err:
                print('exception :', err)

        return result_list