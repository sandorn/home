# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 18:48:30
#FilePath     : /xjLib/xt_Thread/manage.py
#LastEditTime : 2020-07-22 15:02:22
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from threading import Thread, Event
from queue import Queue, Empty
import traceback
import sys
from time import sleep


def _handle_thread_exception(request, exc_info):
    """默认错误处理"""
    traceback.print_exception(*exc_info)


class task_object:
    '''任务处理的对象类'''
    def __init__(self, func, args=None, kwds=None, callback=None, exc_callback=_handle_thread_exception):
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
    '''自编线程池，可以再次添加任务;\n
    获取阶段结果：getAllResult();\n
    关闭线程获取最终结果：wait_completed()'''
    def __init__(self, items=None, MaxSem=66, callback=None, exc_callback=_handle_thread_exception, **kwds):
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.all_Thread = []
        self.callback = callback
        self.exc_callback = exc_callback
        self.kwds = kwds
        if items:
            self.add_work_queue(items)
        self.setMaxcs(MaxSem)

    def add_work_queue(self, args_list):
        # #初始化工作队列,添加工作入队
        for args in args_list:
            assert isinstance(args, (list, tuple))
            func = args.pop(0)
            task = task_object(func, args, callback=self.callback, exc_callback=self.exc_callback)
            self.work_queue.put(task)

    def setMaxcs(self, MaxSem):
        """修改最大工作线程数，根据差额创建或关闭工作线程"""
        self.MaxSem = MaxSem
        if self.MaxSem > len(self.all_Thread):
            self.create_work_thread(self.MaxSem - len(self.all_Thread), **self.kwds)
        elif self.MaxSem < len(self.all_Thread):
            self.close_work_thread(len(self.all_Thread) - self.MaxSem, **self.kwds)

    def create_work_thread(self, MaxSem, **kwds):
        """按照设计数量，初始化线程并运行"""
        for i in range(MaxSem):
            self.all_Thread.append(Work(self.work_queue, self.result_queue, **kwds))

    def close_work_thread(self, num_workers):
        """关闭要求数量的工作线程"""
        _stop_list = []
        for _ in range(min(num_workers, len(self.all_Thread))):
            thread = self.all_Thread.pop()
            thread.stop_work()
            _stop_list.append(thread)

        for worker in _stop_list:
            thread.join()

    def break_manager(self):
        """直接关闭全部工作线程"""
        self.close_work_thread(len(self.all_Thread))

    def wait_completed(self):
        '''禁止添加任务，等待所有线程运行完毕,返回尚未获取的全部结果'''
        self.work_queue.join()  # #确保所有任务完成
        self.close_work_thread(len(self.all_Thread))  # #再关闭全部工作线程

        result_list = []
        while not self.result_queue.empty():
            res = self.result_queue.get_nowait()
            # !get(False) 任务异步出队 get_nowait()
            result_list.append(res)
        return result_list

    def getAllResult(self):
        '''获取之前任务的全部结果，work_thread继续值机'''
        self.work_queue.join()
        result_list = []
        while not self.result_queue.empty():
            res = self.result_queue.get_nowait()
            result_list.append(res)
        return result_list


class Work(Thread):
    def __init__(self, work_queue, result_queue, **kwds):
        super().__init__(**kwds)
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self._stop_event = Event()
        self.start()

    def run(self):
        # #有优化空间，event理解不够
        while not self._stop_event.is_set():
            if not self.work_queue.empty():
                task = self.work_queue.get(False)  # !任务异步出队 get_nowait()
                try:
                    result = task.func(*task.args, **task.kwds)  # 传递 list 各元素
                except Exception as err:
                    task.exception = err
                    if task.exc_callback: task.exc_callback(err)
                    self.result_queue.put(task)  # 存储错误信息
                else:
                    self.result_queue.put(result)  # 取得函数返回值
                    if task.callback: task.callback(err)
                self.work_queue.task_done()  # 通知系统任务完成
            else:
                self._stop_event.wait(0.2)

    def stop_work(self):
        """停止工作线程"""
        self._stop_event.set()


class thread_pool:
    '''仿写vthread,
    # thread_pool(200)'''
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
