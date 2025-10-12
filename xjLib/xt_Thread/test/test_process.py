# !/usr/bin/env python3
"""
测试 process.py 文件中的功能
包含进程基础功能、进程管理器和自定义进程运行器的测试
"""

from __future__ import annotations

import asyncio
import time

from xt_thread.process import ProcessBase, ProcessManager, SafeProcess, process_manager, run_custom_process


def basic_task(x: int) -> int:
    """基本任务函数"""
    print(f"处理任务: {x}")
    time.sleep(0.5)  # 模拟耗时操作
    return x * x


def duration_task(duration: float) -> int:
    """一个简单的任务函数，睡眠指定秒数后返回结果"""
    print(f"任务开始,将睡眠{duration}秒")
    time.sleep(duration)
    print(f"任务完成,睡眠了{duration}秒")
    return int(duration * 10)


def square(x: int) -> int:
    """计算平方并模拟工作负载"""
    time.sleep(0.1)  # 模拟耗时操作
    return x * x


def add(x: int, y: int) -> int:
    """计算两数之和并模拟工作负载"""
    time.sleep(0.1)  # 模拟耗时操作
    return x + y


def divide(x: int, y: int) -> float:
    """执行除法操作，测试异常处理"""
    time.sleep(0.1)  # 模拟耗时操作
    return x / y


def process_number(x: int) -> int:
    """模拟复杂的数值处理"""
    time.sleep(0.05)  # 模拟中等耗时操作
    return sum(i for i in range(x))


def power(x: int, exponent: int = 2) -> int:
    """计算x的exponent次方"""
    time.sleep(0.1)  # 模拟耗时操作
    return x**exponent


def process_task(task_id: int) -> str:
    """模拟原始测试程序中的任务处理函数"""
    time.sleep(0.2)  # 模拟工作负载
    return f'Task {task_id} completed'


async def async_square(x: int) -> int:
    """异步计算平方函数"""
    await asyncio.sleep(0.1)  # 模拟异步I/O操作
    return x * x


async def async_add(x: int, y: int) -> int:
    """异步计算两数之和"""
    await asyncio.sleep(0.1)  # 模拟异步I/O操作
    return x + y


# 注意：multiprocessing模块本身不支持直接调用异步函数
# 下面创建包装函数，将异步函数转换为同步调用
def sync_wrapper(func, *args, **kwargs):
    """将异步函数包装为同步函数"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(func(*args, **kwargs))
    finally:
        loop.close()


def async_square_sync(x: int) -> int:
    """异步平方函数的同步包装器"""
    return sync_wrapper(async_square, x)


def async_add_sync(x: int, y: int) -> int:
    """异步加法函数的同步包装器"""
    return sync_wrapper(async_add, x, y)


# 全局变量用于跟踪失败次数
fail_count = [0]


def flaky_task(x: int) -> int:
    """可能失败的任务函数"""
    global fail_count
    fail_count[0] += 1
    if fail_count[0] <= 2:  # 前两次调用失败
        print(f"任务失败 (第 {fail_count[0]} 次尝试)")
        raise ValueError(f"模拟失败 #{fail_count[0]}")
    print(f"任务成功 (第 {fail_count[0]} 次尝试)")
    return x * x


def manager_task(x: int) -> int:
    """管理器任务函数"""
    print(f"管理器任务: {x}")
    time.sleep(0.3)
    return x * 10


def square_task(x: int) -> int:
    """计算平方的任务函数"""
    print(f"计算 {x} 的平方")
    time.sleep(0.2)  # 模拟耗时操作
    return x * x


def add_task(x: int, y: int) -> int:
    """加法任务函数"""
    return x + y


def cube_task(x: int) -> int:
    """计算立方的任务函数"""
    return x * x * x


def test_basic_function():
    """测试基本的进程功能"""
    print("\n===== 测试基本进程功能 =====")

    # 测试 ProcessBase
    try:
        with ProcessBase(basic_task, 5) as p:
            result = p.get_result()
            print(f"ProcessBase 结果: {result}")
    except Exception as e:
        print(f"ProcessBase 测试失败: {e}")

    # 测试 SafeProcess
    try:
        with SafeProcess(basic_task, 6) as p:
            result = p.get_result()
            print(f"SafeProcess 结果: {result}")
    except Exception as e:
        print(f"SafeProcess 测试失败: {e}")


def test_error_retry():
    """测试错误重试功能"""
    print("\n===== 测试错误重试功能 =====")

    try:
        # 创建一个允许重试的安全进程
        p = SafeProcess(flaky_task, 7, max_retries=3, retry_delay=0.3)
        p.start()
        result = p.get_result()
        print(f"重试后结果: {result}")
    except Exception as e:
        print(f"错误重试测试失败: {e}")


def test_process_manager():
    """测试进程管理器功能"""
    print("\n===== 测试进程管理器 =====")

    try:
        # 清除之前可能存在的进程
        process_manager.stop_all()

        # 创建多个进程
        processes = []
        for i in range(5):
            p = process_manager.create_safe_process(manager_task, i)
            processes.append(p)

        # 等待所有进程完成并获取结果
        results = process_manager.wait_all_completed()
        print(f"管理器收集的结果: {results}")

        # 验证所有进程都已停止
        process_manager.stop_all()
        print("所有进程已停止")
    except Exception as e:
        print(f"进程管理器测试失败: {e}")


def test_process_manager_methods():
    """测试ProcessManager的新方法：get_active_count、get_process_by_id、get_process_by_name和stop_process"""
    # 清空所有可能存在的进程
    ProcessManager.stop_all()
    
    print("\n===== 测试ProcessManager新方法 =====")
    
    # 创建几个进程
    process1 = ProcessManager.create_process(duration_task, 1.0, name="test_process_1")
    process2 = ProcessManager.create_process(duration_task, 2.0, name="test_process_2")
    process3 = ProcessManager.create_process(duration_task, 1.5, name="test_process_1")  # 与process1同名
    
    # 获取进程ID
    pid1 = id(process1)
    pid2 = id(process2)
    pid3 = id(process3)
    
    print(f"\n创建的进程ID: {pid1}, {pid2}, {pid3}")
    print(f"活动进程数量: {ProcessManager.get_active_count()}")
    
    # 测试get_process_by_id方法
    retrieved_process = ProcessManager.get_process_by_id(pid1)
    print(f"通过ID {pid1} 获取进程: {'成功' if retrieved_process is process1 else '失败'}")
    
    # 测试get_process_by_name方法
    processes_with_name = ProcessManager.get_process_by_name("test_process_1")
    print(f"通过名称'test_process_1' 获取到的进程数量: {len(processes_with_name)}")
    
    # 测试stop_process方法
    stop_result = ProcessManager.stop_process(pid2, timeout=0.5)
    print(f"停止进程 {pid2}: {'成功' if stop_result else '失败'}")
    
    # 等待一会儿，让进程完成或停止
    time.sleep(0.5)
    print(f"当前活动进程数量: {ProcessManager.get_active_count()}")
    
    # 等待所有进程完成
    time.sleep(2)
    print(f"最终活动进程数量: {ProcessManager.get_active_count()}")
    
    # 清理所有进程
    ProcessManager.stop_all()
    print("所有进程已清理")


def test_run_custom_process():
    """测试 run_custom_process 函数"""
    print("\n===== 测试 run_custom_process 函数 =====")

    try:
        # 并行计算多个数的平方
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        results = run_custom_process(square_task, numbers, max_workers=4)

        print(f"输入: {numbers}")
        print(f"结果: {results}")

        # 测试多参数函数
        numbers1 = [1, 2, 3]
        numbers2 = [4, 5, 6]
        add_results = run_custom_process(add_task, numbers1, numbers2)
        print(f"多参数输入: {numbers1}, {numbers2}")
        print(f"多参数结果: {add_results}")
    except Exception as e:
        print(f"run_custom_process 测试失败: {e}")


def test_run_custom_process_detailed():
    """详细测试 run_custom_process 函数的各种功能"""
    # 测试1: 简单函数的并行执行
    print('\n测试1: 简单函数的并行执行')

    # 并行计算多个数的平方
    numbers = list(range(10))
    start_time = time.time()
    results = run_custom_process(square, numbers, max_workers=5)
    end_time = time.time()

    print(f'输入: {numbers}')
    print(f'结果: {results}')
    print(f'执行时间: {end_time - start_time:.4f}秒')
    print(f'预期结果: {[x * x for x in numbers]}')
    print(f'结果正确: {results == [x * x for x in numbers]}\n')

    # 测试2: 多参数函数的并行执行
    print('测试2: 多参数函数的并行执行')

    # 并行计算多组数的和
    list1 = [1, 2, 3, 4, 5]
    list2 = [10, 20, 30, 40, 50]
    start_time = time.time()
    results = run_custom_process(add, list1, list2, max_workers=3)
    end_time = time.time()

    print(f'输入1: {list1}')
    print(f'输入2: {list2}')
    print(f'结果: {results}')
    print(f'执行时间: {end_time - start_time:.4f}秒')
    print(f'预期结果: {[x + y for x, y in zip(list1, list2, strict=False)]}')
    print(f'结果正确: {results == [x + y for x, y in zip(list1, list2, strict=False)]}\n')

    # 测试3: 异常处理功能
    print('测试3: 异常处理功能')

    # 包含会引发异常的输入
    numerators = [10, 20, 30, 40]
    denominators = [2, 0, 5, 8]  # 第二个元素会导致ZeroDivisionError
    start_time = time.time()
    results = run_custom_process(divide, numerators, denominators, max_workers=4, name='测试3: 异常处理功能')
    end_time = time.time()

    print(f'分子: {numerators}')
    print(f'分母: {denominators}')
    print(f'结果: {results}')
    print(f'执行时间: {end_time - start_time:.4f}秒')
    print(f'异常处理正常: {'测试3: 异常处理功能' in str(results[1])}\n')

    # 测试4: 大规模任务处理性能
    print('测试4: 大规模任务处理性能')

    # 生成大规模任务
    large_list = list(range(100))
    start_time = time.time()
    results = run_custom_process(process_number, large_list, max_workers=8)
    end_time = time.time()

    print(f'任务数量: {len(large_list)}')
    print(f'总执行时间: {end_time - start_time:.4f}秒')
    print(f'平均每个任务执行时间: {(end_time - start_time) * 1000 / len(large_list):.2f}毫秒')
    print(f'结果示例: {results[:5]}...{results[-5:]}\n')

    # 测试5: 关键字参数支持
    print('测试5: 关键字参数支持')

    # 使用默认关键字参数
    numbers = [1, 2, 3, 4, 5]
    start_time = time.time()
    results_default = run_custom_process(power, numbers, max_workers=3)
    end_time = time.time()

    print(f'输入: {numbers}')
    print(f'默认指数结果: {results_default}')
    print(f'默认指数执行时间: {end_time - start_time:.4f}秒')

    # 使用自定义关键字参数
    start_time = time.time()
    results_custom = run_custom_process(power, numbers, exponent=3, max_workers=3)
    end_time = time.time()

    print(f'指数为3的结果: {results_custom}')
    print(f'自定义指数执行时间: {end_time - start_time:.4f}秒')
    print(f'结果正确: {results_default == [x**2 for x in numbers] and results_custom == [x**3 for x in numbers]}\n')

    # 测试6: 与原始测试程序的兼容性
    print('测试6: 与原始测试程序的兼容性')

    # 模拟原始测试程序的调用方式
    task_ids = list(range(16))  # 假设有16个任务
    start_time = time.time()
    results = run_custom_process(process_task, task_ids, max_workers=8)
    end_time = time.time()

    print(f'任务数量: {len(task_ids)}')
    print(f'执行时间: {end_time - start_time:.4f}秒')
    print(f'结果示例: {results[:3]}...{results[-3:]}')
    print(f'所有任务完成: {all('completed' in result for result in results)}\n')

    # 测试7: 异步函数的并行执行（通过同步包装器）
    print('测试7: 异步函数的并行执行')

    # 测试异步平方函数
    numbers = list(range(10))
    start_time = time.time()
    results = run_custom_process(async_square_sync, numbers, max_workers=5)
    end_time = time.time()

    print(f'异步平方函数输入: {numbers}')
    print(f'异步平方函数结果: {results}')
    print(f'异步平方函数执行时间: {end_time - start_time:.4f}秒')
    print(f'异步平方函数结果正确: {results == [x * x for x in numbers]}')

    # 测试异步加法函数
    list1 = [1, 2, 3, 4, 5]
    list2 = [10, 20, 30, 40, 50]
    start_time = time.time()
    results = run_custom_process(async_add_sync, list1, list2, max_workers=3)
    end_time = time.time()

    print(f'异步加法函数输入1: {list1}')
    print(f'异步加法函数输入2: {list2}')
    print(f'异步加法函数结果: {results}')
    print(f'异步加法函数执行时间: {end_time - start_time:.4f}秒')
    print(f'异步加法函数结果正确: {results == [x + y for x, y in zip(list1, list2, strict=False)]}\n')


def main():
    """主测试函数"""
    print("开始测试 process.py 功能...")
    test_basic_function()
    test_error_retry()
    test_process_manager()
    test_process_manager_methods()  # 测试ProcessManager的新方法
    test_run_custom_process()
    test_run_custom_process_detailed()  # 详细测试run_custom_process的各种功能
    print("\n所有测试完成!")


if __name__ == "__main__":
    main()
