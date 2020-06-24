# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 09:07:36
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-24 18:28:39
'''

__doc__ = [
    'SingletonThread',  # 单例
    'SingletonThread_Queue',
    'CustomThread',  # 继承线程
    'Custom_Thread_Queue',
    'NoResultsPending',  # 任务均已处理
    'NoWorkersAvailable',  # 无工作线程可用
    'WorkManager',  # 线程池管理，参照htreadpool编写的自定义库
    'Work',  # 线程池任务结构，参照htreadpool编写的自定义库
    'thread_pool_maneger',
    'WorkThread',  # 继承线程,利用queue；参照htreadpool编写的自定义库
    'my_pool',  # 装饰符方式
    'stop_thread',  # 外部停止线程
    'thread_wrap',  # 线程装饰器
    'thread_wraps',  # 线程装饰器,带参数
    'thread_wrap_class',  # 线程装饰器,获取结果
    'thread_wraps_class',  # 线程装饰器,带参数,获取结果
    'thread_safe',  # 线程安全锁，需要提供lock
]

import inspect
from threading import Lock, Thread, enumerate, main_thread
from time import sleep, time
from queue import Empty, Queue
from xt_Singleon import singleton_wrap_return_class
# #引入装饰器
from .wraps import thread_wrap_class, thread_wraps_class
from .wraps import thread_wraps, thread_wrap
from .wraps import thread_safe, print
# #引入自定义thread pool
from .Pool import WorkManager, thread_pool_maneger


def stop_thread(thread):
    import ctypes
    '''外部停止线程'''
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    _async_raise(thread.ident, SystemExit)


class thread_pool:
    '''
    仿写vthread
    @thread_pool(200)
    '''
    def __init__(self, pool_num=10):
        self._pool_queue = Queue()  # #任务存储,组内queue
        self.main_monitor()  # # 开启监视器线程
        self._pool_max_num = pool_num  # #最大线程数,字典存储
        self._run(pool_num)  # #运行伺服线程
        self._result_list = []  # #任务结果存储

    def __call__(self, func):
        @wraps(func)
        def _run_threads(*args, **kw):
            self._pool_queue.put((func, args, kw))

        return _run_threads

    def change_thread_num(self, num):
        x = self._pool_max_num - num
        if x < 0:
            self._run(abs(x))
        if x > 0:
            for _ in range(abs(x)):
                self._pool_queue.put('KillThreadParams')
        self._pool_max_num = num

    def _run(self, num):
        def _pools_pull():
            while True:
                args_list = self._pool_queue.get()
                if args_list == 'KillThreadParams':
                    return
                try:
                    func, args, kw = args_list
                    Result = func(*args, **kw)  # 获取结果
                    self._result_list.append(Result)
                except BaseException as e:
                    print(" - thread stop_by_error - ", e)
                    break
                finally:
                    self._pool_queue.task_done()  # 发出此队列完成信号

        # 线程的开启
        for _ in range(num):
            Thread(target=_pools_pull).start()

    def main_monitor(self):
        def _func():
            while True:

                sleep(0.25)
                if not main_thread().isAlive():
                    self.close_all()
                    break

        self._MainMonitor = Thread(target=_func, name="MainMonitor")
        self._MainMonitor.start()

    def joinall(self):
        self._pool_queue.join()

    def wait_completed(self):
        """等待全部线程结束，返回结果"""
        self._pool_queue.join()
        return self._result_list

    def close_all(self):
        self.change_thread_num(0)


class CustomThread(Thread):
    """多线程，继承自threading.Thread"""

    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func, args=args, kwargs=kwargs)
        self.daemon = True
        self.start()
        self.all_Thread.append(self)

    '''下标obj[key]'''

    def __getitem__(self, attr):
        return getattr(self, attr)

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)

    def getResult(self):
        try:
            self.join()
            return self.Result
        except Exception:
            return None

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()  # @单例无效

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果
        # @单例无效"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束，返回结果"""
        cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
        finished = True
        while finished:
            nowlist = enumerate()  # 线程list
            list_tmp = [
                type(nowlist[index]).__name__ for index in range(len(nowlist))
            ]
            if cls.__name__ in list_tmp:
                # print(time(), 'has ', cls.__name__, len(nowlist), len(list_tmp))
                sleep(0.1)
                continue
            else:
                finished = False  # while结束标识
                break

        res, cls.result_list = cls.result_list, []
        return res


class CustomThread_Queue(Thread):
    """单例多线程，继承自threading.Thread"""
    """采用queue传递工作任务"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    task_queue = Queue()

    def __init__(self, queue_list, **kwargs):
        super().__init__(**kwargs)
        self.task_queue.put([*queue_list])
        self.start()
        self.all_Thread.append(self)

    '''下标obj[key]'''

    def __getitem__(self, attr):
        return getattr(self, attr)

    def run(self):
        try:
            args = self.task_queue.get()  # task_queue.get(False)
        except Empty:
            return
        target = args.pop(0)
        self.Result = target(*args)  # 获取结果
        self.result_list.append(self.Result)
        self.task_queue.task_done()  # @发出此队列完成信号，放在函数运行后

    def getResult(self):
        """获取当前线程结果"""
        try:
            return self.Result
        except Exception:
            return None

    def join_with_timeout(self, timeout=15):
        self.task_queue.all_tasks_done.acquire()
        try:
            endtime = time() + timeout
            while self.task_queue.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    print('unfinished_tasks in task_queue : ',
                          self.task_queue.unfinished_tasks)
                    break
                self.task_queue.all_tasks_done.wait(0.2)
        finally:
            self.task_queue.all_tasks_done.release()

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()
        self.task_queue.join()  # !queue.join

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """等待线程，超时结束，返回结果"""
        cls.join_with_timeout(cls)  # !queue.join,使用带timeout
        res, cls.result_list = cls.result_list, []
        return res


class SingletonThread(Thread):
    """单例多线程，继承自threading.Thread"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func, args=args, **kwargs)
        self.start()
        self.all_Thread.append(self)

    '''下标obj[key]'''

    def __getitem__(self, attr):
        return getattr(self, attr)

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)

    def getResult(self):
        try:
            return self.Result
        except Exception:
            return None

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()  # !单例此处无效果

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果
        # @单例无效"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束，返回结果"""
        cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
        finished = True
        while finished:
            nowlist = enumerate()  # 线程list
            list_tmp = [
                type(nowlist[index]).__name__ for index in range(len(nowlist))
            ]
            if cls.__name__ in list_tmp:
                # print(time(), 'has ', cls.__name__, len(nowlist), len(list_tmp))
                sleep(0.5)
                continue
            else:
                finished = False  # 结束while
                break
            # nowlist = enumerate()  # 线程list
            # for index in range(len(nowlist)):
            #     if type(nowlist[index]).__name__ == cls.__name__:
            #         sleep(0.1)
            #         finished = True  # 继续while
            #         break  # 跳出for
            #     elif index + 1 == len(nowlist):
            #         finished = False  # 结束while
            #         break  # 跳出for
            #     else:
            #         continue  # 继续for

        res, cls.result_list = cls.result_list, []
        return res


def make_singleton_thread_class(name):
    _cls = singleton_wrap_return_class(CustomThread)
    _cls.__name__ = name  # @单例线程运行结束判断依据
    _cls.result_list = []  # @单独配置结果字典
    _cls.wait_completed, _cls.getAllResult = _cls.getAllResult, _cls.wait_completed
    return _cls


def make_queue_singleton_thread_class():
    _cls = singleton_wrap_return_class(CustomThread_Queue)
    _cls.result_list = []  # @单独配置结果字典
    return _cls


SigThread = make_singleton_thread_class('SigThread')

SigThreadQ = make_queue_singleton_thread_class()
