# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 19:25:55
LastEditTime : 2025-09-06 20:12:09
FilePath     : /CODE/xjLib/xt_thread/test/test_process.py
Github       : https://github.com/sandorn/home
==============================================================
"""


import asyncio
import time

# 直接从同级目录的process.py导入
from xt_thread.process import run_custom_process


# 定义顶层测试函数，避免嵌套函数无法序列化的问题
def square(x):
    """计算平方并模拟工作负载"""
    time.sleep(0.1)  # 模拟耗时操作
    return x * x


def add(x, y):
    """计算两数之和并模拟工作负载"""
    time.sleep(0.1)  # 模拟耗时操作
    return x + y


def divide(x, y):
    """执行除法操作，测试异常处理"""
    time.sleep(0.1)  # 模拟耗时操作
    return x / y


def process_number(x):
    """模拟复杂的数值处理"""
    time.sleep(0.05)  # 模拟中等耗时操作
    return sum(i for i in range(x))


def power(x, exponent=2):
    """计算x的exponent次方"""
    time.sleep(0.1)  # 模拟耗时操作
    return x ** exponent


def process_task(task_id):
    """模拟原始测试程序中的任务处理函数"""
    time.sleep(0.2)  # 模拟工作负载
    return f"Task {task_id} completed"


async def async_square(x):
    """异步计算平方函数"""
    await asyncio.sleep(0.1)  # 模拟异步I/O操作
    return x * x


async def async_add(x, y):
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


def async_square_sync(x):
    """异步平方函数的同步包装器"""
    return sync_wrapper(async_square, x)


def async_add_sync(x, y):
    """异步加法函数的同步包装器"""
    return sync_wrapper(async_add, x, y)


def test_simple_function():
    """测试简单函数的并行执行"""
    print("测试1: 简单函数的并行执行")
    
    # 并行计算多个数的平方
    numbers = list(range(10))
    start_time = time.time()
    results = run_custom_process(square, numbers, max_workers=5)
    end_time = time.time()
    
    print(f"输入: {numbers}")
    print(f"结果: {results}")
    print(f"执行时间: {end_time - start_time:.4f}秒")
    print(f"预期结果: {[x*x for x in numbers]}")
    print(f"结果正确: {results == [x*x for x in numbers]}\n")


def test_multi_argument():
    """测试多参数函数的并行执行"""
    print("测试2: 多参数函数的并行执行")
    
    # 并行计算多组数的和
    list1 = [1, 2, 3, 4, 5]
    list2 = [10, 20, 30, 40, 50]
    start_time = time.time()
    results = run_custom_process(add, list1, list2, max_workers=3)
    end_time = time.time()
    
    print(f"输入1: {list1}")
    print(f"输入2: {list2}")
    print(f"结果: {results}")
    print(f"执行时间: {end_time - start_time:.4f}秒")
    print(f"预期结果: {[x+y for x,y in zip(list1, list2)]}")
    print(f"结果正确: {results == [x+y for x,y in zip(list1, list2)]}\n")


def test_exception_handling():
    """测试异常处理功能"""
    print("测试3: 异常处理功能")
    
    # 包含会引发异常的输入
    numerators = [10, 20, 30, 40]
    denominators = [2, 0, 5, 8]  # 第二个元素会导致ZeroDivisionError
    start_time = time.time()
    results = run_custom_process(divide, numerators, denominators, max_workers=4)
    end_time = time.time()
    
    print(f"分子: {numerators}")
    print(f"分母: {denominators}")
    print(f"结果: {results}")
    print(f"执行时间: {end_time - start_time:.4f}秒")
    print(f"异常处理正常: {'ZeroDivisionError' in str(results[1])}\n")


def test_large_scale():
    """测试大规模任务处理性能"""
    print("测试4: 大规模任务处理性能")
    
    # 生成大规模任务
    large_list = list(range(100))
    start_time = time.time()
    results = run_custom_process(process_number, large_list, max_workers=8)
    end_time = time.time()
    
    print(f"任务数量: {len(large_list)}")
    print(f"总执行时间: {end_time - start_time:.4f}秒")
    print(f"平均每个任务执行时间: {(end_time - start_time) * 1000 / len(large_list):.2f}毫秒")
    print(f"结果示例: {results[:5]}...{results[-5:]}\n")


def test_kwargs_support():
    """测试关键字参数支持"""
    print("测试5: 关键字参数支持")
    
    # 使用默认关键字参数
    numbers = [1, 2, 3, 4, 5]
    start_time = time.time()
    results_default = run_custom_process(power, numbers, max_workers=3)
    end_time = time.time()
    
    print(f"输入: {numbers}")
    print(f"默认指数结果: {results_default}")
    print(f"默认指数执行时间: {end_time - start_time:.4f}秒")
    
    # 使用自定义关键字参数
    start_time = time.time()
    results_custom = run_custom_process(power, numbers, exponent=3, max_workers=3)
    end_time = time.time()
    
    print(f"指数为3的结果: {results_custom}")
    print(f"自定义指数执行时间: {end_time - start_time:.4f}秒")
    print(f"结果正确: {results_default == [x**2 for x in numbers] and results_custom == [x**3 for x in numbers]}\n")


def test_with_original_example():
    """测试与原始测试程序的兼容性"""
    print("测试6: 与原始测试程序的兼容性")
    
    # 模拟原始测试程序的调用方式
    task_ids = list(range(16))  # 假设有16个任务
    start_time = time.time()
    results = run_custom_process(process_task, task_ids, max_workers=8)
    end_time = time.time()
    
    print(f"任务数量: {len(task_ids)}")
    print(f"执行时间: {end_time - start_time:.4f}秒")
    print(f"结果示例: {results[:3]}...{results[-3:]}")
    print(f"所有任务完成: {all('completed' in result for result in results)}\n")


def test_async_function():  # 测试7
    """测试异步函数的并行执行（通过同步包装器）"""
    print("测试7: 异步函数的并行执行")
    
    # 测试异步平方函数
    numbers = list(range(10))
    start_time = time.time()
    results = run_custom_process(async_square_sync, numbers, max_workers=5)
    end_time = time.time()
    
    print(f"异步平方函数输入: {numbers}")
    print(f"异步平方函数结果: {results}")
    print(f"异步平方函数执行时间: {end_time - start_time:.4f}秒")
    print(f"异步平方函数结果正确: {results == [x*x for x in numbers]}")
    
    # 测试异步加法函数
    list1 = [1, 2, 3, 4, 5]
    list2 = [10, 20, 30, 40, 50]
    start_time = time.time()
    results = run_custom_process(async_add_sync, list1, list2, max_workers=3)
    end_time = time.time()
    
    print(f"异步加法函数输入1: {list1}")
    print(f"异步加法函数输入2: {list2}")
    print(f"异步加法函数结果: {results}")
    print(f"异步加法函数执行时间: {end_time - start_time:.4f}秒")
    print(f"异步加法函数结果正确: {results == [x+y for x,y in zip(list1, list2)]}\n")


def run_all_tests():
    """运行所有测试"""
    print("="*50)
    print("运行所有测试")
    print("="*50)
    test_simple_function()
    test_multi_argument()
    test_exception_handling()
    test_large_scale()
    test_kwargs_support()
    test_with_original_example()
    test_async_function()
    print("所有测试完成")
    print("="*50)


if __name__ == "__main__":
    run_all_tests()