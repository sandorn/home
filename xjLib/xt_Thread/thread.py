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
import queue
import threading
import time
from queue import Empty, Queue
from threading import Event, Thread, main_thread
from threading import enumerate as thread_enumerate
from time import sleep
from typing import Any, Callable, List

import psutil
import wrapt
from xt_class import ItemGetMixin
from xt_singleon import SingletonMixin, singleton_decorator_factory
from xt_thread import thread_print


class DynamicThreadPool:
    def __init__(
        self, min_workers: int = 2, max_workers: int = 10, queue_size: int = 100
    ) -> None:
        """
        动态调整的线程池实现

        :param min_workers: 最小工作线程数（保持活跃）
        :param max_workers: 最大工作线程数（根据负载自动调整）
        :param queue_size: 任务队列最大容量
        """
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.task_queue = Queue(maxsize=queue_size)
        self.workers = []
        self.isrunning = True
        self.lock = threading.Lock()

        # 启动监控线程
        self.monitor = threading.Thread(target=self._monitor_resources)
        self.monitor.start()

        # 启动初始工作线程
        self._adjust_worker_count(min_workers)

    def __enter__(self) :
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """安全关闭线程池"""
        self.shutdown(wait=True)

    def _monitor_resources(self):
        """监控系统资源和任务队列，动态调整线程数"""
        while self.isrunning:
            cpu_percent = psutil.cpu_percent()
            queue_size = self.task_queue.qsize()
            current_workers = len(self.workers)

            if queue_size > current_workers * 2 and cpu_percent < 80:
                # 队列积压且CPU资源充足，增加线程
                self._adjust_worker_count(min(current_workers + 2, self.max_workers))
            elif queue_size < current_workers and current_workers > self.min_workers:
                # 任务较少，减少线程
                self._adjust_worker_count(max(current_workers - 1, self.min_workers))

            time.sleep(2)  # 监控间隔

    def _adjust_worker_count(self, target_count: int):
        """调整工作线程数量"""
        with self.lock:
            current_count = len(self.workers)
            if target_count > current_count:
                # 增加工作线程
                for _ in range(target_count - current_count):
                    worker = threading.Thread(target=self._worker_loop)
                    worker.start()
                    self.workers.append(worker)
            elif target_count < current_count:
                # 标记多余的工作线程退出
                for _ in range(current_count - target_count):
                    self.task_queue.put(None)

    def _worker_loop(self):
        """工作线程主循环"""
        while self.isrunning or not self.task_queue.empty():
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # 退出信号
                    with self.lock:
                        self.workers.remove(threading.current_thread())
                    break

                func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"任务执行异常: {e}")
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """提交任务到线程池"""
        if not self.isrunning:
            raise RuntimeError("线程池已关闭")
        self.task_queue.put((func, args, kwargs))

    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        self.isrunning = False  # 先停止接受新任务
        if wait:
            # 等待队列处理完毕
            while not self.task_queue.empty():
                time.sleep(0.1)
            # 等待所有工作线程完成当前任务
            self.task_queue.join()
            # 发送终止信号给工作线程
            for _ in range(len(self.workers)):
                self.task_queue.put(None)
            # 等待线程终止
            for worker in self.workers:
                worker.join()
        # 确保监控线程终止
        self.monitor.join()
        # 清空工作线程列表
        self.workers.clear()


class ProductionSystem:
    def __init__(self, queue_size: int = 10):
        """初始化生产系统"""
        self.queue = queue.Queue(maxsize=queue_size)
        self.running = threading.Event()
        self.producers: List[threading.Thread] = []
        self.consumers: List[threading.Thread] = []

    def add_producer(self, producer_fn, name: str = None):
        """添加生产者线程"""
        producer = threading.Thread(
            target=self._producer_wrapper,
            args=(producer_fn,),
            name=name or f"Producer-{len(self.producers)}",
        )
        self.producers.append(producer)
        producer.start()

    def add_consumer(self, consumer_fn, name: str = None):
        """添加消费者线程"""
        consumer = threading.Thread(
            target=self._consumer_wrapper,
            args=(consumer_fn,),
            name=name or f"Consumer-{len(self.consumers)}",
        )
        self.consumers.append(consumer)
        consumer.start()

    def _producer_wrapper(self, producer_fn):
        """生产者包装函数，处理异常和停止信号"""
        while not self.running.is_set():
            try:
                item = producer_fn()
                self.queue.put(item, timeout=1)
            except queue.Full:
                continue
            except Exception as e:
                print(f"生产者发生错误: {e}")
                break

    def _consumer_wrapper(self, consumer_fn):
        """消费者包装函数（增强版），处理异常和停止信号，确保消费完队列后退出"""
        while not (self.running.is_set() and self.queue.empty()):
            try:
                item = self.queue.get(timeout=1)
                try:
                    consumer_fn(item)
                except Exception as e:
                    if hasattr(self, "error_callback"):
                        self.error_callback(e, item)
                    else:
                        print(f"消费失败: {e}")
                finally:
                    self.queue.task_done()
            except queue.Empty:
                continue

    def shutdown(self):
        """停止所有生产者和消费者，等待队列消费完毕"""
        self.running.set()  # 发送停止信号，生产者停止生产
        for thread in self.producers:
            thread.join()  # 等待所有生产者线程结束
        for thread in self.consumers:
            thread.join()  # 等待所有消费者线程结束


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
    # #使用类装饰器 singleton_decorator_factory 转换为单例类
    _cls = singleton_decorator_factory(parent_cls)
    _cls.__name__ = new_class_name  # @单例线程运行结束判断依据
    _cls.result_list = []  # @单独配置结果字典
    _cls.wait_completed, _cls.getAllResult = _cls.getAllResult, _cls.wait_completed
    return _cls


SigThread = _create_singleton_thread_class(CustomThread, "SigThread")
SigThreadQ = _create_singleton_thread_class(CustomThread_Queue, "SigThreadQ")

if __name__ == "__main__":

    def func_print(*arg, **kwargs):
        thread_print(*arg, **kwargs)
        sleep(2)
        return arg

    # a = SigThread(print, 111111111111111)
    # print(22222222222, a.getResult(), a.__name__, type(a))
    # b = SigThread(func, 2, 3)
    # print(33333333333, b.getResult())
    # c = SigThreadQ([func, 2, 3])
    # print(44444444444, c.getResult(), c.__name__, type(c))
    """
    tpool = ThreadPoolWraps(200)

    for index, arg in enumerate(args, start=1):
        tpool(func)(arg, kwargs)
    text_list = tpool.wait_completed()
    """

    def Production(*arg, **kwargs):
        # 定义生产者函数

        import random

        def producer_function():
            """生产者生成随机数"""
            time.sleep(random.uniform(0.1, 0.5))  # 模拟生产时间
            item = random.randint(1, 100)  # 生成随机数
            thread_print(f"生产者生成: {item}")
            return item

        # 定义消费者函数
        def consumer_function(item):
            """消费者处理生成的随机数"""
            time.sleep(random.uniform(0.1, 0.5))  # 模拟消费时间
            thread_print(f"消费者消费: {item}")

        # 创建生产系统实例
        production_system = ProductionSystem(queue_size=5)

        # 添加生产者和消费者
        for _ in range(3):  # 添加3个生产者
            production_system.add_producer(producer_function)

        for _ in range(2):  # 添加2个消费者
            production_system.add_consumer(consumer_function)

        # 运行一段时间后停止
        time.sleep(2)  # 让生产和消费运行2秒
        production_system.shutdown()  # 停止所有生产者和消费者
        thread_print("生产系统已停止。")

    Production()

    # 定义一个简单的任务函数
    def DynamicT(task_id):
        """模拟一个耗时的任务"""
        import random

        sleep_time = random.uniform(0.1, 1.0)  # 随机等待一段时间
        thread_print(f"任务 {task_id} 开始，预计耗时 {sleep_time:.2f} 秒")
        time.sleep(sleep_time)
        thread_print(f"任务 {task_id} 完成")

    def func2():
        # 创建动态线程池实例
        thread_pool = DynamicThreadPool(min_workers=2, max_workers=5, queue_size=10)

        # 提交多个任务
        for i in range(15):
            thread_pool.submit(DynamicT, i)

        # 运行一段时间后关闭线程池
        # time.sleep(10)  # 让任务运行一段时间
        thread_pool.shutdown(wait=True)  # 等待所有任务完成后关闭线程池
        thread_print("动态线程池已关闭。")

    # func2()
