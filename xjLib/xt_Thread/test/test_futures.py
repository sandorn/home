"""
==============================================================
Description  : futures.py模块测试代码
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-08-21 14:27:52
==============================================================
"""

import time
import unittest
from concurrent.futures import wait

from xt_thread.futures import (
    AsyncFunction,
    BaseThreadPool,
    DynamicThreadPool,
    EnhancedThreadPool,
    FnInPool,
    PoolExecutor,
    TaskExecutor,
    ThreadPool,
    ThreadPoolManager,
)


class TestBaseThreadPool(unittest.TestCase):
    """测试BaseThreadPool类的功能"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""
        results = []
        
        def worker(task_id):
            results.append(task_id)
            time.sleep(0.1)  # 模拟工作负载
        
        pool = BaseThreadPool(max_workers=3)
        threads = []
        
        # 提交5个任务
        for i in range(5):
            thread = pool.submit(worker, i)
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证所有任务都已执行
        self.assertEqual(set(results), set(range(5)))
    
    def test_thread_limit(self):
        """测试线程数量限制"""
        active_threads = []
        max_count = [0]
        
        def worker(task_id):
            active_threads.append(task_id)
            # 在任务执行过程中检查活跃线程数
            current_active = pool.active_threads
            max_count[0] = max(max_count[0], current_active)
            time.sleep(0.2)  # 模拟较长的工作负载
        
        pool = BaseThreadPool(max_workers=2)
        threads = []
        
        # 提交4个任务
        for i in range(4):
            thread = pool.submit(worker, i)
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证最大线程数不超过限制
        self.assertEqual(max_count[0], 2)
        self.assertEqual(set(active_threads), set(range(4)))


class TestThreadPool(TestBaseThreadPool):
    """测试ThreadPool类的功能（兼容层）"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""
        results = []
        
        def worker(task_id):
            results.append(task_id)
            time.sleep(0.1)  # 模拟工作负载
        
        pool = ThreadPool(max_workers=3)
        threads = []
        
        # 提交5个任务
        for i in range(5):
            thread = pool.submit(worker, i)
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证所有任务都已执行
        self.assertEqual(set(results), set(range(5)))
    
    def test_thread_limit(self):
        """测试线程数量限制"""
        active_threads = []
        max_count = [0]
        
        def worker(task_id):
            active_threads.append(task_id)
            # 在任务执行过程中检查活跃线程数
            current_active = pool.active_threads
            max_count[0] = max(max_count[0], current_active)
            time.sleep(0.2)  # 模拟较长的工作负载
        
        pool = ThreadPool(max_workers=2)
        threads = []
        
        # 提交4个任务
        for i in range(4):
            thread = pool.submit(worker, i)
            threads.append(thread)
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 验证最大线程数不超过限制
        self.assertEqual(max_count[0], 2)
        self.assertEqual(set(active_threads), set(range(4)))


class TestDynamicThreadPool(unittest.TestCase):
    """测试DynamicThreadPool类的功能"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和执行"""
        results = []
        
        def worker(task_id):
            results.append(task_id)
            time.sleep(0.1)  # 模拟工作负载
        
        with DynamicThreadPool(min_workers=2, max_workers=5) as pool:
            # 提交10个任务
            for i in range(10):
                pool.submit(worker, i)
        
        # 验证所有任务都已执行
        self.assertEqual(set(results), set(range(10)))
    
    def test_context_manager(self):
        """测试上下文管理器功能"""
        results = []
        
        def worker(task_id):
            results.append(task_id)
        
        # 使用上下文管理器
        with DynamicThreadPool() as pool:
            for i in range(5):
                pool.submit(worker, i)
        
        # 验证线程池已关闭且任务已执行
        self.assertEqual(set(results), set(range(5)))


class TestThreadPoolManager(unittest.TestCase):
    """测试ThreadPoolManager类的功能"""
    
    def test_singleton_behavior(self):
        """测试单例行为"""
        pool1 = ThreadPoolManager.get_pool()
        pool2 = ThreadPoolManager.get_pool()
        
        # 验证两次获取的是同一个实例
        self.assertIs(pool1, pool2)
    
    def test_different_max_workers(self):
        """测试不同max_workers参数获取不同实例"""
        pool1 = ThreadPoolManager.get_pool(max_workers=4)
        pool2 = ThreadPoolManager.get_pool(max_workers=8)
        
        # 验证max_workers不同时返回不同实例
        self.assertIsNot(pool1, pool2)
        self.assertEqual(pool1._max_workers, 4)
        self.assertEqual(pool2._max_workers, 8)
    
    def test_task_execution(self):
        """测试任务执行"""
        results = []
        
        def worker(task_id):
            results.append(task_id)
            return task_id
        
        with ThreadPoolManager.get_pool() as executor:
            futures = [executor.submit(worker, i) for i in range(5)]
            wait(futures)  # 等待所有任务完成
        
        # 验证所有任务都已执行
        self.assertEqual(set(results), set(range(5)))
    
    def test_shutdown(self):
        """测试关闭功能"""
        pool1 = ThreadPoolManager.get_pool()
        ThreadPoolManager.shutdown()
        pool2 = ThreadPoolManager.get_pool()
        
        # 验证shutdown后获取的是新实例
        self.assertIsNot(pool1, pool2)


class TestEnhancedThreadPool(unittest.TestCase):
    """测试EnhancedThreadPool类的功能"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和结果收集"""
        def worker(task_id):
            time.sleep(0.1)  # 模拟工作负载
            return task_id * 2
        
        with EnhancedThreadPool(max_workers=3) as pool:
            # 提交5个任务
            for i in range(5):
                pool.submit_task(worker, i)
            
            # 等待所有任务完成
            completed = pool.wait_for_completion(timeout=5)
            
            # 获取结果
            results = pool.get_results()
        
        # 验证所有任务都已完成
        self.assertTrue(completed)
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 2 for i in range(5)))
    
    def test_exception_handling(self):
        """测试异常处理功能"""
        exceptions = []
        
        def exception_handler(e):
            exceptions.append(e)
        
        def worker(task_id):
            if task_id == 2:
                raise ValueError("测试异常")
            return task_id * 2
        
        with EnhancedThreadPool() as pool:
            pool.set_exception_handler(exception_handler)
            
            # 提交5个任务
            for i in range(5):
                pool.submit_task(worker, i)
            
            # 等待所有任务完成
            pool.wait_for_completion()
            
            # 获取结果
            results = pool.get_results()
        
        # 验证异常被处理
        self.assertEqual(len(exceptions), 1)
        self.assertIsInstance(exceptions[0], ValueError)
        # 验证成功任务的结果
        expected_results = [i * 2 for i in range(5) if i != 2]
        self.assertEqual(set(results), set(expected_results))


class TestTaskExecutor(unittest.TestCase):
    """测试TaskExecutor类的功能"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和结果收集"""
        def worker(task_id):
            time.sleep(0.1)  # 模拟工作负载
            return task_id * 3
        
        with TaskExecutor(io_bound=True) as executor:
            # 添加多个任务
            executor.add_tasks(worker, [0, 1, 2, 3, 4])
            
            # 等待所有任务完成并获取结果
            results = executor.wait_completed()
        
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 3 for i in range(5)))
    
    def test_with_max_workers(self):
        """测试手动指定max_workers参数"""
        def worker(task_id):
            return task_id * 2
        
        with TaskExecutor(max_workers=4) as executor:
            executor.add_tasks(worker, [0, 1, 2, 3, 4])
            results = executor.wait_completed()
        
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 2 for i in range(5)))
    
    def test_with_callback(self):
        """测试带回调函数的任务提交"""
        results = []
        callback_results = []
        
        def worker(task_id):
            return task_id * 2
        
        def callback(future):
            callback_results.append(future.result())
        
        with TaskExecutor() as executor:
            executor.add_tasks(worker, [0, 1, 2, 3, 4], callback=callback)
            results = executor.wait_completed()
        
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 2 for i in range(5)))
        # 验证回调函数被调用
        self.assertEqual(set(callback_results), set(i * 2 for i in range(5)))


class TestPoolExecutor(TestTaskExecutor):
    """测试PoolExecutor类的功能（兼容层）"""
    
    def test_basic_functionality(self):
        """测试基本的任务提交和结果收集"""
        def worker(task_id):
            time.sleep(0.1)  # 模拟工作负载
            return task_id * 3
        
        with PoolExecutor(io_bound=True) as executor:
            # 添加多个任务
            executor.add_tasks(worker, [0, 1, 2, 3, 4])
            
            # 等待所有任务完成并获取结果
            results = executor.wait_completed()
        
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 3 for i in range(5)))
    
    def test_with_callback(self):
        """测试带回调函数的任务提交"""
        results = []
        callback_results = []
        
        def worker(task_id):
            return task_id * 2
        
        def callback(future):
            callback_results.append(future.result())
        
        with PoolExecutor() as executor:
            executor.add_tasks(worker, [0, 1, 2, 3, 4], callback=callback)
            results = executor.wait_completed()
        
        # 验证结果正确性
        self.assertEqual(set(results), set(i * 2 for i in range(5)))
        # 验证回调函数被调用
        self.assertEqual(set(callback_results), set(i * 2 for i in range(5)))


class TestAsyncFunction(unittest.TestCase):
    """测试AsyncFunction类的功能"""
    
    def test_single_arg_list(self):
        """测试单参数列表的情况"""
        def worker(task_id):
            time.sleep(0.1)  # 模拟工作负载
            return task_id * 2
        
        # 使用单参数列表
        result_obj = AsyncFunction(worker, [0, 1, 2, 3, 4])
        
        # 验证结果正确性
        self.assertEqual(sorted(result_obj.result), sorted([i * 2 for i in range(5)]))
    
    def test_multi_arg_lists(self):
        """测试多参数列表的情况"""
        def worker(a, b):
            time.sleep(0.1)  # 模拟工作负载
            return a + b
        
        # 使用多参数列表
        result_obj = AsyncFunction(worker, [1, 2, 3], [4, 5, 6])
        
        # 验证结果正确性
        expected_results = [1+4, 2+5, 3+6]
        self.assertEqual(sorted(result_obj.result), sorted(expected_results))
    
    def test_with_kwargs(self):
        """测试带关键字参数的情况"""
        def worker(a, multiplier=2):
            return a * multiplier
        
        # 使用关键字参数
        result_obj = AsyncFunction(worker, [1, 2, 3], multiplier=3)
        
        # 验证结果正确性
        self.assertEqual(sorted(result_obj.result), sorted([3, 6, 9]))
    
    def test_with_max_workers(self):
        """测试手动指定max_workers参数"""
        def worker(task_id):
            return task_id * 2
        
        # 指定线程数
        result_obj = AsyncFunction(worker, [0, 1, 2, 3, 4], max_workers=4)
        
        # 验证结果正确性
        self.assertEqual(sorted(result_obj.result), sorted([i * 2 for i in range(5)]))


class TestFnInPool(TestAsyncFunction):
    """测试FnInPool类的功能（兼容层）"""
    
    def test_single_arg_list(self):
        """测试单参数列表的情况"""
        def worker(task_id):
            time.sleep(0.1)  # 模拟工作负载
            return task_id * 2
        
        # 使用单参数列表
        result_obj = FnInPool(worker, [0, 1, 2, 3, 4])
        
        # 验证结果正确性
        self.assertEqual(sorted(result_obj.result), sorted([i * 2 for i in range(5)]))
    
    def test_multi_arg_lists(self):
        """测试多参数列表的情况"""
        def worker(a, b):
            time.sleep(0.1)  # 模拟工作负载
            return a + b
        
        # 使用多参数列表
        result_obj = FnInPool(worker, [1, 2, 3], [4, 5, 6])
        
        # 验证结果正确性
        expected_results = [1+4, 2+5, 3+6]
        self.assertEqual(sorted(result_obj.result), sorted(expected_results))
    
    def test_with_kwargs(self):
        """测试带关键字参数的情况"""
        def worker(a, multiplier=2):
            return a * multiplier
        
        # 使用关键字参数
        result_obj = FnInPool(worker, [1, 2, 3], multiplier=3)
        
        # 验证结果正确性
        self.assertEqual(sorted(result_obj.result), sorted([3, 6, 9]))


if __name__ == "__main__":
    unittest.main()