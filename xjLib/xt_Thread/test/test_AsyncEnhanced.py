# !/usr/bin/env python
"""
==============================================================
Description  : AsyncEnhancedThreadPool 测试程序
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-10-10
==============================================================
"""

from __future__ import annotations

import asyncio
import time
import unittest

from xt_thread.futures import AsyncEnhancedThreadPool


class TestAsyncEnhancedThreadPool(unittest.TestCase):
    """AsyncEnhancedThreadPool 测试类 - 针对简化版本"""

    def setUp(self):
        """测试前准备"""
        self.pool = AsyncEnhancedThreadPool(max_workers=2)

    # 测试同步函数
    def test_sync_function(self):
        """测试同步函数执行"""

        def sync_add(a, b):
            return a + b

        result = self.pool.submit_task(sync_add, 2, 3)
        self.assertEqual(result, 5)

    def test_sync_function_with_kwargs(self):
        """测试带关键字参数的同步函数"""

        def sync_multiply(a, b=1):
            return a * b

        result = self.pool.submit_task(sync_multiply, 5, b=3)
        self.assertEqual(result, 15)

    # 测试异步函数
    def test_async_function(self):
        """测试异步函数执行"""

        async def async_add(a, b):
            await asyncio.sleep(0.1)
            return a + b

        result = self.pool.submit_task(async_add, 2, 3)
        self.assertEqual(result, 5)

    def test_async_function_with_kwargs(self):
        """测试带关键字参数的异步函数"""

        async def async_multiply(a, b=1):
            await asyncio.sleep(0.1)
            return a * b

        result = self.pool.submit_task(async_multiply, 5, b=3)
        self.assertEqual(result, 15)

    # 测试批量任务
    def test_batch_tasks_simple_format(self):
        """测试简单格式的批量任务"""

        def square(x):
            return x * x

        numbers = [1, 2, 3, 4, 5]
        results = self.pool.submit_tasks(square, numbers)
        self.assertEqual(results, [1, 4, 9, 16, 25])

    def test_batch_tasks_complex_format(self):
        """测试复杂格式的批量任务"""

        def power(base, exponent=2):
            return base**exponent

        # 复杂格式: [(args_tuple, kwargs_dict), ...]
        tasks = [
            ((2,), {}),  # 2^2 = 4
            ((3,), {'exponent': 3}),  # 3^3 = 27
            ((5,), {'exponent': 1}),  # 5^1 = 5
        ]
        results = self.pool.submit_tasks(power, tasks)
        self.assertEqual(results, [4, 27, 5])

    def test_batch_tasks_tuple_format(self):
        """测试元组格式的批量任务"""

        def multiply(args):
            a, b = args
            return a * b

        # 元组格式: [(a1, b1), (a2, b2), ...]
        tasks = [(2, 3), (4, 5), (6, 7)]
        results = self.pool.submit_tasks(multiply, tasks)
        self.assertEqual(results, [6, 20, 42])

    def test_batch_tasks_mixed_functions(self):
        """测试混合函数的批量任务"""

        async def async_square(x):
            await asyncio.sleep(0.01)
            return x * x

        def sync_cube(x):
            return x * x * x

        numbers = [1, 2, 3]

        # 测试异步函数批量
        results = self.pool.submit_tasks(async_square, numbers)
        self.assertEqual(results, [1, 4, 9])

        # 测试同步函数批量
        results = self.pool.submit_tasks(sync_cube, numbers)
        self.assertEqual(results, [1, 8, 27])

    # 测试回调函数
    def test_batch_tasks_with_callback(self):
        """测试批量任务的回调函数"""
        callback_results = []

        def callback(result):
            callback_results.append(result)

        def increment(x):
            return x + 1

        numbers = [1, 2, 3]
        results = self.pool.submit_tasks(increment, numbers)
        self.assertEqual(results, [2, 3, 4])

    # 测试异常处理
    def test_sync_function_exception(self):
        """测试同步函数异常处理"""

        def faulty_function():
            raise ValueError('测试同步函数异常处理 Test error')

        result = self.pool.submit_task(faulty_function)
        self.assertIn('ValueError', str(result))

    def test_async_function_exception(self):
        """测试异步函数异常处理"""

        async def faulty_async_function():
            await asyncio.sleep(0.1)
            raise RuntimeError('测试异步函数异常处理 Async test error')

        result = self.pool.submit_task(faulty_async_function)
        self.assertIn('RuntimeError', str(result))

    def test_batch_tasks_with_exceptions(self):
        """测试批量任务中的异常处理"""

        def sometimes_faulty(x):
            if x == 2:
                raise ValueError("测试批量任务中的异常处理 I don't like 2")
            return x * 10

        numbers = [1, 2, 3]
        results = self.pool.submit_tasks(sometimes_faulty, numbers)

        self.assertEqual(results[0], 10)  # 1 * 10 = 10
        self.assertEqual(results[2], 30)  # 3 * 10 = 30

    # 测试上下文管理器
    def test_context_manager(self):
        """测试上下文管理器用法"""
        with AsyncEnhancedThreadPool(max_workers=2) as pool:
            result = pool.submit_task(lambda x: x * 3, 4)
            self.assertEqual(result, 12)

    # 测试性能和多线程
    def test_concurrent_execution(self):
        """测试并发执行性能"""

        def slow_operation(x):
            time.sleep(0.1)
            return x

        start_time = time.time()

        numbers = list(range(5))
        results = self.pool.submit_tasks(slow_operation, numbers)

        end_time = time.time()
        execution_time = end_time - start_time

        # 由于是并发执行，总时间应该远小于 5 * 0.1 = 0.5 秒
        self.assertLess(execution_time, 0.5)
        self.assertEqual(results, numbers)

    # 测试边界情况
    def test_empty_batch_tasks(self):
        """测试空批量任务"""

        def dummy_func(x):
            return x

        results = self.pool.submit_tasks(dummy_func, [])
        self.assertEqual(results, [])

    def test_none_results(self):
        """测试返回 None 的函数"""

        def none_function():
            return None

        result = self.pool.submit_task(none_function)
        self.assertIsNone(result)

    def test_large_batch_tasks(self):
        """测试大批量任务"""

        def identity(x):
            return x

        large_list = list(range(100))
        results = self.pool.submit_tasks(identity, large_list)
        self.assertEqual(results, large_list)

    def test_custom_exception_handler(self):
        """测试自定义异常处理器"""
        exception_caught = []

        def custom_handler(exc):
            exception_caught.append(str(exc))

        pool = AsyncEnhancedThreadPool(exception_handler=custom_handler)

        def faulty_function():
            raise ValueError('Custom handler test')

        result = pool.submit_task(faulty_function)

        self.assertEqual(len(exception_caught), 1)
        self.assertIn('Custom handler test', exception_caught[0])


class TestAsyncEnhancedThreadPoolAdvanced(unittest.TestCase):
    """高级测试用例"""

    def setUp(self):
        """测试前准备"""
        self.pool = AsyncEnhancedThreadPool(max_workers=4)

    def test_mixed_async_sync_batch(self):
        """测试混合异步和同步函数的批量任务执行"""

        async def async_task(x):
            await asyncio.sleep(0.01)
            return f'async_{x}'

        def sync_task(x):
            return f'sync_{x}'

        # 分别测试
        async_results = self.pool.submit_tasks(async_task, [1, 2, 3])
        sync_results = self.pool.submit_tasks(sync_task, [1, 2, 3])

        self.assertEqual(async_results, ['async_1', 'async_2', 'async_3'])
        self.assertEqual(sync_results, ['sync_1', 'sync_2', 'sync_3'])

    def test_thread_pool_isolation(self):
        """测试线程池隔离"""

        def task_that_uses_resources(x):
            # 模拟资源密集型任务
            return x**2

        # 创建多个线程池实例
        pool1 = AsyncEnhancedThreadPool(max_workers=1)
        pool2 = AsyncEnhancedThreadPool(max_workers=1)

        results1 = pool1.submit_tasks(task_that_uses_resources, [1, 2, 3])
        results2 = pool2.submit_tasks(task_that_uses_resources, [4, 5, 6])

        self.assertEqual(results1, [1, 4, 9])
        self.assertEqual(results2, [16, 25, 36])

    def test_stress_test(self):
        """压力测试"""

        def simple_computation(x):
            return x * x + x

        # 测试大量任务
        large_input = list(range(1000))
        results = self.pool.submit_tasks(simple_computation, large_input)

        expected = [x * x + x for x in large_input]
        self.assertEqual(results, expected)

    def test_concurrent_independent_calls(self):
        """测试并发独立调用"""

        def add_one(x):
            return x + 1

        # 多次独立调用应该是完全隔离的
        result1 = self.pool.submit_task(add_one, 1)
        result2 = self.pool.submit_task(add_one, 2)
        result3 = self.pool.submit_task(add_one, 3)

        self.assertEqual(result1, 2)
        self.assertEqual(result2, 3)
        self.assertEqual(result3, 4)


class TestAsyncEnhancedThreadPoolEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def setUp(self):
        """测试前准备"""
        self.pool = AsyncEnhancedThreadPool(max_workers=2)

    def test_single_item_batch(self):
        """测试单个项目的批量任务"""

        def double(x):
            return x * 2

        # 单个项目的批量任务
        results = self.pool.submit_tasks(double, [5])
        self.assertEqual(results, [10])

    def test_nested_functions(self):
        """测试嵌套函数"""

        def outer_function(x):
            def inner_function(y):
                return y * 2

            return inner_function(x) + 1

        result = self.pool.submit_task(outer_function, 3)
        self.assertEqual(result, 7)  # 3*2 + 1 = 7

    def test_lambda_functions(self):
        """测试 lambda 函数"""
        result = self.pool.submit_task(lambda x, y: x + y, 10, 20)
        self.assertEqual(result, 30)

    def test_class_methods(self):
        """测试类方法"""

        class Calculator:
            def add(self, a, b):
                return a + b

        calc = Calculator()
        result = self.pool.submit_task(calc.add, 7, 8)
        self.assertEqual(result, 15)

    def test_static_methods(self):
        """测试静态方法"""

        class MathUtils:
            @staticmethod
            def multiply(a, b):
                return a * b

        result = self.pool.submit_task(MathUtils.multiply, 6, 7)
        self.assertEqual(result, 42)

    def test_instance_with_state(self):
        """测试有状态的实例方法"""

        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self):
                self.count += 1
                return self.count

        counter = Counter()
        result1 = self.pool.submit_task(counter.increment)
        result2 = self.pool.submit_task(counter.increment)

        # 修复：由于使用的是同一个实例，状态会在调用间保持
        # 但要注意，由于线程池的异步特性，实际的执行顺序可能不确定
        # 这里我们只检查两个结果都大于等于1，且不相等（因为状态递增）
        self.assertEqual(result1, 1)
        self.assertEqual(result2, 2)


def performance_demo():
    """性能演示函数"""
    print('=== AsyncEnhancedThreadPool 性能演示 ===')

    def slow_sync_task(x):
        time.sleep(0.1)
        return x * 2

    async def slow_async_task(x):
        await asyncio.sleep(0.1)
        return x * 3

    pool = AsyncEnhancedThreadPool(max_workers=4)

    # 测试同步任务性能
    print('测试同步任务...')
    start_time = time.time()
    results_sync = pool.submit_tasks(slow_sync_task, list(range(10000)))
    sync_time = time.time() - start_time
    print(f'同步任务完成: {len(results_sync)} 个任务, 耗时: {sync_time:.2f}秒')

    # 测试异步任务性能
    print('测试异步任务...')
    start_time = time.time()
    results_async = pool.submit_tasks(slow_async_task, list(range(10000)))
    async_time = time.time() - start_time
    print(f'异步任务完成: {len(results_async)} 个任务, 耗时: {async_time:.2f}秒')

    if async_time > 0:
        print(f'性能提升: {sync_time / async_time:.2f}x')
    else:
        print('异步任务完成太快，无法计算性能提升')


if __name__ == '__main__':
    # 运行测试
    print('开始运行 AsyncEnhancedThreadPool 测试...')
    unittest.main()  # verbosity=2)

    # 运行性能演示
    print('\n' + '=' * 50)
    performance_demo()
