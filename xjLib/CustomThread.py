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
@LastEditors: Even.Sand
@LastEditTime: 2020-04-04 17:52:45
'''


__all__ = [
    'SingletonThread',  # 单例
    'SingletonThread_Queue',
    'CustomThread',  # 继承线程
    'Custom_Thread_Queue',
    'NoResultsPending',  # 任务均已处理
    'NoWorkersAvailable',  # 无工作线程可用
    'WorkManager',  # 线程池管理，参照htreadpool编写的自定义库
    'Work',  # 线程池任务结构，参照htreadpool编写的自定义库
    'thread_pool_maneger',
    'WorkThread'  # 继承线程,利用queue；参照htreadpool编写的自定义库
]


import ctypes
import inspect
import sys
import threading
import traceback
from queue import Queue, Empty
from time import time, sleep


class SingletonThread(threading.Thread):
    """单例多线程，继承自threading.Thread"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    _instance_lock = threading.Lock()
    rlock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, func, args, **kwargs):
        super().__init__(target=func, args=args, **kwargs)
        SingletonThread.all_Thread.append(self)
        self.start()

    def run(self):
        # 调用线程函数，并将元组类型的参数值分解为单个的参数值传入线程函数
        self.Result = self._target(self.rlock, *self._args)  # 获取结果
        SingletonThread.result_list.append(self.Result)

    def getResult(self):
        try:
            return self.Result
        except Exception:
            return None

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(SingletonThread.all_Thread)):
            thread = SingletonThread.all_Thread.pop()
            thread.join()  # !单例此处无效果

    @classmethod
    def wait_completed(cls):
        """利用enumerate,根据类名判断线程结束，返回结果"""
        cls.stop_all(cls)   # !向stop_all函数传入self 或cls ,三处保持一致
        finished = True
        while finished:
            nowlist = threading.enumerate()
            for index, item in enumerate(nowlist):
                if(type(item).__name__ == 'SingletonThread'):
                    sleep(0.1)
                    finished = True  # 继续while
                    break  # 跳出for
                elif(index + 1 == len(nowlist)):
                    finished = False   # 结束while
                    break  # 跳出for
                else:
                    continue  # 继续for

        res, SingletonThread.result_list = SingletonThread.result_list, []
        return res

    @classmethod
    def getAllResult(cls):
        """等待线程结束，返回结果"""
        res, SingletonThread.result_list = SingletonThread.result_list, []
        return res


class SingletonThread_Queue(threading.Thread):
    """单例多线程，继承自threading.Thread"""
    """采用queue传递工作任务，queue不能超出线程数量"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    _instance_lock = threading.Lock()
    rlock = threading.RLock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, queue, **kwargs):
        super().__init__(**kwargs)
        SingletonThread_Queue.queue = queue
        SingletonThread_Queue.all_Thread.append(self)
        self.start()

    def run(self):
        try:
            args = SingletonThread_Queue.queue.get()  # 相当queue.get(False)
        except Empty:
            return
        else:
            target = args.pop(0)
            self.Result = target(SingletonThread_Queue.rlock, *args)   # 获取结果
            # with SingletonThread_Queue.rlock:
            #    print(self.name, '\targs:', *args, '\tdone。', flush=True)
            SingletonThread_Queue.queue.task_done()  # 发出此队列完成信号
            SingletonThread_Queue.result_list.append(self.Result)

    def getResult(self):
        """获取当前线程结果"""
        try:
            return self.Result
        except Exception:
            return None

    def join_with_timeout(timeout=5):
        SingletonThread_Queue.queue.all_tasks_done.acquire()
        try:
            endtime = time() + timeout
            while SingletonThread_Queue.queue.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    print('unfinished_tasks in queue : ', SingletonThread_Queue.queue.unfinished_tasks)
                    break
                SingletonThread_Queue.queue.all_tasks_done.wait(0.2)
        finally:
            SingletonThread_Queue.queue.all_tasks_done.release()

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(SingletonThread_Queue.all_Thread)):
            thread = SingletonThread_Queue.all_Thread.pop()
            thread.join()
        SingletonThread_Queue.queue.join()  # !queue.join

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)   # !向stop_all函数传入self 或cls ,三处保持一致
            res, SingletonThread_Queue.result_list = SingletonThread_Queue.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """等待线程，超时结束，返回结果"""
        cls.join_with_timeout()  # !queue.join,使用带timeout
        res, SingletonThread_Queue.result_list = SingletonThread_Queue.result_list, []
        return res


class CustomThread(threading.Thread):
    """多线程，继承自threading.Thread"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    rlock = threading.RLock()

    def __init__(self, func, args, **kwargs):
        super().__init__(target=func, args=args, **kwargs)
        self.daemon = True
        CustomThread.all_Thread.append(self)
        self.start()

    def run(self):
        # 调用线程函数，并将元组类型的参数值分解为单个的参数值传入线程函数
        self.Result = self._target(self.rlock, *self._args)  # 获取结果
        CustomThread.result_list.append(self.Result)

    def getResult(self):
        try:
            return self.Result
        except Exception:
            return None

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(CustomThread.all_Thread)):
            thread = CustomThread.all_Thread.pop()
            thread.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)   # !向stop_all函数传入self 或cls ,三处保持一致
            res, CustomThread.result_list = CustomThread.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """返回结果"""
        res, CustomThread.result_list = CustomThread.result_list, []
        return res


class Custom_Thread_Queue(threading.Thread):
    """多线程，继承自threading.Thread"""
    """采用queue传递工作任务，queue不能超出线程数量"""
    all_Thread = []  # 线程列表，用于jion。类属性或类变量,实例公用
    result_list = []  # 结果列表
    rlock = threading.RLock()

    def __init__(self, queue, **kwargs):
        super().__init__(**kwargs)
        self.daemon = True
        Custom_Thread_Queue.queue = queue
        Custom_Thread_Queue.all_Thread.append(self)
        self.start()

    def run(self):
        try:
            args = Custom_Thread_Queue.queue.get()
        except Empty:
            return
        else:
            target = args.pop(0)
            self.Result = target(Custom_Thread_Queue.rlock, *args)   # 获取结果
            # with Custom_Thread_Queue.rlock:
            #    print(self.name, '\targs:', *args, '\tdone。', flush=True)
            Custom_Thread_Queue.queue.task_done()  # 发出此队列完成信号
            Custom_Thread_Queue.result_list.append(self.Result)

    def getResult(self):
        """获取当前线程结果"""
        try:
            return self.Result
        except Exception:
            return None

    def join_with_timeout(timeout=5):
        Custom_Thread_Queue.queue.all_tasks_done.acquire()
        try:
            endtime = time() + timeout
            while Custom_Thread_Queue.queue.unfinished_tasks:
                remaining = endtime - time()
                if remaining <= 0.0:
                    print('unfinished_tasks in queue : ', Custom_Thread_Queue.queue.unfinished_tasks)
                    break
                Custom_Thread_Queue.queue.all_tasks_done.wait(0.2)
        finally:
            Custom_Thread_Queue.queue.all_tasks_done.release()

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(Custom_Thread_Queue.all_Thread)):
            thread = Custom_Thread_Queue.all_Thread.pop()
            thread.join()
        Custom_Thread_Queue.queue.join()  # !queue.join

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)   # !向stop_all函数传入self 或cls ,三处保持一致
            res, Custom_Thread_Queue.result_list = Custom_Thread_Queue.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """等待线程，超时结束，返回结果"""
        cls.join_with_timeout()  # !queue.join,使用带timeout
        res, Custom_Thread_Queue.result_list = Custom_Thread_Queue.result_list, []
        return res


class NoResultsPending(Exception):
    '''所有任务均已处理'''
    pass


class NoWorkersAvailable(Exception):
    '''没有工作线程可用于处理剩余请求'''
    pass


def _handle_thread_exception(request, exc_info):
    """默认错误处理"""
    traceback.print_exception(*exc_info)


def make_task_object(args_list, callback=None, exc_callback=_handle_thread_exception):
    tasks = []
    for args in args_list:
        assert isinstance(args, list)
        func = args.pop(0)
        tasks.append(
            task_object(func, args, callback=callback,
                        exc_callback=exc_callback)
        )
    return tasks


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
    '''简单线程池，不能再次添加任务'''

    def __init__(self, items, MaxSem=99, callback=None, exc_callback=_handle_thread_exception, kwds={}):
        self.lock = threading.RLock()
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.all_Thread = []
        self.add_work_queue(items, callback=callback, exc_callback=exc_callback)
        self.MaxSem = MaxSem
        self.create_thread(**kwds)

    def add_work_queue(self, items, callback=None, exc_callback=_handle_thread_exception):
        # #初始化工作队列,添加工作入队
        tasks = make_task_object(items, callback=callback, exc_callback=exc_callback)
        for task in tasks:
            assert isinstance(task, task_object)
            assert not getattr(task, 'exception', None)
            self.work_queue.put(task)

    def create_thread(self, **kwds):
        # #初始化线程,同时运行线程数量
        for i in range(self.MaxSem):
            self.all_Thread.append(Work(self.lock, self.work_queue, self.result_queue, **kwds))

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


class Work(threading.Thread):
    def __init__(self, lock, work_queue, result_queue, kwds={}):
        super().__init__(**kwds)
        self.lock = lock
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.start()

    def run(self):
        while True:
            try:
                task = self.work_queue.get(False)   # !任务异步出队 get_nowait()
            except Empty:
                break
            else:
                result = task.func(self.lock, *task.args, **task.kwds)  # 传递 list 各元素
                self.result_queue.put(result)  # 取得函数返回值
                self.work_queue.task_done()  # 通知系统任务完成


class thread_pool_maneger(object):
    '''参照htreadpool编写的自定义库 '''

    def __init__(self, items, MaxSem=99, callback=None, exc_callback=_handle_thread_exception, poll_timeout=5, kwds={}):
        self.lock = threading.RLock()
        self.work_queue = Queue()  # 任务队列
        self.result_queue = Queue()  # 结果队列
        self.all_Thread = []
        self.result_list = []
        self.stoped_thread = []
        self.all_Tasks = {}

        if MaxSem is not None:
            self.setMaxcs(MaxSem, poll_timeout=5, **kwds)
        self.add_work_queue(items, callback=callback, exc_callback=exc_callback, poll_timeout=poll_timeout)

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
                WorkThread(self.lock, self.work_queue, self.result_queue, poll_timeout=poll_timeout, **kwds)
            )

    def add_work_queue(self, items, callback=None, exc_callback=_handle_thread_exception, block=True, poll_timeout=5):
        """初始化工作队列,添加工作入队"""
        tasks = make_task_object(items, callback=callback, exc_callback=exc_callback)
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
        while True:
            if not self.all_Tasks:
                raise NoResultsPending
            elif block and not self.work_queue:
                raise NoWorkersAvailable

            if self.result_queue.empty():
                break
            else:
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


class WorkThread(threading.Thread):
    def __init__(self, lock, work_queue, result_queue, poll_timeout=5, kwds={}):
        super().__init__(**kwds)
        self.lock = lock
        self.daemon = True
        self.work_queue = work_queue
        self.result_queue = result_queue
        self._poll_timeout = poll_timeout
        self._stop_event = threading.Event()
        self.start()

    def run(self):
        """工作线程启动函数"""
        while True:
            # 检查线程是否被停止
            if self._stop_event.is_set():
                break

            # 请求队列中取出
            try:
                task = self.work_queue.get(True, self._poll_timeout)  # 可以等待添加任务
            except Empty:
                sleep(0.1)
                continue
            # 检查线程是否被停止
            if self._stop_event.is_set():
                self.work_queue.put(task)
                break

            # 执行请求队列中的请求
            try:
                result = task.func(self.lock, *task.args, **task.kwds)
                self.result_queue.put((task, result))
            except BaseException:
                task.exception = True
                self.result_queue.put((task, sys.exc_info()))

    def stop_work(self):
        """停止工作线程"""
        self._stop_event.set()


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


'''
限制线程:
    threadingSum = 200 #同步线程数
    for index in range(len(urls)):
        # 创建多线程
        TASKS = CustomThread(get_content, (index, urls[index]), threadingSum,daemon=True)

    for thread in TASKS.all_Thread:
        thread.join()  # join等待线程执行结束
        callback(thread.getResult())  # 线程结果执行回调函数


单例多线程:
    _ = [SingletonThread(get_contents, (index, urls[index])) for index in range(len(urls))]

    # 循环等待线程数量，降低到2
    while True:
        thread_num = len(enumerate())
        # print("线程数量是%d" % thread_num)
        if thread_num <= 2:
            break
        time.sleep(0.1)

    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)

'''

'''
对象	描述
Thread	表示一个执行线程的对象
Lock	锁对象
RLock	可重入锁对象，使单一线程可以（再次）获得已持有的锁（递归锁）
Condition	条件变量对象，使得一个线程等待另外一个线程满足特定的条件，比如改变状态或者某个数据值
Event　	条件变量的通用版本，任意数量的线程等待某个事件的发生，在该事件发生后所有的线程都将被激活
Semaphore	为线程间的有限资源提供一个计数器，如果没有可用资源时会被阻塞
BoundedSemaphore	于Semaphore相似，不过它不允许超过初始值
Timer	于Thread类似，不过它要在运行前等待一定时间
Barrier	创建一个障碍，必须达到指定数量的线程后才可以继续

下面是Thread类的属性和方法列表：

属性	描述
Thread类属性
name	线程名
ident	线程的标识符
daemon	布尔值，表示这个线程是否是守护线程
isDaemon()
setDaemon()

Thread(group=None, target=None, name=None, args=(), kwargs={})
    group: 线程组，目前还没有实现，库引用中提示必须是None；
    target: 要执行的方法；
    name: 线程名；
    args/kwargs: 要传入方法的参数。

Thread类方法
__init__(group=None,target=None,name=None,args=(),kwargs={},verbose=None,daemon=None)	实例化一个线程对象，需要一个可调用的target对象，以及参数args或者kwargs。还可以传递name参数。daemon的值将会设定thread.daemon的属性
start()	开始执行该线程
run()	定义线程的方法。（通常开发者应该在子类中重写）
join(timeout=None)	直至启动的线程终止之前一直挂起；除非给出了timeout(单位秒)，否则一直被阻塞
isAlive	布尔值，表示这个线程是否还存活（驼峰式命名，python2.6版本开始已被取代）
is_alive()

threading.active_count()
threading.activeCount()
获取当前活动的(alive)线程的个数。

threading.currentThread()
获取当前的线程对象（Thread object）。

threading.enumerate()
获取当前所有活动线程的列表。

threading.settrace(func)
设置一个跟踪函数，用于在run()执行之前被调用。

threading.setprofile(func)
设置一个跟踪函数，用于在run()执行完毕之后调用。

手册
https://docs.python.org/3/library/threading.html#module-threading
'''
