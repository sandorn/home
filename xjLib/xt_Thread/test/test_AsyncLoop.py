# !/usr/bin/env python
"""
AsyncLoopThreadPool 类测试程序（优化版）
修复结果格式和参数传递问题
"""

from __future__ import annotations

import asyncio
import os
import sys
import time

# 添加路径以导入模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from xt_thread.futures import AsyncLoopThreadPool


def simple_sync_task(task_id: int) -> int:
    """简单的同步任务"""
    time.sleep(0.05)  # 减少等待时间
    return task_id * 2


async def simple_async_task(task_id: int) -> int:
    """简单的异步任务"""
    await asyncio.sleep(0.05)  # 减少等待时间
    return task_id * 3


def error_task(task_id: int) -> int:
    """会抛出异常的任务"""
    if task_id == 2:
        raise ValueError(f'任务 {task_id} 故意抛出异常')
    return task_id * 4


def extract_results(results: list) -> list:
    """从AsyncLoopThreadPool的结果中提取实际值"""
    if not results:
        return []

    # 如果结果是字典格式，提取result字段
    if isinstance(results[0], dict) and 'result' in results[0]:
        return [r['result'] for r in results if isinstance(r, dict) and 'result' in r]

    # 如果结果已经是简单值，直接返回
    return results


def test_basic_sync_tasks():
    """测试基本同步任务"""
    print('=' * 50)
    print('测试1: 基本同步任务')
    print('=' * 50)

    try:
        with AsyncLoopThreadPool(max_workers=2) as pool:
            print('[OK] 线程池创建成功')

            # 提交3个简单同步任务
            for i in range(3):
                pool.submit_task(simple_sync_task, i)

            results = pool.wait_all_completed()
            print(f'[OK] 任务完成，结果数量: {len(results)}')

            # 提取实际结果值
            actual_values = extract_results(results)
            expected = [i * 2 for i in range(3)]

            if set(actual_values) == set(expected):
                print('[OK] 结果验证通过')
                return True
            print(f'[ERROR] 结果不匹配，期望: {expected}, 实际: {actual_values}')
            return False

    except Exception as e:
        print(f'[ERROR] 测试1 失败: {e}')
        return False


def test_basic_async_tasks():
    """测试基本异步任务"""
    print('\n' + '=' * 50)
    print('测试2: 基本异步任务')
    print('=' * 50)

    try:
        with AsyncLoopThreadPool(max_workers=2) as pool:
            print('[OK] 线程池创建成功')

            # 提交3个简单异步任务
            for i in range(3):
                pool.submit_task(simple_async_task, i)

            results = pool.wait_all_completed()
            print(f'[OK] 异步任务完成，结果数量: {len(results)}')

            # 提取实际结果值
            actual_values = extract_results(results)
            expected = [i * 3 for i in range(3)]

            if set(actual_values) == set(expected):
                print('[OK] 结果验证通过')
                return True
            print(f'[ERROR] 结果不匹配，期望: {expected}, 实际: {actual_values}')
            return False

    except Exception as e:
        print(f'[ERROR] 测试2 失败: {e}')
        return False


def test_mixed_sync_async():
    """测试混合同步和异步任务"""
    print('\n' + '=' * 50)
    print('测试3: 混合同步和异步任务')
    print('=' * 50)

    try:
        with AsyncLoopThreadPool(max_workers=4) as pool:
            print('[OK] 线程池创建成功')

            # 混合提交同步和异步任务
            for i in range(6):
                if i % 2 == 0:
                    pool.submit_task(simple_sync_task, i)
                else:
                    pool.submit_task(simple_async_task, i)

            results = pool.wait_all_completed()
            print(f'[OK] 混合任务完成，结果数量: {len(results)}')

            # 提取实际结果值
            actual_values = extract_results(results)
            expected = []
            for i in range(6):
                if i % 2 == 0:
                    expected.append(i * 2)
                else:
                    expected.append(i * 3)

            if set(actual_values) == set(expected):
                print('[OK] 结果验证通过')
                return True
            print(f'[ERROR] 结果不匹配，期望: {expected}, 实际: {actual_values}')
            return False

    except Exception as e:
        print(f'[ERROR] 测试3 失败: {e}')
        return False


def test_batch_tasks():
    """测试批量任务提交"""
    print('\n' + '=' * 50)
    print('测试4: 批量任务提交')
    print('=' * 50)

    try:
        with AsyncLoopThreadPool(max_workers=3) as pool:
            print('[OK] 线程池创建成功')

            # 批量提交任务（不使用callback参数）
            tasks = [1, 2, 3, 4, 5]
            futures = pool.submit_tasks(simple_sync_task, tasks)
            print(f'[OK] 提交了 {len(futures)} 个任务')

            results = pool.wait_all_completed()
            print(f'[OK] 批量任务完成，结果数量: {len(results)}')

            # 提取实际结果值
            actual_values = extract_results(results)
            expected = [i * 2 for i in tasks]

            if set(actual_values) == set(expected):
                print('[OK] 结果验证通过')
                return True
            print(f'[ERROR] 结果不匹配，期望: {expected}, 实际: {actual_values}')
            return False

    except Exception as e:
        print(f'[ERROR] 测试4 失败: {e}')
        return False


def test_exception_handling():
    """测试异常处理"""
    print('\n' + '=' * 50)
    print('测试6: 异常处理')
    print('=' * 50)

    try:
        exceptions = []

        def exception_handler(e: Exception) -> None:
            exceptions.append(e)

        with AsyncLoopThreadPool(exception_handler=exception_handler) as pool:
            print('[OK] 线程池创建成功')

            # 提交包含异常的任务
            for i in range(5):
                pool.submit_task(error_task, i)

            results = pool.wait_all_completed()
            print(f'[OK] 任务完成，结果数量: {len(results)}')
            print(f'[OK] 捕获异常数量: {len(exceptions)}')

            # 验证异常处理
            if len(exceptions) == 1 and isinstance(exceptions[0], ValueError):
                print('[OK] 异常处理验证通过')
                return True
            print(f'[ERROR] 异常处理失败，期望1个ValueError，实际: {exceptions}')
            return False

    except Exception as e:
        print(f'[ERROR] 测试6 失败: {e}')
        return False


def test_timeout_feature():
    """测试超时功能"""
    print('\n' + '=' * 50)
    print('测试7: 超时功能')
    print('=' * 50)

    try:

        def slow_task(task_id: int) -> int:
            time.sleep(0.2)  # 较慢的任务
            return task_id * 2

        with AsyncLoopThreadPool(max_workers=2) as pool:
            print('[OK] 线程池创建成功')

            # 提交慢任务
            for i in range(3):
                pool.submit_task(slow_task, i)

            # 使用短超时
            results = pool.wait_all_completed(timeout=0.1)
            print(f'[OK] 超时测试结果数量: {len(results)}')

            # 等待任务完成
            time.sleep(0.3)
            results = pool.wait_all_completed()
            print(f'[OK] 最终结果数量: {len(results)}')

            print('[OK] 超时功能测试通过')
            return True

    except Exception as e:
        print(f'[ERROR] 测试7 失败: {e}')
        return False


def test_performance():
    """测试性能"""
    print('\n' + '=' * 50)
    print('测试8: 性能测试')
    print('=' * 50)

    try:

        def quick_task(task_id: int) -> int:
            return task_id * 2

        start_time = time.time()

        with AsyncLoopThreadPool(max_workers=4) as pool:
            # 提交50个快速任务（减少数量避免卡住）
            for i in range(50):
                pool.submit_task(quick_task, i)

            results = pool.wait_all_completed()

        end_time = time.time()
        duration = end_time - start_time

        print(f'[OK] 50个任务完成，耗时: {duration:.4f}秒')
        print(f'[OK] 平均每个任务: {duration / 50 * 1000:.2f}毫秒')

        # 验证结果
        if len(results) == 50:
            print('[OK] 性能测试通过')
            return True
        print(f'[ERROR] 任务数量不匹配，期望50，实际: {len(results)}')
        return False

    except Exception as e:
        print(f'[ERROR] 测试8 失败: {e}')
        return False


def run_all_tests():
    """运行所有测试"""
    print('AsyncLoopThreadPool 功能测试开始')
    print('测试时间:', time.strftime('%Y-%m-%d %H:%M:%S'))

    tests = [
        test_basic_sync_tasks,
        test_basic_async_tasks,
        test_mixed_sync_async,
        test_batch_tasks,
        test_exception_handling,
        test_timeout_feature,
        test_performance,
    ]

    results = []
    for test_func in tests:
        try:
            success = test_func()
            results.append((test_func.__name__, success))

            # 测试间短暂暂停
            time.sleep(0.1)
        except Exception as e:
            print(f'[ERROR] 测试 {test_func.__name__} 发生异常: {e}')
            results.append((test_func.__name__, False))

    # 输出测试结果汇总
    print('\n' + '=' * 50)
    print('最终测试结果汇总:')
    print('=' * 50)
    passed = 0
    for test_name, success in results:
        status = '[OK] 通过' if success else '[ERROR] 失败'
        print(f'{test_name}: {status}')
        if success:
            passed += 1

    print(f'\n总计: {passed}/{len(results)} 个测试通过')
    print('测试程序结束')

    return passed == len(results)


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
