# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-29 11:40:57
FilePath     : /CODE/xjLib/xt_thread/thread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import ctypes
import inspect
from queue import Empty, Queue
from threading import Event, Thread, main_thread
from threading import enumerate as thread_enumerate
from time import sleep, time

import wrapt
from xt_class import ItemGetMixin
from xt_singleon import SingletonMixin, singleton_decorator_class
from xt_thread import thread_print


class CustomThreadMeta(Thread, ItemGetMixin):
    all_Thread = []  # 线程列表,用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    finished = Event()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        try:
            cls.stop_all()
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def stop_all(cls):
        """停止线程池, 所有线程停止工作"""
        while cls.all_Thread:
            _thread = cls.all_Thread.pop()
            _thread.join()

    def getResult(self):
        try:
            self.join()
            return self.Result
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束,返回结果"""
        cls.stop_all()
        nowlist = thread_enumerate()  # 线程list
        while not cls.finished.is_set():
            list_tmp = [type(nowlist[index]).__name__ for index in range(len(nowlist))]
            if cls.__name__ in list_tmp:
                cls.finished.wait(0.1)  # sleep(0.1)
            else:
                cls.finished.set()
                break

        res, cls.result_list = cls.result_list, []
        return res


class ThreadPoolWraps:
    """仿写vthread,线程装饰器,ThreadPoolWraps(200)"""

    def __init__(self, pool_num=32):
        self._task_queue = Queue()  # 任务存储,组内queue
        self._max_threads = pool_num  # 最大线程数,字典存储
        self._result_list = []  # 任务结果存储
        # 开启监视器线程
        self._MainMonitor = Thread(target=self._monitor_function, name="Monitor")
        self._MainMonitor.start()
        self._start_servo_threads(self._max_threads)  # 运行伺服线程

    @wrapt.decorator
    def __call__(self, func, instance, args, kwargs):
        self._task_queue.put([func, args, kwargs])

    def change_thread_num(self, num):
        """改变线程数量"""
        x = self._max_threads - num
        abs_x = abs(x)
        if x < 0:
            self._start_servo_threads(abs_x)
        if x > 0:
            for _ in range(abs_x):
                self._task_queue.put("KillThreadParams")
        self._max_threads = num

    def _servo_function(self):
        while True:
            args_list = self._task_queue.get()
            if args_list == "KillThreadParams":
                return
            try:
                func, args, kw = args_list
                Result = func(*args, **kw)
                self._result_list.append(Result)
            except BaseException as e:
                print(f"[thread stop_with_error:{e}]")
                break
            finally:
                self._task_queue.task_done()  # 发出此队列完成信号

    def _start_servo_threads(self, num):
        """开启伺服线程"""
        for _ in range(num):
            thread = Thread(target=self._servo_function, name="servo", daemon=True)
            thread.start()

    def _monitor_function(self):
        _main_thr = main_thread()
        while True:
            sleep(0.2)
            if not _main_thr.is_alive():
                self.close_all()
                break

    def joinall(self):
        self._task_queue.join()

    def wait_completed(self):
        """等待全部线程结束，返回结果"""
        self._task_queue.join()
        return self._result_list

    def close_all(self):
        self.change_thread_num(0)


def stop_thread(thread):
    """外部停止线程"""

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


class CustomThread(CustomThreadMeta):
    """多线程,继承自threading.Thread"""

    all_Thread = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用
    finished = Event()

    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self._isRunning = True
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.daemon = True
        self.all_Thread.append(self)
        self.start()

    def __del__(self):
        # 线程状态改变与线程终止
        self.join()  # 等待线程执行完毕
        self.stop()

    def stop(self):
        self._isRunning = False

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)


class CustomThread_Queue(CustomThreadMeta):
    """
    单例多线程,继承自threading.Thread\n
    采用queue传递工作任务
    """

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

    @classmethod
    def join_with_timeout(cls, timeout=15):
        cls.task_queue.all_tasks_done.acquire()

        try:
            endtime = time() + timeout
            while cls.task_queue.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    print(
                        "unfinished_tasks in task_queue : ",
                        cls.task_queue.unfinished_tasks,
                    )
                    break
                cls.task_queue.all_tasks_done.wait(remaining)
        finally:
            cls.task_queue.all_tasks_done.release()

    @classmethod
    def stop_all(cls):
        """停止线程池, 所有线程停止工作"""
        super().stop_all()
        cls.task_queue.join()

    @classmethod
    def getAllResult(cls):
        """等待线程,超时结束,返回结果"""
        cls.join_with_timeout()  # !queue.join,使用带timeout
        res, cls.result_list = cls.result_list, []
        return res


class SingletonThread(SingletonMixin, CustomThread): ...


def _create_singleton_thread_class(parent_cls, new_class_name):
    # #使用类装饰器 singleton_decorator_class 转换为单例类
    _cls = singleton_decorator_class(parent_cls)
    _cls.__name__ = new_class_name  # @单例线程运行结束判断依据
    _cls.result_list = []  # @单独配置结果字典
    _cls.wait_completed, _cls.getAllResult = _cls.getAllResult, _cls.wait_completed
    return _cls


SigThread = _create_singleton_thread_class(CustomThread, "SigThread")
SigThreadQ = _create_singleton_thread_class(CustomThread_Queue, "SigThreadQ")

if __name__ == "__main__":

    def func(*arg, **kwargs):
        thread_print(*arg, **kwargs)
        sleep(2)
        return arg

    a = SigThread(print, 111111111111111)
    print(22222222222, a.getResult(), a.__name__, type(a))
    b = SigThread(func, 2, 3)
    print(33333333333, b.getResult())
    c = SigThreadQ([func, 2, 3])
    print(44444444444, c.getResult(), c.__name__, type(c))
    """
    tpool = ThreadPoolWraps(200)

    for index, arg in enumerate(args, start=1):
        tpool(func)(arg, kwargs)
    text_list = tpool.wait_completed()
    """
