"""
==============================================================
Description  : wraps.py模块测试代码 - 测试线程装饰器模块的功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-07 17:30:00
FilePath     : /CODE/xjLib/xt_thread/test/test_wraps.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import random
import threading
import time

# 导入要测试的装饰器
from xt_thread.wraps import (
    ThreadWrapsManager,
    parallelize_wraps,
    qthread_wraps,
    run_in_qtthread,
    run_in_thread,
    thread_print,
    thread_safe,
    thread_wraps,
)

# 准备测试数据和辅助函数
global_counter = 0
shared_resource = []


# 1. 测试thread_safe装饰器
def test_01_thread_safe():
    """1. 测试thread_safe装饰器"""
    print("\n=== 1. 测试thread_safe装饰器 ===")
    
    # 测试共享资源访问
    @thread_safe
    def increment_global_counter():
        """增加全局计数器的线程安全函数"""
        global global_counter
        current_value = global_counter
        # 模拟并发竞争条件
        time.sleep(0.001)
        global_counter = current_value + 1
    
    @thread_safe
    def add_to_shared_resource(item):
        """向共享资源添加元素的线程安全函数"""
        shared_resource.append(item)
        time.sleep(0.001)  # 模拟耗时操作
    
    # 创建多个线程并发访问共享资源
    threads = []
    for i in range(100):
        t = threading.Thread(target=increment_global_counter)
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print(f"全局计数器期望值: 100, 实际值: {global_counter}")
    
    # 测试向共享资源添加元素
    threads = []
    for i in range(50):
        t = threading.Thread(target=add_to_shared_resource, args=(i,))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print(f"共享资源长度期望值: 50, 实际值: {len(shared_resource)}")
    
    # 测试内置函数的线程安全包装
    @thread_safe
    def safe_print(*args, **kwargs):
        """线程安全的打印函数"""
        print(*args, **kwargs)
    
    # 创建多个线程并发打印
    threads = []
    for i in range(10):
        t = threading.Thread(target=safe_print, args=(f"线程安全打印测试 {i}",))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()


# 2. 测试thread_print装饰器
def test_02_thread_print():
    """2. 测试thread_print装饰器"""
    print("\n=== 2. 测试thread_print装饰器 ===")
    
    def concurrent_print_task(task_id):
        """并发打印任务"""
        for i in range(3):
            thread_print(f"任务 {task_id}, 迭代 {i}")
            time.sleep(0.01)  # 模拟并发条件
    
    # 创建多个线程并发打印
    threads = []
    for i in range(5):
        t = threading.Thread(target=concurrent_print_task, args=(i,))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    print("线程安全打印测试完成")


# 3. 测试run_in_thread装饰器
def test_03_run_in_thread():
    """3. 测试run_in_thread装饰器"""
    print("\n=== 3. 测试run_in_thread装饰器 ===")
    
    @run_in_thread
    def simple_task():
        """简单任务函数"""
        time.sleep(0.2)
        return "任务成功"
    
    @run_in_thread
    def parameterized_task(x, y=0):
        """带参数的任务函数"""
        time.sleep(0.1)
        return f"参数: {x}, {y}", x + y
    
    # 测试基本功能
    thread = simple_task()
    result = thread.get_result()
    print(f"run_in_thread结果: {result}")
    
    # 测试带参数的任务
    thread = parameterized_task(10, 5)
    result = thread.get_result()
    print(f"带参数的run_in_thread结果: {result}")
    
    # 测试多个线程并发执行
    threads = []
    for i in range(3):
        thread = parameterized_task(i, i*2)
        threads.append(thread)
    
    # 获取所有结果
    for i, thread in enumerate(threads):
        result = thread.get_result()
        print(f"线程 {i} 结果: {result}")


# 4. 测试thread_wraps装饰器
def test_04_thread_wraps():
    """4. 测试thread_wraps装饰器"""
    print("\n=== 4. 测试thread_wraps装饰器 ===")
    
    @thread_wraps
    def decorated_task():
        """被装饰的简单任务"""
        time.sleep(0.1)
        return "装饰器任务成功"
    
    # 测试基本功能
    thread = decorated_task()
    result = thread.get_result()
    print(f"thread_wraps结果: {result}")
    
    # 测试带回调函数的情况
    @thread_wraps
    def task_with_result(x):
        """带返回值的任务"""
        time.sleep(0.1)
        return x * 2
    
    def custom_callback(result):
        """自定义回调函数"""
        print(f"回调函数收到结果: {result}")
        return result + 10
    
    thread = task_with_result(5, callback=custom_callback)
    result = thread.get_result()
    print(f"带回调的thread_wraps结果: {result} (期望: 20)")
    
    # 测试守护线程参数
    @thread_wraps(daemon=False)
    def daemon_task():
        """守护线程任务"""
        time.sleep(0.5)
        return "守护线程完成"
    
    thread = daemon_task()
    print(f"守护线程状态: {thread.daemon}")
    
    # 测试重试机制
    @thread_wraps(max_retries=2)
    def retry_task():
        """可能失败的重试任务"""
        if random.random() < 0.7:
            raise ValueError("随机失败")
        return "重试成功"
    
    thread = retry_task()
    try:
        result = thread.get_result()
        print(f"重试任务结果: {result}")
    except Exception as e:
        print(f"重试任务最终失败: {e}")


# 5. 测试ThreadWrapsManager类
def test_05_thread_wraps_manager():
    """5. 测试ThreadWrapsManager类"""
    print("\n=== 5. 测试ThreadWrapsManager类 ===")
    
    @ThreadWrapsManager
    def class_decorated_task(x):
        """被ThreadWrapsManager装饰的任务"""
        time.sleep(0.1)
        return f"类装饰器结果: {x * 3}"
    
    # 创建多个线程
    threads = []
    for i in range(5):
        thread = class_decorated_task(i)
        threads.append(thread)
    
    # 获取单个结果
    for i, thread in enumerate(threads):
        result = thread.get_result()
        print(f"线程 {i} 结果: {result}")
    
    # 获取所有结果
    all_results = ThreadWrapsManager.getAllResult()
    print(f"所有线程结果数量: {len(all_results)}")
    
    # 测试清除功能
    ThreadWrapsManager.clear()
    all_results = ThreadWrapsManager.getAllResult()
    print(f"清除后所有线程结果数量: {len(all_results)}")


# 6. 测试parallelize_wraps装饰器
def test_06_parallelize_wraps():
    """6. 测试parallelize_wraps装饰器"""
    print("\n=== 6. 测试parallelize_wraps装饰器 ===")
    
    @parallelize_wraps
    def parallel_square(x):
        """并行计算平方"""
        time.sleep(0.05)  # 模拟耗时操作
        return x * x
    
    @parallelize_wraps
    def process_with_error(x):
        """可能失败的并行处理"""
        time.sleep(0.05)
        if x % 3 == 0:
            raise ValueError(f"处理值 {x} 时出错")
        return x * 2
    
    # 测试基本并行处理
    data = list(range(10))
    
    # 测量并行处理时间
    start_time = time.time()
    results = parallel_square(data)
    end_time = time.time()
    
    print(f"并行处理结果: {results}")
    print(f"并行处理耗时: {end_time - start_time:.4f}秒")
    
    # 测试串行处理时间进行对比
    start_time = time.time()
    serial_results = [x * x for x in data]
    end_time = time.time()
    
    print(f"串行处理耗时: {end_time - start_time:.4f}秒")
    print(f"结果一致性: {results == serial_results}")
    
    # 测试自定义线程池大小
    start_time = time.time()
    results = parallel_square(data, max_workers=2)
    end_time = time.time()
    
    print(f"自定义线程池大小(2)处理耗时: {end_time - start_time:.4f}秒")
    
    # 测试异常处理
    try:
        results = process_with_error(data)
    except Exception as e:
        print(f"并行处理异常测试: 正确捕获到异常 - {e}")


# 7. 测试run_in_qtthread装饰器
def test_07_run_in_qtthread():
    """7. 测试run_in_qtthread装饰器"""
    print("\n=== 7. 测试run_in_qtthread装饰器 ===")
    
    @run_in_qtthread
    def qt_task(x):
        """Qt线程任务"""
        time.sleep(0.2)
        return f"Qt线程处理结果: {x * 10}"
    
    # 测试基本功能
    thread = qt_task(5)
    result = thread.get_result()
    print(f"run_in_qtthread结果: {result}")
    
    # 测试带超时的结果获取
    thread = qt_task(10)
    result = thread.get_result(timeout=0.3)  # 超时时间足够长
    print(f"带超时的run_in_qtthread结果: {result}")
    
    # 测试多个Qt线程
    threads = []
    for i in range(3):
        thread = qt_task(i)
        threads.append(thread)
    
    # 获取所有结果
    for i, thread in enumerate(threads):
        result = thread.get_result()
        print(f"Qt线程 {i} 结果: {result}")


# 8. 测试qthread_wraps装饰器
def test_08_qthread_wraps():
    """8. 测试qthread_wraps装饰器"""
    print("\n=== 8. 测试qthread_wraps装饰器 ===")
    
    @qthread_wraps
    def qt_wrapped_task(x):
        """被qthread_wraps装饰的任务"""
        time.sleep(0.1)
        return f"Qt装饰器处理结果: {x * 5}"
    
    # 测试基本功能
    thread = qt_wrapped_task(4)
    result = thread.get_result()
    print(f"qthread_wraps结果: {result}")
    
    # 测试带重试机制的Qt线程
    @qthread_wraps
    def qt_retry_task():
        """可能失败的Qt线程任务"""
        if random.random() < 0.7:
            raise ValueError("Qt任务随机失败")
        return "Qt任务重试成功"
    
    thread = qt_retry_task(max_retries=3, retry_delay=0.2)
    try:
        result = thread.get_result()
        print(f"Qt重试任务结果: {result}")
    except Exception as e:
        print(f"Qt重试任务最终失败: {e}")
    
    # 测试带回调的Qt线程
    def qt_callback(result):
        """Qt线程回调函数"""
        print(f"Qt回调函数收到结果: {result}")
        return result + " (已处理)"
    
    thread = qt_wrapped_task(6, callback=qt_callback)
    result = thread.get_result()
    print(f"带回调的qthread_wraps结果: {result}")


# 9. 测试装饰器组合使用
def test_09_all_decorators_combined():
    """9. 测试装饰器组合使用"""
    print("\n=== 9. 测试装饰器组合使用 ===")
    
    @thread_safe
    @run_in_thread
    def combined_task(x):
        """组合使用thread_safe和run_in_thread的任务"""
        time.sleep(0.1)
        return f"组合装饰器结果: {x * 100}"
    
    # 测试基本功能
    thread = combined_task(5)
    result = thread.get_result()
    print(f"组合装饰器结果: {result}")
    
    # 测试多个线程并发访问
    threads = []
    for i in range(3):
        thread = combined_task(i)
        threads.append(thread)
    
    # 获取所有结果
    for i, thread in enumerate(threads):
        result = thread.get_result()
        print(f"组合装饰器线程 {i} 结果: {result}")


# 10. 测试异常处理
def test_10_exception_handling():
    """10. 测试异常处理"""
    print("\n=== 10. 测试异常处理 ===")
    
    @run_in_thread
    def task_with_exception():
        """会抛出异常的任务"""
        time.sleep(0.1)
        raise ValueError("测试异常")
    
    @thread_wraps
    def wrapped_task_with_exception():
        """会抛出异常的装饰器任务"""
        time.sleep(0.1)
        raise RuntimeError("包装任务异常")
    
    # 测试run_in_thread异常处理
    thread = task_with_exception()
    try:
        result = thread.get_result()
    except Exception as e:
        print(f"run_in_thread异常测试: 正确捕获到异常 - {e}")
    
    # 测试thread_wraps异常处理
    thread = wrapped_task_with_exception()
    try:
        result = thread.get_result()
    except Exception as e:
        print(f"thread_wraps异常测试: 正确捕获到异常 - {e}")


def test_11_thread_wraps():
    """11. 测试thread_wraps装饰器"""
    print("\n=== 11. 测试thread_wraps装饰器 ===")

    @thread_wraps
    def decorated_task():
        """被装饰的简单任务"""
        time.sleep(0.1)
        return "装饰器任务成功"

    # 测试基本功能
    thread = decorated_task()
    result = thread.get_result()
    print(f"thread_wraps结果: {result}")

    # 测试带回调函数的情况
    @thread_wraps
    def task_with_result(x):
        """带返回值的任务"""
        time.sleep(0.1)
        return x * 2

    def custom_callback(result):
        """自定义回调函数"""
        print(f"回调函数收到结果: {result}")
        return result + 10

    thread = task_with_result(5, callback=custom_callback)
    result = thread.get_result()
    print(f"带回调的thread_wraps结果: {result} (期望: 20)")

    # 测试守护线程参数
    @thread_wraps(daemon=True)
    def daemon_task():
        """守护线程任务"""
        time.sleep(0.5)
        return "守护线程完成"

    thread = daemon_task()
    print(f"守护线程状态: {thread.daemon}")

    # 测试重试机制 - 使用带参数的装饰器
    @thread_wraps(daemon=True, max_retries=3)
    def retry_task():
        """可能失败的重试任务"""
        if random.random() < 0.7:
            raise ValueError("随机失败")
        return "重试成功"

    # 调用时不传递max_retries参数
    thread = retry_task()
    try:
        result = thread.get_result()
        print(f"重试任务结果: {result}")
    except Exception as e:
        print(f"重试任务最终失败: {e}")

# 运行所有测试
def run_all_tests():
    """运行所有测试函数"""
    print("开始运行所有wraps.py装饰器测试...")
    
    # 按顺序运行所有测试
    test_01_thread_safe()
    test_02_thread_print()
    test_03_run_in_thread()
    test_04_thread_wraps()
    test_05_thread_wraps_manager()
    test_06_parallelize_wraps()
    test_07_run_in_qtthread()
    test_08_qthread_wraps()
    test_09_all_decorators_combined()
    test_10_exception_handling()
    test_11_thread_wraps()
    
    print("\n所有测试运行完成!")


if __name__ == "__main__":
    run_all_tests()