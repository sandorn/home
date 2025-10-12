# !/usr/bin/env python
"""
测试thread.py模块的功能
"""

from __future__ import annotations

import random
import time

from xt_thread.thread import ComposedSingletonThread, SafeThread, SingletonThread, ThreadBase, ThreadManager


# 改进callback匿名函数，确保正确返回结果
def callback_func(result):
    print(result := f'callback |{result}')
    return result


# 测试辅助函数
def simple_task():
    """简单任务函数"""
    print('任务开始执行')
    time.sleep(1)  # 模拟耗时操作
    print('任务执行完成')
    return '任务成功'


def risky_task():
    """可能失败的任务"""
    print('风险任务开始执行')
    time.sleep(0.5)
    # 模拟随机失败
    if random.random() < 0.5:
        print('风险任务失败')
        raise ValueError('随机失败')
    print('风险任务执行完成')
    return '风险任务成功'


# 1. 测试ThreadBase类
def test_01_thread_base():
    """1. 测试ThreadBase类"""
    print('\n=== 1. 测试ThreadBase类 ===')

    thread = ThreadBase(simple_task)
    thread.start()
    result = thread.get_result()
    print(f'ThreadBase结果: {result}')
    print(f'线程是否在运行: {thread.is_running()}')


# 2. 测试SafeThread类
def test_02_safe_thread():
    """2. 测试SafeThread类"""
    print('\n=== 2. 测试SafeThread类 ===')
    thread = SafeThread(risky_task, max_retries=3, callback=callback_func)
    thread.start()
    result = thread.get_result()
    print(f'SafeThread结果: {result}')
    print(f'重试次数: {thread.retry_count}')


# 3. 测试ThreadManager类
def test_03_thread_manager():
    """3. 测试ThreadManager类"""
    print('\n=== 3. 测试ThreadManager类 ===')
    # 创建线程
    ThreadManager.create_thread(simple_task)
    ThreadManager.create_safe_thread(risky_task, max_retries=2)

    # 检查活动线程数量
    print(f'活动线程数量: {ThreadManager.get_active_count()}')

    # 获取线程结果
    results = ThreadManager.wait_all_completed()
    print(f'所有线程结果: {results}')
    print(f'等待后活动线程数量: {ThreadManager.get_active_count()}')


# 4. 测试SingletonThread类
def test_04_singleton_thread():
    """4. 测试SingletonThread类"""
    print('\n=== 4. 测试SingletonThread类 ===')
    # 创建两个相同目标函数的线程实例
    thread1 = SingletonThread(simple_task)
    thread2 = SingletonThread(simple_task)

    print(f'两个线程实例是否相同: {thread1 is thread2}')

    # 启动线程
    thread1.start()
    result = thread1.get_result()
    print(f'SingletonThread结果: {result}')


# 5. 测试ComposedSingletonThread类
def test_05_composed_singleton_thread():
    """5. 测试ComposedSingletonThread类"""
    print('\n=== 5. 测试ComposedSingletonThread类 ===')
    # 创建两个相同目标函数的线程实例
    thread1 = ComposedSingletonThread(simple_task)
    thread2 = ComposedSingletonThread(simple_task)

    print(f'两个线程实例是否相同: {thread1 is thread2}')

    # 启动线程
    thread1.start()
    result = thread1.get_result()
    print(f'ComposedSingletonThread结果: {result}')


# 8. 测试线程的上下文管理器功能
def test_08_context_manager():
    """8. 测试线程的上下文管理器功能"""
    print('\n=== 8. 测试线程的上下文管理器功能 ===')
    with ThreadBase(simple_task):
        print('在线程上下文中')
        time.sleep(0.5)
    print('上下文管理器结束')


# 运行所有测试
def run_all_tests():
    """运行所有测试"""
    print('开始测试thread.py模块...')
    test_01_thread_base()
    test_02_safe_thread()
    test_03_thread_manager()
    test_04_singleton_thread()
    test_05_composed_singleton_thread()
    test_08_context_manager()
    print('\n所有测试完成!')


if __name__ == '__main__':
    run_all_tests()
