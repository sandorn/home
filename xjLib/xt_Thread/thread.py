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
from threading import Condition, Event, Thread, enumerate
from time import time

from xt_Class import item_get_Mixin
from xt_Thread import Singleton_Mixin, singleton_wrap_return_class


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

    all_Thread = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用
    finished = Event()

    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.index = len(self.all_Thread)
        self._target = target
        self._args = args
        self._kwargs = kwargs
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
        """停止线程池, 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()  # @单例无效

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果
        # @单例无效"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束,返回结果"""
        cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
        nowlist = enumerate()  # 线程list
        while not cls.finished.is_set():
            list_tmp = [type(nowlist[index]).__name__ for index in range(len(nowlist))]
            if cls.__name__ in list_tmp:
                cls.finished.wait(0.1)  # sleep(0.1)
            else:
                cls.finished.set()
                break

        res, cls.result_list = cls.result_list, []
        return res


class CustomThread_Queue(Thread, item_get_Mixin):
    """单例多线程,继承自threading.Thread"""
    """采用queue传递工作任务"""
    all_Thread = []  # 线程列表,用于jion。类属性或类变量,实例公用
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
        self.task_queue.task_done()  # @发出此队列完成信号,放在函数运行后

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
                self.task_queue.all_tasks_done.wait(0.1)
        finally:
            self.task_queue.all_tasks_done.release()

    def stop_all(self):
        """停止线程池, 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()
        self.task_queue.join()  # !queue.join

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """等待线程,超时结束,返回结果"""
        cls.join_with_timeout(cls)  # !queue.join,使用带timeout
        res, cls.result_list = cls.result_list, []
        return res


class SingletonThread(Thread, item_get_Mixin, Singleton_Mixin):
    """单例多线程,继承自threading.Thread"""

    all_Thread = []  # 线程列表,用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    finished = Event()

    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._target = target
        self._args = args
        self._kwargs = kwargs
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
        """停止线程池, 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()  # @单例无效

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果
        # @单例无效"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束,返回结果"""
        cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
        nowlist = enumerate()  # 线程list
        while not cls.finished.is_set():
            list_tmp = [type(nowlist[index]).__name__ for index in range(len(nowlist))]
            if cls.__name__ in list_tmp:
                cls.finished.wait(0.1)  # sleep(0.1)
            else:
                cls.finished.set()
                break

        res, cls.result_list = cls.result_list, []
        return res


def _create_singleton_thread_class(parent_cls, new_class_name):
    # #使用类装饰器 singleton_wrap_return_class 转换为单例类
    _cls = singleton_wrap_return_class(parent_cls)
    _cls.__name__ = new_class_name  # @单例线程运行结束判断依据
    _cls.result_list = []  # @单独配置结果字典
    _cls.wait_completed, _cls.getAllResult = _cls.getAllResult, _cls.wait_completed
    return _cls


SigThread = _create_singleton_thread_class(CustomThread, 'SigThread')
SigThreadQ = _create_singleton_thread_class(CustomThread_Queue, 'SigThreadQ')


class CustomThread_Pool:
    """线程池,继承自threading.Thread,Copilot自编"""

    def __init__(self, max_workers=10, target=None, *args, **kwargs):
        self.max_workers = max_workers
        self.all_Thread = []  # 线程列表,用于jion。类属性或类变量,实例公用
        self.result_list = []  # 结果列表
        self.task_queue = Queue()  # 任务队列
        self.task_queue.all_tasks_done = Condition()  # 任务队列锁
        self.finished = Event()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._create_thread_pool()

    def _create_thread_pool(self):
        for _ in range(self.max_workers):
            thread = Thread(target=self._target, args=self._args, kwargs=self._kwargs)
            thread.daemon = True
            thread.start()
            self.all_Thread.append(thread)

    def _get_result(self):
        """获取结果"""
        self.result_list.append(self._target(*self._args, **self._kwargs))

    def add_task(self, target, *args, **kwargs):
        """添加任务"""
        self.task_queue.put((target, args, kwargs))

    def run(self):
        """运行任务"""
        while True:
            target, args, kwargs = self.task_queue.get()
            self._target = target
            self._args = args
            self._kwargs = kwargs
            self._get_result()
            self.task_queue.task_done()
            self.task_queue.all_tasks_done.acquire()
            self.task_queue.all_tasks_done.notify_all()
            self.task_queue.all_tasks_done.release()

    def join_with_timeout(self, timeout=10):
        """等待线程,超时结束,返回结果"""
        self.task_queue.all_tasks_done.acquire()
        try:
            endtime = time() + timeout
            while self.task_queue.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    print('unfinished_tasks in task_queue : ', self.task_queue.unfinished_tasks)
                    break
                self.task_queue.all_tasks_done.wait(0.1)
        finally:
            self.task_queue.all_tasks_done.release()

    def stop_all(self):
        """停止线程池, 所有线程停止工"""
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()  # @单例无效