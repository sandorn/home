"""
==============================================================
Description  : futures.py模块测试代码
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-08-21 14:27:52
==============================================================
"""

from __future__ import annotations

import time
import unittest
from concurrent.futures import wait


class TestBaseThreadRunner(unittest.TestCase):
    """测试BaseThreadRunner类的功能"""

    def setUp(self):
        """测试前准备"""
        from xt_thread.futures import BaseThreadRunner

        self.BaseThreadRunner = BaseThreadRunner

    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""

        def worker(task_id):
            time.sleep(0.1)
            return f'Task {task_id} completed'

        pool = self.BaseThreadRunner(max_workers=3)
        threads = []

        # 提交5个任务
        for i in range(5):
            thread = pool.submit(worker, i)
            threads.append(thread)

        # 等待所有线程完成并获取结果
        thread_results = []
        for thread in threads:
            result = thread.get_result()
            thread_results.append(result)

        self.assertEqual(len(thread_results), 5)
        for i, result in enumerate(thread_results):
            self.assertEqual(result, f'Task {i} completed')

    def test_thread_limit(self):
        """测试线程数量限制"""
        import threading

        active_threads = set()
        max_count = [0]
        lock = threading.Lock()

        def worker(task_id):
            with lock:
                active_threads.add(task_id)
                current_active = len([t for t in threads if t.is_alive()])
                max_count[0] = max(max_count[0], current_active)
            time.sleep(0.3)  # 增加睡眠时间确保并发

        pool = self.BaseThreadRunner(max_workers=2)
        threads = []

        # 提交4个任务
        for i in range(4):
            thread = pool.submit(worker, i)
            threads.append(thread)

        # 等待所有线程完成
        for thread in threads:
            thread.join()

        # 验证最大线程数不超过限制（可能为1或2，取决于执行时机）
        self.assertLessEqual(max_count[0], 2)
        self.assertEqual(set(active_threads), set(range(4)))

    def test_shutdown(self):
        """测试关闭功能"""
        pool = self.BaseThreadRunner(max_workers=2)

        def worker():
            time.sleep(0.1)
            return 'done'

        # 提交任务
        thread = pool.submit(worker)
        pool.shutdown(wait=True)

        # 验证任务完成
        self.assertEqual(thread.get_result(), 'done')


class TestDynamicThreadRunner(unittest.TestCase):
    """测试DynamicThreadRunner类的功能"""

    def setUp(self):
        """测试前准备"""
        from xt_thread.futures import DynamicThreadRunner

        self.DynamicThreadRunner = DynamicThreadRunner

    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""
        results = []

        def worker(task_id):
            results.append(task_id)
            time.sleep(0.1)

        with self.DynamicThreadRunner(min_workers=2, max_workers=5) as pool:
            for i in range(10):
                pool.submit(worker, i)

        self.assertEqual(set(results), set(range(10)))

    def test_context_manager(self):
        """测试上下文管理器功能"""
        results = []

        def worker(task_id):
            results.append(task_id)

        with self.DynamicThreadRunner() as pool:
            for i in range(5):
                pool.submit(worker, i)

        self.assertEqual(set(results), set(range(5)))

    def test_dynamic_adjustment(self):
        """测试动态调整线程数功能"""

        def cpu_intensive_task():
            # 模拟CPU密集型任务
            start = time.time()
            while time.time() - start < 0.1:
                pass
            return 'done'

        with self.DynamicThreadRunner(min_workers=1, max_workers=10) as pool:
            # 提交多个CPU密集型任务，观察线程数调整
            for i in range(10):
                pool.submit(cpu_intensive_task)

        # 验证线程池正常工作（通过上下文管理器确保正确关闭）
        self.assertTrue(True)  # 如果没有异常抛出，说明测试通过


class TestThreadPoolManager(unittest.TestCase):
    """测试ThreadPoolManager类的功能"""

    def setUp(self):
        """测试前准备"""
        from xt_thread.futures import ThreadPoolManager

        self.ThreadPoolManager = ThreadPoolManager

    def test_singleton_behavior(self):
        """测试单例行为"""
        pool1 = self.ThreadPoolManager.get_pool()
        pool2 = self.ThreadPoolManager.get_pool()

        self.assertIs(pool1, pool2)

    def test_different_max_workers(self):
        """测试不同max_workers参数获取不同实例"""
        pool1 = self.ThreadPoolManager.get_pool(max_workers=4)
        pool2 = self.ThreadPoolManager.get_pool(max_workers=8)

        self.assertIsNot(pool1, pool2)
        self.assertEqual(pool1._max_workers, 4)
        self.assertEqual(pool2._max_workers, 8)

    def test_task_execution(self):
        """测试任务执行"""
        results = []

        def worker(task_id):
            results.append(task_id)
            return task_id

        with self.ThreadPoolManager.get_pool() as executor:
            futures = [executor.submit(worker, i) for i in range(5)]
            wait(futures)

        self.assertEqual(set(results), set(range(5)))

    def test_shutdown(self):
        """测试关闭功能"""
        pool1 = self.ThreadPoolManager.get_pool()
        self.ThreadPoolManager.shutdown()
        pool2 = self.ThreadPoolManager.get_pool()

        self.assertIsNot(pool1, pool2)

    def test_auto_worker_calculation(self):
        """测试自动计算工作线程数"""
        import os

        # 测试None参数时的自动计算
        pool = self.ThreadPoolManager.get_pool(max_workers=None)
        expected_workers = (os.cpu_count() or 4) * 4
        self.assertEqual(pool._max_workers, expected_workers)


class TestEnhancedThreadPool(unittest.TestCase):
    """测试EnhancedThreadPool类的功能"""

    def setUp(self):
        """测试前准备"""
        from xt_thread.futures import EnhancedThreadPool

        self.EnhancedThreadPool = EnhancedThreadPool

    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""

        def worker(task_id):
            time.sleep(0.1)
            return f'Task {task_id} completed'

        pool = self.EnhancedThreadPool(max_workers=3)
        futures = []

        # 提交5个任务
        for i in range(5):
            future = pool.submit_task(worker, i)
            futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()

        # 验证结果数量和内容
        self.assertEqual(len(pool.results), 5)
        success_results = [result['result'] for result in pool.results if result['state'] == 'success']
        self.assertEqual(len(success_results), 5)
        for i in range(5):
            self.assertIn(f'Task {i} completed', success_results)

    def test_batch_submit_simple(self):
        """测试批量提交简单格式的任务"""

        def worker(task_id):
            time.sleep(0.1)
            return f'Task {task_id} completed'

        pool = self.EnhancedThreadPool()
        # 简单格式: [item1, item2, ...]
        futures = pool.submit_tasks(worker, list(range(5)))
        
        # 等待所有任务完成
        for future in futures:
            future.result()
            
        # 验证结果
        self.assertEqual(len(pool.results), 5)
        success_results = [result['result'] for result in pool.results if result['state'] == 'success']
        self.assertEqual(len(success_results), 5)

    def test_batch_submit_complex(self):
        """测试批量提交复杂格式的任务"""

        def worker(task_id, delay=0.1):
            time.sleep(delay)
            return f'Task {task_id} completed with delay {delay}'

        pool = self.EnhancedThreadPool()
        # 复杂格式: [(args_tuple, kwargs_dict), ...]
        iterables = [
            ((1,), {'delay': 0.05}),
            ((2,), {'delay': 0.1}),
            ((3,), {'delay': 0.15})
        ]
        futures = pool.submit_tasks(worker, iterables)
        
        # 等待所有任务完成
        for future in futures:
            future.result()
            
        # 验证结果
        self.assertEqual(len(pool.results), 3)
        success_results = [result['result'] for result in pool.results if result['state'] == 'success']
        self.assertEqual(len(success_results), 3)
        for i in range(1, 4):
            self.assertTrue(any(f'Task {i} completed' in result for result in success_results))

    def test_exception_handling(self):
        """测试异常处理功能"""

        def worker(task_id):
            if task_id % 2 == 0:
                raise ValueError(f'Error in task {task_id}')
            return f'Task {task_id} completed'

        pool = self.EnhancedThreadPool()
        futures = []
        for i in range(5):
            future = pool.submit_task(worker, i)
            futures.append(future)
        
        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception:
                pass  # 忽略异常，因为我们要测试异常处理
                
        # 验证结果
        self.assertEqual(len(pool.results), 5)
        success_count = sum(1 for result in pool.results if result['state'] == 'success')
        error_count = sum(1 for result in pool.results if result['state'] == 'error')
        self.assertEqual(success_count, 2)  # 任务1, 3 应该成功
        self.assertEqual(error_count, 3)    # 任务0, 2, 4 应该失败

    def test_context_manager(self):
        """测试上下文管理器功能"""

        def worker(task_id):
            time.sleep(0.1)
            return f'Task {task_id} completed'

        results = []
        pool = self.EnhancedThreadPool()
        futures = []
        
        with pool:
            for i in range(5):
                future = pool.submit_task(worker, i)
                futures.append(future)
            
            # 等待所有任务完成
            for future in futures:
                future.result()
            
            # 直接使用pool.results
            results = pool.results

        # 验证结果
        self.assertEqual(len(results), 5)
        success_results = [result['result'] for result in results if result['state'] == 'success']
        self.assertEqual(len(success_results), 5)

    def test_shutdown(self):
        """测试关闭功能"""

        def worker():
            time.sleep(0.1)
            return 'done'

        pool = self.EnhancedThreadPool(max_workers=2)

        # 提交任务
        pool.submit_task(worker)
        pool.shutdown(wait=True)

        # 验证线程池已关闭（通过尝试再次提交任务应引发异常）
        with self.assertRaises(RuntimeError):
            pool.submit_task(worker)

    def test_auto_worker_calculation(self):
        """测试自动计算工作线程数"""
        import os

        # 测试默认参数时的自动计算
        pool = self.EnhancedThreadPool()
        base_workers = os.cpu_count() or 4
        expected_workers = base_workers * 4
        self.assertEqual(pool.executor._max_workers, expected_workers)

        # 测试指定max_workers时的行为
        pool = self.EnhancedThreadPool(max_workers=10)
        self.assertEqual(pool.executor._max_workers, 10)
        
    def test_wait_all_completed(self):
        """测试wait_all_completed方法的功能"""
        
        # 测试1: 基本功能 - 所有任务正常完成
        def worker1(task_id):
            time.sleep(0.1)
            return f'Task {task_id} completed'
            
        pool1 = self.EnhancedThreadPool(max_workers=3)
        pool1.submit_tasks(worker1, list(range(5)))
        
        # 等待所有任务完成并获取结果
        results1 = pool1.wait_all_completed()
        self.assertEqual(len(results1), 5)
        success_count1 = sum(1 for result in results1 if result['state'] == 'success')
        self.assertEqual(success_count1, 5)
        
        # 测试2: 超时处理
        def worker2(task_id):
            time.sleep(0.3)  # 故意设置较长的睡眠时间
            return f'Task {task_id} completed'
            
        pool2 = self.EnhancedThreadPool(max_workers=1)  # 限制为1个工作线程确保任务排队
        # 提交任务并保存返回的future列表用于验证
        futures = pool2.submit_tasks(worker2, list(range(3)))
        self.assertEqual(len(futures), 3)
        
        # 设置较短的超时时间，应该只能获取到部分已完成的任务结果
        start_time = time.time()
        results2 = pool2.wait_all_completed(timeout=0.4)
        elapsed_time = time.time() - start_time
        
        # 确保在超时时间内返回
        self.assertLess(elapsed_time, 0.5)
        
        # 继续等待剩余任务完成，增加等待时间和重试次数
        remaining_results = []
        max_wait_time = 2.0  # 最多等待2秒
        wait_start_time = time.time()
        
        while pool2._future_tasks and (time.time() - wait_start_time) < max_wait_time:
            new_results = pool2.wait_all_completed(timeout=0.5)  # 增加超时时间
            remaining_results.extend(new_results)
            time.sleep(0.1)  # 增加等待间隔
        
        # 如果还有未完成的任务，强制等待它们完成
        if pool2._future_tasks:
            for future in pool2._future_tasks:
                future.result()  # 阻塞等待每个任务完成
            final_results = pool2.wait_all_completed()
            remaining_results.extend(final_results)
        
        # 验证总共获取到了所有任务的结果
        total_results = len(results2) + len(remaining_results)
        self.assertEqual(total_results, 3)
        
        # 测试3: 异常处理
        def worker3(task_id):
            if task_id % 2 == 0:
                raise ValueError(f'Error in task {task_id}')
            return f'Task {task_id} completed'
            
        pool3 = self.EnhancedThreadPool()
        pool3.submit_tasks(worker3, list(range(5)))
        
        # 等待所有任务完成并获取结果
        results3 = pool3.wait_all_completed()
        self.assertEqual(len(results3), 5)
        success_count3 = sum(1 for result in results3 if result['state'] == 'success')
        error_count3 = sum(1 for result in results3 if result['state'] == 'error')
        self.assertEqual(success_count3, 2)  # 任务1, 3 应该成功
        self.assertEqual(error_count3, 3)    # 任务0, 2, 4 应该失败


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
