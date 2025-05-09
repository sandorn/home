# !/usr/bin/env python
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-08 12:17:17
LastEditTime : 2025-05-09 10:04:18
FilePath     : /CODE/xjLib/xt_thread/production.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import queue
import threading
import time
from typing import List

from xt_thread import thread_print


class Production:
    def __init__(self, queue_size: int = 10):
        """初始化生产系统"""
        self.queue = queue.Queue(maxsize=queue_size)
        self.res_queue = queue.Queue()
        self.running = threading.Event()
        self.producers: List[threading.Thread] = []
        self.consumers: List[threading.Thread] = []
        self.tasks = 0

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
                _item = producer_fn()
                self.queue.put(_item, timeout=1)
                self.tasks += 1
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
                    _res = consumer_fn(item)
                    self.res_queue.put(_res)
                    self.tasks -= 1
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
        _res_list = list(self.res_queue.queue)
        self.res_queue.queue.clear()
        print("生产系统已关闭")
        return _res_list
    
    def getResult(self):
        """获取结果"""
        return self.res_queue.get()

    def getResultList(self):
        """获取结果列表"""
        return list(self.res_queue.queue)
    
    def getTask(self):
        """获取任务数量"""
        return self.tasks


if __name__ == "__main__":

    def test(*arg, **kwargs):
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
            return item * 2  # 返回处理结果，这里简单返回两倍的数

        # 创建生产系统实例
        production_system = Production(queue_size=5)

        # 添加生产者和消费者
        for _ in range(3):  # 添加3个生产者
            production_system.add_producer(producer_function)

        for _ in range(2):  # 添加2个消费者
            production_system.add_consumer(consumer_function)

        # 运行一段时间后停止
        time.sleep(2)  # 让生产和消费运行2秒
        return production_system.shutdown()  # 停止所有生产者和消费者

    print(999999999999999,test())
