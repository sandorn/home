# !/usr/bin/env python
"""
==============================================================
Description  : 生产者-消费者模式实现 - 提供同步和异步版本的任务处理框架
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-08 12:17:17
LastEditTime : 2025-09-06 21:00:00
FilePath     : /CODE/xjLib/xt_thread/production.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- Production：同步多线程生产者-消费者模式实现
- AsyncProduction：异步协程生产者-消费者模式实现

主要特性：
- 支持动态添加多个生产者和消费者
- 任务队列管理，自动处理队列满/空的情况
- 完整的异常捕获和处理机制
- 优雅的系统关闭流程
- 结果收集和管理功能
- 适用于IO密集型和计算密集型任务的并行处理
==============================================================
"""

from __future__ import annotations

import asyncio
import queue
import threading
import time
from collections.abc import Callable, Coroutine
from random import randint
from typing import Any


class Production:
    """
    同步多线程生产者-消费者模式实现

    提供一个基于多线程的任务处理框架，支持动态添加多个生产者和消费者线程，
    适用于需要高效处理批量任务的场景。

    Args:
        queue_size: 任务队列的最大容量，默认为10

    Example:
        >>> def producer():
        ...     return random.randint(1, 100)
        >>> def consumer(item):
        ...     return item * 2
        >>> production = Production(queue_size=5)
        >>> production.add_producer(producer)
        >>> production.add_consumer(consumer)
        >>> time.sleep(2)
        >>> results = production.shutdown()
    """

    def __init__(self, queue_size: int = 10):
        """初始化生产系统

        Args:
            queue_size: 任务队列的最大容量，默认为10
        """
        self.queue = queue.Queue(maxsize=queue_size)
        self.res_queue = queue.Queue()
        self.running = threading.Event()
        self.producers: list[threading.Thread] = []
        self.consumers: list[threading.Thread] = []
        self.tasks = 0
        self.error_callback: Callable | None = None

    def add_producer(self, producer_fn: Callable[[], Any], name: str = None) -> None:
        """添加生产者线程

        Args:
            producer_fn: 生产者函数，无参数，返回待处理的任务项
            name: 线程名称，默认为自动生成的名称

        Example:
            >>> production.add_producer(lambda: random.randint(1, 100), 'NumberProducer')
        """
        producer = threading.Thread(
            target=self._producer_wrapper,
            args=(producer_fn,),
            name=name or f'Producer-{len(self.producers)}',
            daemon=True,  # 设置为守护线程，避免阻止程序退出
        )
        self.producers.append(producer)
        producer.start()

    def add_consumer(self, consumer_fn: Callable[[Any], Any], name: str = None) -> None:
        """添加消费者线程

        Args:
            consumer_fn: 消费者函数，接收任务项参数，返回处理结果
            name: 线程名称，默认为自动生成的名称

        Example:
            >>> production.add_consumer(lambda x: x * 2, 'DoubleProcessor')
        """
        consumer = threading.Thread(
            target=self._consumer_wrapper,
            args=(consumer_fn,),
            name=name or f'Consumer-{len(self.consumers)}',
            daemon=True,  # 设置为守护线程，避免阻止程序退出
        )
        self.consumers.append(consumer)
        consumer.start()

    def _producer_wrapper(self, producer_fn: Callable[[], Any]) -> None:
        """生产者包装函数，处理异常和停止信号

        持续调用生产者函数生成任务项，并将其放入任务队列中，直到收到停止信号或发生异常。

        Args:
            producer_fn: 生产者函数，无参数，返回待处理的任务项
        """
        while not self.running.is_set():
            try:
                _item = producer_fn()
                self.queue.put(_item, timeout=1)  # 设置超时，定期检查停止信号
                self.tasks += 1
            except queue.Full:
                continue  # 队列满时继续尝试
            except Exception as e:
                print(f'生产者发生错误: {e}')
                break

    def _consumer_wrapper(self, consumer_fn: Callable[[Any], Any]) -> None:
        """消费者包装函数，处理异常和停止信号，确保消费完队列后退出

        持续从任务队列中获取任务项并调用消费者函数处理，直到队列清空且收到停止信号。

        Args:
            consumer_fn: 消费者函数，接收任务项参数，返回处理结果
        """
        while not (self.running.is_set() and self.queue.empty()):
            try:
                item = self.queue.get(timeout=1)  # 设置超时，定期检查停止信号
                try:
                    _res = consumer_fn(item)
                    self.res_queue.put(_res)
                    self.tasks -= 1
                except Exception as e:
                    if self.error_callback:
                        self.error_callback(e, item)
                    else:
                        print(f'消费失败: {e}')
                finally:
                    self.queue.task_done()  # 标记任务完成
            except queue.Empty:
                continue  # 队列为空时继续尝试

    def set_error_callback(self, callback: Callable[[Exception, Any], None]) -> None:
        """设置错误处理回调函数

        Args:
            callback: 接收异常对象和失败的任务项作为参数的回调函数

        Example:
            >>> production.set_error_callback(lambda e, item: print(f'处理{item}时出错: {e}'))
        """
        self.error_callback = callback

    def shutdown(self) -> list[Any]:
        """停止所有生产者和消费者，等待队列消费完毕

        Returns:
            List[Any]: 所有处理结果的列表

        Example:
            >>> results = production.shutdown()
            >>> print(f'共处理了{len(results)}个任务')
        """
        self.running.set()  # 发送停止信号，生产者停止生产
        for thread in self.producers:
            thread.join(timeout=1)  # 等待所有生产者线程结束，设置超时避免永久阻塞
        for thread in self.consumers:
            thread.join(timeout=1)  # 等待所有消费者线程结束，设置超时避免永久阻塞
        self.queue.join()  # 等待队列清空
        _res_list = list(self.res_queue.queue)
        self.res_queue.queue.clear()
        print('生产系统已关闭')
        return _res_list

    def get_result(self) -> Any:
        """从结果队列中获取一个结果（阻塞直到有结果可用）

        Returns:
            Any: 消费者处理后的结果

        Example:
            >>> result = production.get_result()
        """
        return self.res_queue.get()

    def get_result_list(self) -> list[Any]:
        """获取当前所有的处理结果列表

        Returns:
            List[Any]: 所有已处理完成的结果列表

        Example:
            >>> current_results = production.get_result_list()
        """
        return list(self.res_queue.queue)

    def get_task_count(self) -> int:
        """获取当前待处理的任务数量

        Returns:
            int: 待处理的任务数量

        Example:
            >>> if production.get_task_count() > 0:
            ...     print(f'还有{production.get_task_count()}个任务未完成')
        """
        return self.tasks


class AsyncProduction:
    """
    异步协程生产者-消费者模式实现

    提供一个基于asyncio的异步任务处理框架，使用协程而非线程来实现生产者-消费者模式，
    特别适合IO密集型任务的高效处理。

    Args:
        queue_size: 异步任务队列的最大容量，默认为10

    Example:
        >>> async def producer():
        ...     await asyncio.sleep(0.1)
        ...     return random.randint(1, 100)
        >>> async def consumer(item):
        ...     await asyncio.sleep(0.2)
        ...     return item * 2
        >>> async def main():
        ...     production = AsyncProduction(queue_size=5)
        ...     await production.start(2, 3, producer, consumer)
        ...     await asyncio.sleep(2)
        ...     await production.stop()
        >>> asyncio.run(main())
    """

    def __init__(self, queue_size: int = 10):
        """初始化异步生产系统

        Args:
            queue_size: 异步任务队列的最大容量，默认为10
        """
        self.queue = asyncio.Queue(maxsize=queue_size)
        self.producer_tasks: list[asyncio.Task] = []
        self.consumer_tasks: list[asyncio.Task] = []
        self.running = False
        self.error_callback: Callable[[Exception, Any], Coroutine] | None = None

    async def start(
        self,
        num_producers: int,
        num_consumers: int,
        producer_fn: Callable[[], Coroutine[Any, Any, Any]],
        consumer_fn: Callable[[Any], Coroutine[Any, Any, Any]],
    ) -> None:
        """启动异步生产消费系统

        Args:
            num_producers: 要创建的生产者协程数量
            num_consumers: 要创建的消费者协程数量
            producer_fn: 异步生产者函数，无参数，返回待处理的任务项
            consumer_fn: 异步消费者函数，接收任务项参数，返回处理结果

        Example:
            >>> await production.start(num_producers=2, num_consumers=3, producer_fn=async_producer, consumer_fn=async_consumer)
        """
        if self.running:
            return  # 防止重复启动

        self.running = True
        # 创建任务并保存引用
        self.producer_tasks = [asyncio.create_task(self._producer_loop(producer_fn)) for _ in range(num_producers)]
        self.consumer_tasks = [asyncio.create_task(self._consumer_loop(consumer_fn)) for _ in range(num_consumers)]

    async def set_error_callback(self, callback: Callable[[Exception, Any], Coroutine]) -> None:
        """设置错误处理回调函数

        Args:
            callback: 异步回调函数，接收异常对象和失败的任务项作为参数

        Example:
            >>> async def error_handler(e, item):
            ...     print(f'处理{item}时出错: {e}')
            >>> await production.set_error_callback(error_handler)
        """
        self.error_callback = callback

    async def _producer_loop(self, producer_fn: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        """生产者协程循环，持续生成任务项

        Args:
            producer_fn: 异步生产者函数，无参数，返回待处理的任务项
        """
        while self.running:
            try:
                item = await producer_fn()
                await self.queue.put(item)
            except asyncio.CancelledError:
                break  # 任务被取消时退出循环
            except Exception as e:
                print(f'生产者异常: {e}')
                break  # 发生其他异常时退出循环

    async def _consumer_loop(self, consumer_fn: Callable[[Any], Coroutine[Any, Any, Any]]) -> None:
        """消费者协程循环，持续处理任务项

        Args:
            consumer_fn: 异步消费者函数，接收任务项参数，返回处理结果
        """
        while self.running:
            try:
                item = await asyncio.wait_for(
                    self.queue.get(),
                    timeout=0.5,  # 关键优化：避免永久阻塞，定期检查running状态
                )
                try:
                    await consumer_fn(item)
                except Exception as e:
                    if self.error_callback:
                        await self.error_callback(e, item)
                    else:
                        print(f'消费者异常: {e}')
                finally:
                    self.queue.task_done()  # 标记任务完成
            except TimeoutError:
                continue  # 超时后继续循环，检查running状态
            except asyncio.CancelledError:
                break  # 任务被取消时退出循环
            except Exception as e:
                print(f'消费者循环异常: {e}')
                break  # 发生其他异常时退出循环

    async def shutdown(self) -> None:
        """安全停止异步生产消费系统

        停止所有生产者和消费者协程，清理资源，确保系统优雅退出。

        Example:
            >>> await production.stop()
        """
        if not self.running:
            return  # 防止重复停止

        self.running = False
        # 取消所有任务
        for task in self.producer_tasks + self.consumer_tasks:
            if not task.done():
                task.cancel()
        # 等待任务清理，允许异常被捕获和处理
        await asyncio.gather(*self.producer_tasks, *self.consumer_tasks, return_exceptions=True)
        # 清空任务引用列表
        self.producer_tasks.clear()
        self.consumer_tasks.clear()
        print('异步生产系统已完全停止')

    async def wait_until_done(self, timeout: float | None = None) -> bool:
        """等待直到队列为空

        Args:
            timeout: 等待超时时间（秒），None表示无限等待

        Returns:
            bool: 如果队列已清空返回True，超时返回False

        Example:
            >>> if await production.wait_until_done(timeout=5):
            ...     print('所有任务已处理完成')
            ... else:
            ...     print('等待超时')
        """
        try:
            await asyncio.wait_for(self.queue.join(), timeout=timeout)
            return True
        except TimeoutError:
            return False


if __name__ == '__main__':
    """测试代码 - 演示同步和异步生产消费系统的使用方法"""
    import asyncio
    import random

    def run_sync_test():
        """测试同步生产消费系统"""
        print('\n=== 开始同步生产消费系统测试 ===')

        def producer_function():
            """生产者生成随机数"""
            time.sleep(random.uniform(0.1, 0.5))  # 模拟生产时间
            item = random.randint(1, 100)  # 生成随机数
            print(f'生产者生成: {item}')
            return item

        def consumer_function(item):
            """消费者处理生成的随机数"""
            time.sleep(random.uniform(0.1, 0.5))  # 模拟消费时间
            print(f'消费者消费: {item}')
            # 模拟偶尔的错误情况，测试错误处理
            if item % 7 == 0:
                raise ValueError(f'测试错误: 数字{item}能被7整除')
            return item * 2  # 返回处理结果

        def error_handler(e, item):
            """处理消费过程中的错误"""
            print(f'处理{item}时发生错误: {e}')

        # 创建生产系统实例
        production_system = Production(queue_size=5)
        production_system.set_error_callback(error_handler)

        # 添加生产者和消费者
        for _ in range(3):  # 添加3个生产者
            production_system.add_producer(producer_function)

        for _ in range(2):  # 添加2个消费者
            production_system.add_consumer(consumer_function)

        # 运行一段时间后停止
        print(f'系统启动，当前任务数: {production_system.get_task_count()}')
        time.sleep(2)  # 让生产和消费运行2秒

        # 检查任务状态
        print(f'运行中，当前任务数: {production_system.get_task_count()}')
        current_results = production_system.get_result_list()
        print(f'当前已完成的结果数: {len(current_results)}')
        if current_results:
            print(f'当前已完成的部分结果: {current_results[:3]}')

        # 测试单独获取结果
        if not production_system.res_queue.empty():
            single_result = production_system.get_result()
            print(f'单独获取的一个结果: {single_result}')

        # 停止系统并获取结果
        results = production_system.shutdown()
        print(f'测试完成，共处理了{len(results)}个任务')
        print(f'前5个结果: {results[:5] if len(results) >= 5 else results}')

    async def run_async_test():
        """测试异步生产消费系统"""
        print('\n=== 开始异步生产消费系统测试 ===')

        async def mock_producer():
            """模拟生产者：生成随机数"""
            await asyncio.sleep(0.1)  # 模拟耗时操作
            item = randint(1, 100)
            print(f'异步生产者生成: {item}')
            return item

        async def mock_consumer(item):
            """模拟消费者：处理数据"""
            await asyncio.sleep(0.2)  # 模拟耗时操作
            print(f'异步消费者处理: {item}')
            # 模拟偶尔的错误情况，测试错误处理
            if item % 7 == 0:
                raise ValueError(f'测试错误: 数字{item}能被7整除')
            return item * 2

        async def error_handler(e, item):
            """处理异步消费过程中的错误"""
            print(f'异步处理{item}时发生错误: {e}')

        # 创建异步生产系统
        system = AsyncProduction(queue_size=5)
        await system.set_error_callback(error_handler)

        # 测试重复启动保护
        await system.start(num_producers=2, num_consumers=3, producer_fn=mock_producer, consumer_fn=mock_consumer)

        print('异步系统启动成功')
        # 测试再次启动（应该不会有问题，因为有重复启动保护）
        await system.start(3, 4, mock_producer, mock_consumer)
        print('验证重复启动保护正常工作')

        # 运行一段时间
        await asyncio.sleep(2)  # 运行2秒

        # 等待队列处理完成
        print('等待所有任务处理完成...')
        done = await system.wait_until_done(timeout=3)
        print(f'队列处理{"完成" if done else "超时"}')

        # 停止系统
        await system.shutdown()
        print('异步测试完成')

        # 测试重复停止保护
        await system.shutdown()
        print('验证重复停止保护正常工作')

    # 运行同步测试
    run_sync_test()

    # 运行异步测试
    asyncio.run(run_async_test())

    print('\n=== 所有测试完成 ===')
