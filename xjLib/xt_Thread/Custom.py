# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-24 13:31:44
FilePath     : /xjLib/xt_Thread/Custom.py
LastEditTime : 2020-11-27 18:34:42
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import ctypes
import inspect
from queue import Empty, Queue
from threading import Event, Thread, enumerate
from time import time

from xt_Class import item_get_Mixin
from xt_Singleon import Singleton_Mixin, singleton_wrap_return_class


def stop_thread(thread):
    '''外部停止线程'''

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

    _async_raise(thread.ident, SystemExit)


class CustomThread(Thread, item_get_Mixin):
    """多线程,继承自threading.Thread"""

    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    finished = Event()

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func, args=args, kwargs=kwargs)
        self.daemon = True
        self.start()
        self.all_Thread.append(self)

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
        # finished = True
        while not cls.finished.is_set():
            nowlist = enumerate()  # 线程list
            list_tmp = [type(nowlist[index]).__name__ for index in range(len(nowlist))]
            if cls.__name__ in list_tmp:
                cls.finished.wait(0.1)  # sleep(0.1)
                continue
            else:
                cls.finished.set()
                break

        res, cls.result_list = cls.result_list, []
        return res


class CustomThread_Queue(Thread, item_get_Mixin):
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
                    print('unfinished_tasks in task_queue : ', self.task_queue.unfinished_tasks)
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


class SingletonThread(Thread, item_get_Mixin, Singleton_Mixin):
    """单例多线程，继承自threading.Thread"""
    # #照写 from xt_Singleon import Singleton_Model

    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    finished = Event()

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func, args=args, kwargs=kwargs)
        self.daemon = True
        self.start()
        self.all_Thread.append(self)

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
        # finished = True
        while not cls.finished.is_set():
            nowlist = enumerate()  # 线程list
            list_tmp = [type(nowlist[index]).__name__ for index in range(len(nowlist))]
            if cls.__name__ in list_tmp:
                cls.finished.wait(0.1)  # sleep(0.1)
                continue
            else:
                cls.finished.set()
                break

        res, cls.result_list = cls.result_list, []
        return res

    # wait_completed, getAllResult = getAllResult, wait_completed


def make_singleton_thread_class(name):
    # #使用类装饰器 from xt_Singleon import singleton_wrap_return_class，转换为单例类
    _cls = singleton_wrap_return_class(CustomThread)
    _cls.__name__ = name  # @单例线程运行结束判断依据
    _cls.result_list = []  # @单独配置结果字典
    _cls.wait_completed, _cls.getAllResult = _cls.getAllResult, _cls.wait_completed
    return _cls


def make_queue_singleton_thread_class():
    # #使用类装饰器 from xt_Singleon import singleton_wrap_return_class，转换为单例类
    _cls = singleton_wrap_return_class(CustomThread_Queue)
    _cls.result_list = []  # @单独配置结果字典
    return _cls


SigThread = make_singleton_thread_class('SigThread')

SigThreadQ = make_queue_singleton_thread_class()


class CustomThread_Singleton(CustomThread, Singleton_Mixin):
    # #混入继承Singleton_Mixin，转换为单例类
    pass


class CustomThread_Queue_Singleton(CustomThread_Queue, Singleton_Mixin):
    # #混入继承Singleton_Mixin，转换为单例类
    pass


'''
类转为单例模式：
    1.照写 from xt_Singleon import Singleton_Model
    2.使用类装饰器 from xt_Singleon import singleton_wrap_return_class
    3.混入继承 from xt_Singleon import Singleton_MiXin
'''
