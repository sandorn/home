import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from queue import Queue
from threading import Lock
from typing import Any, Callable, List

import psutil
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

    def __enter__(self):
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
        self.queue.join()  # 等待队列清空
        print("生产系统已关闭")


class ThreadPoolManager:
    """全局线程池单例管理
    使用示例：
    with ThreadPoolManager.get_pool() as executor:
        future = executor.submit(task_function, args)
    """

    _instance: ThreadPoolExecutor | None = None
    _lock = Lock()

    @classmethod
    def get_pool(cls, max_workers: int | None = None) -> ThreadPoolExecutor:
        """获取线程池实例
        :param max_workers: None-自动计算(IO密集型推荐)，具体数值适用于CPU密集型任务
        """
        with cls._lock:
            if not cls._instance or cls._instance._max_workers != max_workers:
                # 根据任务类型自动优化线程数
                base_workers = cpu_count() or 4
                if max_workers is None:
                    max_workers = base_workers * 4  # 默认IO密集型配置
                cls._instance = ThreadPoolExecutor(max_workers=max_workers)
            return cls._instance

    @classmethod
    def shutdown(cls):
        """安全关闭线程池"""
        if cls._instance:
            cls._instance.shutdown(wait=True)
            cls._instance = None

if __name__ == "__main__":

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

    # Production()

    def func2():
        # 定义一个简单的任务函数
        def DynamicT(task_id):
            """模拟一个耗时的任务"""
            import random

            sleep_time = random.uniform(0.1, 1.0)  # 随机等待一段时间
            thread_print(f"任务 {task_id} 开始，预计耗时 {sleep_time:.2f} 秒")
            time.sleep(sleep_time)
            thread_print(f"任务 {task_id} 完成")

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

    from concurrent.futures import as_completed

    def tpoolmana_test():
        def process_data(data):
            # 数据处理逻辑
            print(f"Processing data: {data}")
            return f"transformed_{data}"

        # 获取线程池实例
        with ThreadPoolManager.get_pool() as executor:
            futures = [executor.submit(process_data, d) for d in range(10)]
            results = [f.result() for f in as_completed(futures)]
            print(results)  # 输出处理后的结果列表

        # 安全关闭线程池
        ThreadPoolManager.shutdown()

    # tpoolmana_test()