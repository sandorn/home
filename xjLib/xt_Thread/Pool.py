# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 18:48:30
#FilePath     : /xjLib/xt_Thread/Pool.py
#LastEditTime : 2020-06-24 17:11:05
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from threading import Thread, Event
from queue import Queue, Empty
import traceback
import sys
from time import sleep


class NoResultsPending(Exception):
    '''所有任务均已处理'''
    pass


class NoWorkersAvailable(Exception):
    '''没有工作线程可用于处理剩余请求'''
    pass


def _handle_thread_exception(request, exc_info):
    """默认错误处理"""
    traceback.print_exception(*exc_info)


def make_task_object(args_list,
                     callback=None,
                     exc_callback=_handle_thread_exception):
    tasks = []
    for args in args_list:
        assert isinstance(args, list)
        func = args.pop(0)
        tasks.append(
            task_object(func,
                        args,
                        callback=callback,
                        exc_callback=exc_callback))
    return tasks


class task_object:
    '''任务处理的对象类'''
    def __init__(self,
                 func,
                 args=None,
                 kwds=None,
                 callback=None,
                 exc_callback=_handle_thread_exception):
        self.requestID = id(self)
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.func = func
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return f"<work_task_object id={self.requestID} target={self.func}  \args={ self.args} kwargs={self.kwds} exception={self.exception}>"


class WorkManager(object):
    '''简单线程池，不能再次添加任务'''
    def __init__(self,
                 items,
                 MaxSem=99,
                 callback=None,
                 exc_callback=_handle_thread_exception,
                 kwds={}):
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.all_Thread = []
        self.add_work_queue(items,
                            callback=callback,
                            exc_callback=exc_callback)
        self.MaxSem = MaxSem
        self.create_thread(**kwds)

    def add_work_queue(self,
                       items,
                       callback=None,
                       exc_callback=_handle_thread_exception):
        # #初始化工作队列,添加工作入队
        tasks = make_task_object(items,
                                 callback=callback,
                                 exc_callback=exc_callback)
        for task in tasks:
            assert isinstance(task, task_object)
            assert not getattr(task, 'exception', None)
            self.work_queue.put(task)

    def create_thread(self, **kwds):
        # #初始化线程,同时运行线程数量
        for i in range(self.MaxSem):
            self.all_Thread.append(
                Work(self.work_queue, self.result_queue, **kwds))

    def wait_allcomplete(self):
        # #等待所有线程运行完毕
        for _ in range(len(self.all_Thread)):
            thread = self.all_Thread.pop()
            thread.join()

        result_list = []
        for i in range(self.result_queue.qsize()):
            res = self.result_queue.get()
            result_list.append(res)
        return result_list

    def queue_join(self):
        # #等待所有线程运行完毕
        self.work_queue.join()

        result_list = []
        while True:
            try:
                res = self.result_queue.get(False)  # !任务异步出队 get_nowait()
                result_list.append(res)
            except Empty:
                break
        self.all_Thread = []
        return result_list


class Work(Thread):
    def __init__(self, work_queue, result_queue, kwds={}):
        super().__init__(**kwds)
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while not self.work_queue.empty():
            try:
                task = self.work_queue.get(False)  # !任务异步出队 get_nowait()
            except Empty:
                break
            else:
                result = task.func(*task.args, **task.kwds)  # 传递 list 各元素
                self.result_queue.put(result)  # 取得函数返回值
                self.work_queue.task_done()  # 通知系统任务完成


class thread_pool_maneger(object):
    '''参照htreadpool编写的自定义库 '''
    def __init__(self,
                 items,
                 MaxSem=99,
                 callback=None,
                 exc_callback=_handle_thread_exception,
                 poll_timeout=5,
                 kwds={}):
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.all_Thread = []
        self.result_list = []
        self.stoped_thread = []
        self.all_Tasks = {}

        if MaxSem is not None:
            self.setMaxcs(MaxSem, poll_timeout=5, **kwds)
        self.add_work_queue(items,
                            callback=callback,
                            exc_callback=exc_callback,
                            poll_timeout=poll_timeout)

    def setMaxcs(self, MaxSem, poll_timeout=5, **kwds):  # 外部修改最大线程数
        self.MaxSem = MaxSem
        self.all_Thread.clear()
        self.create_thread(self.MaxSem, poll_timeout=5, **kwds)

    def getMaxcs(self):  # 外部获得最大线程数
        return self.MaxSem

    def create_thread(self, MaxSem, poll_timeout=5, **kwds):
        """初始化线程,同时运行线程数量"""
        for i in range(MaxSem):
            self.all_Thread.append(
                WorkThread(self.work_queue,
                           self.result_queue,
                           poll_timeout=poll_timeout,
                           **kwds))

    def add_work_queue(self,
                       items,
                       callback=None,
                       exc_callback=_handle_thread_exception,
                       block=True,
                       poll_timeout=5):
        """初始化工作队列,添加工作入队"""
        tasks = make_task_object(items,
                                 callback=callback,
                                 exc_callback=exc_callback)
        for task in tasks:
            assert isinstance(task, task_object)
            assert not getattr(task, 'exception', None)
            self.work_queue.put(task, block, poll_timeout)
            self.all_Tasks[task.requestID] = task

    def stop_thread(self, num_workers, if_join=False):
        """停用一定数量的线程"""
        stop_list = []
        for _ in range(min(num_workers, len(self.all_Thread))):
            thread = self.all_Thread.pop()
            thread.stop_work()
            stop_list.append(thread)

        if if_join:
            for worker in stop_list:
                worker.join()
        else:
            self.stoped_thread.extend(stop_list)

    def join_all_stoped_thread(self):
        """join 所有停用的线程"""
        for worker in self.stoped_thread:
            worker.join()
        self.stoped_thread = []

    def poll(self, block=False):
        """拉取数据进行处理, 用于wait"""
        while not self.result_queue.empty():
            if not self.all_Tasks:
                raise NoResultsPending
            elif block and not self.work_queue:
                raise NoWorkersAvailable

            task, result = self.result_queue.get(block=block)
            if task.exception and task.exc_callback:
                task.exc_callback(task, result)
            if task.callback and not (task.exception and task.exc_callback):
                task.callback(result)
            self.result_list.append(result)
            del self.all_Tasks[task.requestID]

    def wait(self):
        """等待所有请求处理完毕"""
        while True:
            try:
                self.poll(True)
            except NoResultsPending:
                break

    def stop_all(self):
        """停止线程池"""
        self.stop_thread(len(self.all_Thread), True)
        self.join_all_stoped_thread()

    def getAllResult(self):
        """停止线程池， 等待返回结果"""
        self.wait()
        self.stop_thread(len(self.all_Thread), True)
        self.join_all_stoped_thread()
        return self.result_list


class WorkThread(Thread):
    def __init__(self, work_queue, result_queue, poll_timeout=5, kwds={}):
        super().__init__(**kwds)
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self._poll_timeout = poll_timeout
        self._stop_event = Event()
        self.start()

    def run(self):
        """工作线程启动函数"""
        while True:
            # 检查线程是否被停止
            if self._stop_event.is_set():
                break

            # 请求队列中取出
            try:
                task = self.work_queue.get(True, self._poll_timeout)
                # 可以等待添加任务
            except Empty:
                sleep(0.1)
                continue
            # 检查线程是否被停止
            if self._stop_event.is_set():
                self.work_queue.put(task)
                break

            # 执行请求队列中的请求
            try:
                result = task.func(*task.args, **task.kwds)
                self.result_queue.put((task, result))
            except BaseException:
                task.exception = True
                self.result_queue.put((task, sys.exc_info()))

    def stop_work(self):
        """停止工作线程"""
        self._stop_event.set()
