import random
import sys
import time

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from xt_thread import (
    ComposedSingletonQtThread,
    QtThreadBase,
    QtThreadManager,
    SingletonQtThread,
)

# 创建应用实例
app = QApplication(sys.argv)

# 示例函数
def sample_task(task_id: int) -> str:
    """示例任务函数，模拟耗时操作"""
    print(f"任务 {task_id} 开始，需要 0.1 秒")
    time.sleep(0.1)
    print(result := f"任务 {task_id} 完成")
    return result

def error_task(task_id: int) -> str:
    """会抛出异常的任务函数，用于测试异常处理"""
    print(f"错误任务 {task_id} 开始")
    time.sleep(0.1)
    raise ValueError(f"任务 {task_id} 故意抛出异常")

def retry_task(task_id: int) -> str:
    """有概率失败的任务，用于测试重试机制"""
    print(f"重试任务 {task_id} 开始")
    time.sleep(0.1)
    if random.random() < 0.7:  # 70%概率失败
        raise ValueError(f"重试任务 {task_id} 随机失败")
    return f"重试任务 {task_id} 成功完成"

def callback_function(result: str) -> str:
    """测试用的回调函数"""
    return f"[回调处理后] {result}"

def long_running_task(task_id: int) -> str:
    """长时间运行的任务，用于测试超时功能"""
    print(f"长时间任务 {task_id} 开始，需要 3 秒")
    time.sleep(3)
    return f"长时间任务 {task_id} 完成"

# 用于跟踪信号是否被触发
signal_triggered = False
error_occurred = False

def on_finished_callback(thread_obj):
    """线程完成信号的回调函数"""
    global signal_triggered
    signal_triggered = True
    print(
        f"信号回调: 线程 {thread_obj.objectName()} 完成，结果: {thread_obj._result}"
    )

def on_error_callback(exception):
    """线程错误信号的回调函数"""
    global error_occurred
    error_occurred = True
    print(f"错误信号回调: 发生异常 - {exception}")

# 测试 1: 基本线程管理功能
print("=== 测试 1: QtThreadManager 基本功能 ===")

all_threads = []
# 创建多个线程
for i in range(3):
    _thread = QtThreadManager.create_thread(sample_task, i)
    # 连接信号
    _thread.finished_signal.connect(on_finished_callback)
    _thread.error_signal.connect(on_error_callback)
    all_threads.append(_thread)

# 创建带回调函数的线程
callback_thread = QtThreadManager.create_thread(
    sample_task, 99, callback=callback_function
)
callback_thread.finished_signal.connect(on_finished_callback)
all_threads.append(callback_thread)

print(f"活动线程数: {QtThreadManager.get_active_count()}")

# 等待所有线程完成
results = QtThreadManager.wait_all_completed()
print(f"所有线程完成，结果数量: {len(results)}")
print(f"信号是否被触发: {signal_triggered}")

# 测试 2: 异常处理功能
print("\n=== 测试 2: 异常处理功能 ===")
error_occurred = False

# 创建会抛出异常的线程
error_thread = QtThreadManager.create_thread(error_task, 100)
error_thread.error_signal.connect(on_error_callback)
error_thread.start()

# 等待线程完成并检查结果
error_result = error_thread.get_result()
print(f"错误线程结果: {error_result}")
print(f"异常信息: {error_thread.get_exception()}")
print(f"异常信号是否被触发: {error_occurred}")

# 测试 3: 重试机制
print("\n=== 测试 3: 安全线程重试机制 ===")

# 创建带重试机制的安全线程
safe_thread = QtThreadManager.create_safe_thread(
    retry_task, 200, max_retries=5, retry_delay=0.2
)
safe_thread.start()

# 等待线程完成
retry_result = safe_thread.get_result()
print(f"重试线程结果: {retry_result}")
print(f"实际重试次数: {safe_thread.retry_count}")

# 测试 4: 单例线程
print("\n=== 测试 4: SingletonQtThread 单例模式 ===")

def singleton_task(*args):
    """单例任务函数"""
    print(f"单例任务执行中，参数: {args}")
    time.sleep(0.5)
    return f"单例任务完成{args}"

# 创建单例线程
thread1 = SingletonQtThread(singleton_task, 1, 2, 3)
thread2 = SingletonQtThread(singleton_task, 4, 5, 6)

print(f"线程1和线程2是同一个实例: {thread1 is thread2}")

# 等待完成
result1 = thread1.get_result()
result2 = thread2.get_result()  # thread2 是同一个实例
print(f"线程1结果: {result1}, 线程2结果: {result2}")

# 测试重启功能
print("\n测试单例线程重启功能:")
thread1.restart()
restart_result = thread1.get_result()
print(f"重启后结果: {restart_result}")

# 测试 5: 组合式单例线程
print("\n=== 测试 5: ComposedSingletonQtThread 组合式单例 ===")

def composed_singleton_task(*args):
    """组合式单例任务函数"""
    print(f"组合式单例任务执行中，参数: {args}")
    time.sleep(0.5)
    return f"组合式单例任务完成{args}"

# 创建组合式单例线程
comp_thread1 = ComposedSingletonQtThread(composed_singleton_task, "a", "b", "c")
comp_thread2 = ComposedSingletonQtThread(composed_singleton_task, "d", "e", "f")

print(f"组合线程1和组合线程2是同一个实例: {comp_thread1 is comp_thread2}")
print(f"组合线程1正在运行: {comp_thread1.is_running()}")

# 等待完成
comp_result1 = comp_thread1.get_result()
comp_result2 = comp_thread2.get_result()  # comp_thread2 是同一个实例
print(f"组合线程1结果: {comp_result1}, 组合线程2结果: {comp_result2}")

# 测试重启功能
print("\n测试组合式单例线程重启功能:")
comp_thread1.restart()
print(f"重启后，组合线程1正在运行: {comp_thread1.is_running()}")
new_result = comp_thread1.get_result()
print(f"重启后，组合线程1新结果: {new_result}")

# 清理单例实例
ComposedSingletonQtThread.clear_instances()
print("已清理所有组合式单例线程实例")

# 测试 6: 超时功能
print("\n=== 测试 6: 线程超时功能 ===")

# 创建长时间运行的线程
long_thread = QtThreadManager.create_thread(long_running_task, 300)
long_thread.start()

# 测试超时获取结果
timeout_result = long_thread.get_result(timeout=1.0)  # 1秒后超时
print(f"超时1秒后结果: {timeout_result}")
print(f"线程是否仍在运行: {long_thread.is_running()}")

# 等待线程真正完成
final_result = long_thread.get_result(timeout=5.0)
print(f"最终结果: {final_result}")

# 测试 7: 线程停止功能
print("\n=== 测试 7: 线程停止功能 ===")

# 创建新的长时间运行线程
stop_thread = QtThreadManager.create_thread(long_running_task, 400)
stop_thread.start()
time.sleep(0.5)  # 让线程运行一会儿

print(f"尝试停止线程，当前运行状态: {stop_thread.is_running()}")
stop_success = stop_thread.stop(timeout=1.0)
print(f"停止线程结果: {'成功' if stop_success else '失败'}")
print(f"停止后线程运行状态: {stop_thread.is_running()}")

# 测试 8: 上下文管理器
print("\n=== 测试 8: 上下文管理器功能 ===")

with QtThreadBase(sample_task, 500) as context_thread:
    print("线程已在上下文管理器中启动")

print("上下文管理器退出，线程应该已停止")
print(f"线程运行状态: {context_thread.is_running()}")

# 测试 9: 批量线程操作
print("\n=== 测试 9: 批量线程操作 ===")

# 创建多个线程
for i in range(5):
    QtThreadManager.create_thread(sample_task, 600 + i)

print(f"创建的线程数: {QtThreadManager.get_active_count()}")

# 等待所有线程完成
batch_results = QtThreadManager.wait_all_completed()
print(f"批量线程完成，结果数: {len(batch_results)}")
print(f"完成后活动线程数: {QtThreadManager.get_active_count()}")

print("\n=== 所有测试完成 ===")

# 启动事件循环以确保信号被处理
QTimer.singleShot(100, app.quit)  # 100ms后退出应用
app.exec()
