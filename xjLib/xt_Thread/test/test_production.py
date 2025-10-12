"""
==============================================================
Description  : production.py模块测试代码
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-10-09 10:05:00
==============================================================
"""

from __future__ import annotations

import asyncio
import random
import threading
import time
import unittest

from xt_thread.production import AsyncProduction, Production


class TestProduction(unittest.TestCase):
    """测试Production类（同步生产者-消费者模式）的功能"""

    def setUp(self):
        """测试前的准备工作"""
        self.production = None

    def tearDown(self):
        """测试后的清理工作"""
        if self.production:
            self.production.shutdown()

    def test_init(self):
        """测试初始化功能"""
        production = Production(queue_size=3)
        self.assertEqual(production.queue.maxsize, 3)
        self.assertEqual(production.tasks, 0)
        self.assertIsNone(production.error_callback)
        self.assertFalse(production.running.is_set())
        production.shutdown()

    def test_add_producer_and_consumer(self):
        """测试添加生产者和消费者功能"""
        self.production = Production(queue_size=5)

        def simple_producer():
            return 42

        def simple_consumer(item):
            return item * 2

        # 测试添加生产者
        initial_producer_count = len(self.production.producers)
        self.production.add_producer(simple_producer, 'TestProducer')
        self.assertEqual(len(self.production.producers), initial_producer_count + 1)

        # 测试添加消费者
        initial_consumer_count = len(self.production.consumers)
        self.production.add_consumer(simple_consumer, 'TestConsumer')
        self.assertEqual(len(self.production.consumers), initial_consumer_count + 1)

        # 验证线程已启动
        producer_thread = self.production.producers[-1]
        consumer_thread = self.production.consumers[-1]
        self.assertTrue(producer_thread.is_alive())
        self.assertTrue(consumer_thread.is_alive())
        self.assertEqual(producer_thread.name, 'TestProducer')
        self.assertEqual(consumer_thread.name, 'TestConsumer')

    def test_basic_producer_consumer_flow(self):
        """测试基本的生产者-消费者流程"""
        self.production = Production(queue_size=10)
        results_produced = []
        results_consumed = []

        def producer():
            item = len(results_produced) + 1
            results_produced.append(item)
            if len(results_produced) >= 5:  # 限制生产数量
                time.sleep(1)  # 停止生产更多
            return item

        def consumer(item):
            results_consumed.append(item)
            return item * 2

        self.production.add_producer(producer)
        self.production.add_consumer(consumer)

        # 运行一段时间
        time.sleep(0.5)

        # 停止并获取结果
        final_results = self.production.shutdown()

        # 验证生产和消费都有发生
        self.assertGreater(len(results_produced), 0)
        self.assertGreater(len(results_consumed), 0)
        self.assertGreater(len(final_results), 0)

    def test_error_handling_with_callback(self):
        """测试带错误回调的异常处理"""
        self.production = Production(queue_size=5)
        captured_errors = []
        captured_items = []

        def error_callback(exception, item):
            captured_errors.append(exception)
            captured_items.append(item)

        def producer():
            return 42

        def failing_consumer(item):
            raise ValueError(f'消费失败: {item}')

        self.production.set_error_callback(error_callback)
        self.production.add_producer(producer)
        self.production.add_consumer(failing_consumer)

        time.sleep(0.3)  # 让一些错误发生
        self.production.shutdown()

        # 验证错误回调被调用
        self.assertGreater(len(captured_errors), 0)
        self.assertGreater(len(captured_items), 0)

        # 验证错误类型正确
        for error in captured_errors:
            self.assertIsInstance(error, ValueError)
            self.assertIn('消费失败', str(error))

    def test_error_handling_without_callback(self):
        """测试没有错误回调时的异常处理"""
        self.production = Production(queue_size=5)

        def producer():
            return 42

        def failing_consumer(item):
            raise ValueError(f'消费失败: {item}')

        # 记录测试开始前的任务计数
        initial_tasks = self.production.tasks

        # 添加生产者和消费者
        self.production.add_producer(producer)
        self.production.add_consumer(failing_consumer)

        time.sleep(0.3)

        # 即使发生异常，系统也应该能够正常关闭
        results = self.production.shutdown()

        # 验证系统能够继续运行，没有因为异常而崩溃
        self.assertIsNotNone(results)
        # 验证任务已经被处理（虽然可能失败）
        self.assertGreater(self.production.tasks, initial_tasks)

    def test_get_methods(self):
        """测试获取结果和状态的方法"""
        self.production = Production(queue_size=5)

        def producer():
            time.sleep(0.1)
            return 10

        def consumer(item):
            time.sleep(0.1)
            return item * 5

        self.production.add_producer(producer)
        self.production.add_consumer(consumer)

        # 等待一些结果产生
        time.sleep(0.3)

        # 测试获取任务计数
        task_count = self.production.get_task_count()
        self.assertGreaterEqual(task_count, 0)

        # 测试获取结果列表
        results = self.production.get_result_list()
        self.assertIsInstance(results, list)

        # 如果有结果，测试获取单个结果
        if results:
            self.assertEqual(results[0], 50)  # 10 * 5

    def test_queue_size_limit(self):
        """测试队列大小限制"""
        production = Production(queue_size=2)

        def fast_producer():
            return random.randint(1, 100)

        def slow_consumer(item):
            time.sleep(0.2)  # 消费很慢
            return item

        production.add_producer(fast_producer)
        production.add_consumer(slow_consumer)

        time.sleep(0.5)  # 让生产者尝试填满队列

        # 队列大小不应超过限制
        self.assertLessEqual(production.queue.qsize(), 2)

        production.shutdown()

    def test_multiple_producers_consumers(self):
        """测试多个生产者和消费者"""
        self.production = Production(queue_size=20)
        counter = {'value': 0}
        lock = threading.Lock()

        def producer():
            with lock:
                counter['value'] += 1
                return counter['value']

        def consumer(item):
            return item * 3

        # 添加多个生产者和消费者
        for i in range(2):
            self.production.add_producer(producer, f'Producer-{i}')

        for i in range(2):
            self.production.add_consumer(consumer, f'Consumer-{i}')

        # 运行一段时间
        time.sleep(0.5)

        # 停止并获取结果
        results = self.production.shutdown()

        # 验证多个线程工作
        self.assertEqual(len(self.production.producers), 2)
        self.assertEqual(len(self.production.consumers), 2)
        self.assertGreater(len(results), 0)


class TestAsyncProduction(unittest.TestCase):
    """测试AsyncProduction类（异步生产者-消费者模式）的功能"""

    def setUp(self):
        """测试前的准备工作"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """测试后的清理工作"""
        try:
            # 清理所有未完成的任务
            pending = asyncio.all_tasks(self.loop)
            for task in pending:
                task.cancel()
            if pending:
                self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        finally:
            self.loop.close()

    def test_init(self):
        """测试初始化功能"""

        async def test():
            production = AsyncProduction(queue_size=3)
            self.assertEqual(production.queue.maxsize, 3)
            self.assertFalse(production.running)
            self.assertEqual(len(production.producer_tasks), 0)
            self.assertEqual(len(production.consumer_tasks), 0)
            self.assertIsNone(production.error_callback)

        self.loop.run_until_complete(test())

    def test_start_and_shutdown(self):
        """测试启动和关闭系统功能"""

        async def test():
            production = AsyncProduction()

            async def producer():
                await asyncio.sleep(0.01)
                return 42

            async def consumer(item):
                await asyncio.sleep(0.01)
                return item * 2

            # 测试启动
            await production.start(1, 1, producer, consumer)

            # 验证系统已启动
            self.assertTrue(production.running)
            self.assertEqual(len(production.producer_tasks), 1)
            self.assertEqual(len(production.consumer_tasks), 1)

            # 验证任务都在运行
            for task in production.producer_tasks + production.consumer_tasks:
                self.assertFalse(task.done())

            # 测试关闭
            await production.shutdown()

            # 验证系统已停止
            self.assertFalse(production.running)
            self.assertEqual(len(production.producer_tasks), 0)
            self.assertEqual(len(production.consumer_tasks), 0)

        self.loop.run_until_complete(test())

    def test_basic_flow(self):
        """测试基本的异步生产者-消费者流程"""

        async def test():
            production = AsyncProduction(queue_size=10)
            produced_count = 0
            consumed_count = 0

            async def producer():
                nonlocal produced_count
                if produced_count >= 3:  # 限制生产数量
                    await asyncio.sleep(1)  # 长时间休眠停止生产
                    return None

                await asyncio.sleep(0.01)
                produced_count += 1
                return produced_count

            async def consumer(item):
                nonlocal consumed_count
                await asyncio.sleep(0.02)
                consumed_count += 1
                return item * 2

            await production.start(1, 1, producer, consumer)

            # 运行一段时间让生产者产生一些项目
            await asyncio.sleep(0.2)

            await production.shutdown()

            # 验证生产和消费都有发生
            self.assertGreater(produced_count, 0)
            self.assertGreater(consumed_count, 0)

        self.loop.run_until_complete(test())

    def test_error_handling_with_callback(self):
        """测试带错误回调的异常处理"""

        async def test():
            production = AsyncProduction()
            captured_errors = []
            captured_items = []

            async def error_callback(exception, item):
                captured_errors.append(exception)
                captured_items.append(item)

            async def producer():
                await asyncio.sleep(0.01)
                return 42

            async def failing_consumer(item):
                raise ValueError(f'消费失败: {item}')

            await production.set_error_callback(error_callback)
            await production.start(1, 1, producer, failing_consumer)

            await asyncio.sleep(0.1)
            await production.shutdown()

            # 验证错误回调被调用
            self.assertGreater(len(captured_errors), 0)
            self.assertGreater(len(captured_items), 0)

            # 验证错误类型正确
            for error in captured_errors:
                self.assertIsInstance(error, ValueError)
                self.assertIn('消费失败', str(error))

        self.loop.run_until_complete(test())

    def test_error_handling_without_callback(self):
        """测试没有错误回调时的异常处理"""

        async def test():
            production = AsyncProduction()

            async def producer():
                await asyncio.sleep(0.01)
                return 42

            async def failing_consumer(item):
                raise ValueError(f'消费失败: {item}')

            # 添加生产者和消费者
            await production.start(1, 1, producer, failing_consumer)
            await asyncio.sleep(0.1)

            # 即使发生异常，系统也应该能够正常关闭
            await production.shutdown()

            # 验证系统已停止
            self.assertFalse(production.running)
            self.assertEqual(len(production.producer_tasks), 0)
            self.assertEqual(len(production.consumer_tasks), 0)

        self.loop.run_until_complete(test())

    def test_duplicate_start_protection(self):
        """测试重复启动保护"""

        async def test():
            production = AsyncProduction()

            async def producer():
                return 1

            async def consumer(item):
                return item

            # 第一次启动
            await production.start(1, 1, producer, consumer)
            initial_tasks = len(production.producer_tasks) + len(production.consumer_tasks)

            # 第二次启动（应该被忽略）
            await production.start(2, 2, producer, consumer)
            final_tasks = len(production.producer_tasks) + len(production.consumer_tasks)

            # 任务数量不应该改变
            self.assertEqual(initial_tasks, final_tasks)

            await production.shutdown()

        self.loop.run_until_complete(test())

    def test_duplicate_shutdown_protection(self):
        """测试重复关闭保护"""

        async def test():
            production = AsyncProduction()

            async def producer():
                return 1

            async def consumer(item):
                return item

            await production.start(1, 1, producer, consumer)

            # 第一次关闭
            await production.shutdown()

            # 验证系统已停止
            first_running_state = production.running

            # 第二次关闭（应该被忽略）
            await production.shutdown()

            # 验证运行状态没有变化
            second_running_state = production.running

            # 第二次关闭不应该改变运行状态
            self.assertFalse(first_running_state)
            self.assertFalse(second_running_state)
            self.assertFalse(production.running)

        self.loop.run_until_complete(test())

    def test_wait_until_done_success(self):
        """测试等待完成成功功能"""

        async def test():
            production = AsyncProduction()
            task_count = 0

            async def producer():
                nonlocal task_count
                if task_count >= 2:  # 只生产2个项目
                    await asyncio.sleep(10)  # 长时间休眠
                    return None

                await asyncio.sleep(0.01)
                task_count += 1
                return task_count

            async def consumer(item):
                await asyncio.sleep(0.01)
                return item

            await production.start(1, 1, producer, consumer)

            # 等待一段时间让任务完成
            await asyncio.sleep(0.1)

            # 停止生产者
            for task in production.producer_tasks:
                task.cancel()

            # 等待队列清空
            done = await production.wait_until_done(timeout=1)
            self.assertTrue(done)

            await production.shutdown()

        self.loop.run_until_complete(test())


class TestProductionIntegration(unittest.TestCase):
    """集成测试：测试Production和AsyncProduction的综合使用场景"""

    def test_sync_production_stress_test(self):
        """同步生产者-消费者压力测试"""
        production = Production(queue_size=20)
        counter = {'produced': 0, 'consumed': 0}
        lock = threading.Lock()

        def producer():
            with lock:
                if counter['produced'] >= 50:  # 限制生产数量
                    time.sleep(1)
                    return counter['produced']
                counter['produced'] += 1
                return counter['produced']

        def consumer(item):
            time.sleep(0.001)  # 模拟少量工作
            with lock:
                counter['consumed'] += 1
            return item * 2

        # 添加多个生产者和消费者
        for i in range(3):
            production.add_producer(producer)
        for i in range(2):
            production.add_consumer(consumer)

        # 运行较长时间
        time.sleep(1)

        results = production.shutdown()

        # 验证大量任务被处理
        self.assertGreater(len(results), 10)
        self.assertGreater(counter['produced'], 10)
        self.assertGreater(counter['consumed'], 10)

    def test_async_production_stress_test(self):
        """异步生产者-消费者压力测试"""

        async def stress_test():
            production = AsyncProduction(queue_size=50)
            counter = {'produced': 0, 'consumed': 0}

            async def producer():
                if counter['produced'] >= 20:  # 限制生产数量
                    await asyncio.sleep(10)
                    return None

                await asyncio.sleep(0.001)
                counter['produced'] += 1
                return counter['produced']

            async def consumer(item):
                await asyncio.sleep(0.002)
                counter['consumed'] += 1
                return item * 2

            await production.start(2, 2, producer, consumer)

            # 运行较长时间
            await asyncio.sleep(0.5)

            await production.shutdown()

            # 验证大量任务被处理
            self.assertGreater(counter['produced'], 5)
            self.assertGreater(counter['consumed'], 5)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(stress_test())
        finally:
            try:
                # 清理所有未完成的任务
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            finally:
                loop.close()


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)
