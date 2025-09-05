import time
import weakref
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from PyQt6.QtCore import (
    QMutex,
    QMutexLocker,
    QThread,
    QTimer,
    QWaitCondition,
    pyqtSignal,
)
from xt_thread import thread_print
from xt_wraps import SingletonMixin


class QtThreadBase(QThread):
    """
    基于 QThread 的增强型线程基类
    
    Features:
    - 提供结果获取功能
    - 支持安全停止线程
    - 自动资源清理
    - 异常处理和信号通知
    
    Signals:
    - finished_signal: 线程完成时发射，携带执行结果
    - error_signal: 线程发生错误时发射，携带异常信息
    """
    finished_signal = pyqtSignal(object)  # 线程完成信号，携带结果
    error_signal = pyqtSignal(Exception)  # 错误信号，携带异常
    
    def __init__(self, target: Callable, *args, **kwargs):
        """
        初始化线程
        
        Args:
            target: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
        """
        super().__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self._exception = None
        self._is_running = False
        self._stop_requested = False
        self._mutex = QMutex()
        self._condition = QWaitCondition()
        
        # 设置线程名称
        self.setObjectName(target.__name__)
        # 连接信号
        self.finished.connect(self._on_finished)

    def _on_finished(self) -> None:
        """线程完成时的处理"""
        self.finished_signal.emit(self)

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.is_running():
            self.stop()
        return False  # 不抑制异常

    def run(self) -> None:
        """线程主执行方法"""
        self._is_running = True
        
        try:
            if not self._stop_requested:
                self._result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._exception = e
            self.error_signal.emit(e)
        finally:
            self._is_running = False

    def get_result(self, timeout: Optional[float] = None) -> Any:
        """
        获取线程执行结果，等待线程完成
        
        Args:
            timeout: 超时时间（秒），None表示无限等待
            
        Returns:
            线程执行结果，如果超时或出错返回None
        """
        # 等待线程完成
        if self.isRunning() or self._is_running:
            if timeout is not None:
                wait_time = int(timeout * 1000)  # 转换为毫秒
                success = self.wait(wait_time)
            else:
                success = self.wait()
        else:
            success = True
            
        return self._result if success else None

    def stop(self, timeout: Optional[float] = None) -> bool:
        """
        安全停止线程
        
        Args:
            timeout: 等待线程停止的超时时间（秒）
            
        Returns:
            bool: 是否成功停止线程
        """
        if self._is_running:
            self._stop_requested = True
            
            # 请求线程退出
            self.quit()
            
            # 等待线程实际停止
            if timeout is not None:
                wait_time = int(timeout * 1000)  # 转换为毫秒
                return self.wait(wait_time)
            else:
                return self.wait()
                
        return True

    def is_running(self) -> bool:
        """检查线程是否正在运行"""
        return self._is_running or self.isRunning()

    def get_exception(self) -> Optional[Exception]:
        """获取线程执行过程中的异常"""
        return self._exception

    def __del__(self):
        """对象销毁时自动清理资源"""
        if self.is_running():
            self.stop(timeout=1.0)


class QtSafeThread(QtThreadBase):
    """
    安全线程类，提供异常捕获和重试机制
    
    适用于需要异常处理和重试的任务
    
    Usage:
        def risky_task():
            # 可能失败的任务
            if random.random() < 0.3:
                raise ValueError("随机失败")
            return "成功"
            
        thread = QtSafeThread(risky_task, max_retries=3)
        thread.start()
    """
    
    def __init__(self, target: Callable, *args, max_retries: int = 0, retry_delay: float = 1.0, **kwargs):
        super().__init__(target, *args, **kwargs)
        self.max_retries = max_retries
        self.retry_count = 0
        self.retry_delay = retry_delay  # 重试延迟（秒）

    def run(self) -> None:
        """重写run方法，添加重试机制"""
        self._is_running = True
        
        while self.retry_count <= self.max_retries and not self._stop_requested:
            try:
                self._result = self._target(*self._args, **self._kwargs)
                break  # 成功执行，退出循环
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    self._exception = e
                    self.error_signal.emit(e)
                    break
                else:
                    time.sleep(self.retry_delay)
            finally:
                self._is_running = False

class QtThreadManager(SingletonMixin):
    """
    QThread 线程管理器，用于管理所有线程实例
    
    Features:
    - 全局线程跟踪
    - 批量停止和等待
    - 结果收集
    - 线程安全
    """
    
    _threads: Dict[int, weakref.ref] = {}
    _mutex = QMutex()
    
    def __init__(self): 
        """初始化线程管理器"""
        super().__init__()

    @classmethod
    def create_thread(cls, target: Callable, *args, **kwargs) -> QtThreadBase:
        """
        创建并启动线程，自动添加到管理器
        
        Args:
            target: 要执行的函数
            *args: 函数参数
            *kwargs: 函数关键字参数
            
        Returns:
            创建的线程实例
        """
        _thread = QtThreadBase(target, *args, **kwargs)
        
        with QMutexLocker(cls._mutex):
            cls._threads[id(_thread)] = weakref.ref(_thread)
        
        _thread.start()
        return _thread

    @classmethod
    def create_safe_thread(cls, target: Callable, *args, **kwargs) -> QtSafeThread:
        """
        创建并启动安全线程，自动添加到管理器
        
        Args:
            target: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            创建的安全线程实例
        """
        thread = QtSafeThread(target, *args, **kwargs)
        
        with QMutexLocker(cls._mutex):
            cls._threads[id(thread)] = weakref.ref(thread)
        
        thread.start()
        return thread

    @classmethod
    def add_thread(cls, thread: Union[QtThreadBase, QtSafeThread]) -> None:
        """
        将已存在的线程添加到管理器
        
        Args:
            thread: 要添加的线程实例
        """
        with QMutexLocker(cls._mutex):
            cls._threads[id(thread)] = weakref.ref(thread)

    @classmethod
    def stop_all(cls, timeout: Optional[float] = None) -> None:
        """
        停止所有管理的线程
        
        Args:
            timeout: 等待每个线程停止的超时时间（秒）
        """
        with QMutexLocker(cls._mutex):
            threads_to_stop = []
            # 收集所有有效的线程引用
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None and thread.is_running():
                    threads_to_stop.append(thread)
                else:
                    # 清理无效引用
                    del cls._threads[thread_id]
            
            # 停止所有线程
            for thread in threads_to_stop:
                thread.stop(timeout)
                
            # 清理所有引用
            cls._threads.clear()

    @classmethod
    def wait_all_completed(cls, timeout: Optional[float] = None) -> Dict[int, Any]:
        """
        等待所有线程完成并返回结果
        
        Args:
            timeout: 等待所有线程完成的超时时间（秒）
            
        Returns:
            所有线程的结果字典，键为线程ID，值为结果
        """
        # 创建一个字典来存储所有线程的结果
        results = {}
        
        # 获取当前时间，用于计算超时
        start_time = time.time()
        
        # 复制当前所有的线程引用，以便在等待过程中不会丢失
        thread_list = []
        with QMutexLocker(cls._mutex):
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread is not None:
                    thread_list.append(thread)
        
        # 等待所有线程完成并直接从每个线程获取结果
        for thread in thread_list:
            # 等待线程完成，但不依赖get_result()方法
            while thread.is_running():
                # 检查是否超时
                if timeout is not None and time.time() - start_time > timeout:
                    break
                # 短暂休眠
                time.sleep(0.01)
            
            # 直接从线程实例获取结果
            thread_id = id(thread)
            results[thread_id] = thread._result
        
        # 清空并返回结果
        with QMutexLocker(cls._mutex):
            cls._threads.clear()
            
        return results

    @classmethod
    def get_active_count(cls) -> int:
        """
        获取当前活动的线程数量
        
        Returns:
            当前活动的线程数量
        """
        with QMutexLocker(cls._mutex):
            count = 0
            # 清理已经结束的线程引用 
            for thread_id, thread_ref in list(cls._threads.items()): 
                thread = thread_ref()
                if thread is not None and thread.is_running(): 
                    count += 1
                else:
                    del cls._threads[thread_id]
            return count
        
    @classmethod
    def get_thread_by_id(cls, thread_id: int) -> Optional[QtThreadBase]:
        """
        根据ID获取线程实例
        
        Args:
            thread_id: 线程ID
            
        Returns:
            线程实例，如果不存在返回None
        """
        with QMutexLocker(cls._mutex):
            thread_ref = cls._threads.get(thread_id)
            return thread_ref() if thread_ref else None

    @classmethod
    def get_thread_by_name(cls, name: str) -> List[QtThreadBase]:
        """
        根据名称获取线程实例列表
        
        Args:
            name: 线程名称
            
        Returns:
            匹配名称的线程实例列表
        """
        result = []
        with QMutexLocker(cls._mutex):
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread and thread.objectName() == name:
                    result.append(thread)
        return result

    @classmethod
    def stop_thread(cls, thread_id: int, timeout: Optional[float] = None) -> bool:
        """
        停止指定线程
        
        Args:
            thread_id: 线程ID
            timeout: 等待线程停止的超时时间（秒）
            
        Returns:
            bool: 是否成功停止线程
        """
        thread = cls.get_thread_by_id(thread_id)
        if thread and thread.is_running():
            return thread.stop(timeout)
        return False


class SingletonQtThread(SingletonMixin, QtSafeThread):
    """
    单例线程类，确保同一目标函数只有一个线程实例
    
    Features:
    - 单例模式保证唯一性
    - 自动线程管理
    - 安全停止机制
    """
    
    def __init__(self, target: Callable, *args, **kwargs):
        # 让SingletonMixin来管理单例实例
        super().__init__(target, *args, **kwargs)
        
        # 确保所有必要的属性都已初始化
        if not hasattr(self, "_is_running"):
            self._is_running = False
        if not hasattr(self, "_stop_requested"):
            self._stop_requested = False
        if not hasattr(self, "_result"):
            self._result = None
        
        # 只在新实例创建时自动启动
        if not self.isRunning() and not self._is_running:
            self.start()

    def start(self) -> None:
        """启动线程，但只允许启动一次"""
        if not self.isRunning():
            super().start()

    def restart(self) -> None:
        """重启单例线程"""
        if self.isRunning() or self._is_running:
            # 先停止当前线程
            self.stop()
            
            # 重置状态
            self._is_running = False
            self._stop_requested = False
            # 不重置_result，保留最后一次执行的结果
            # self._result = None
            self._exception = None
            self.retry_count = 0
            
            # 重新启动
            self.start()


# 便捷函数
def run_in_qtthread(func: Callable) -> Callable:
    """
    装饰器，将函数在 QThread 中执行
    
    Usage:
        @run_in_qtthread
        def long_running_task(param):
            # 长时间运行的任务
            return result
            
        # 调用方式不变，但会在 QThread 中执行
        result_future = long_running_task(param)
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> QtThreadBase:
        thread = QtThreadManager.create_thread(func, *args, **kwargs)
        return thread
    
    return wrapper


# 示例用法
if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication
    
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 示例函数
    def sample_task(task_id: int) -> str:
        """示例任务函数，模拟耗时操作"""
        thread_print(f"任务 {task_id} 开始，需要 1 秒")
        time.sleep(0.1)
        thread_print(result := f"任务 {task_id} 完成")
        return result
    
    # 测试 QtThreadManager
    thread_print("=== 测试 QtThreadManager[DEBUG] ===")
    
    all_threads = []
    # 创建多个线程
    for i in range(3):
        _thread = QtThreadManager.create_thread(sample_task, i)
        # 连接信号
        _thread.finished_signal.connect(
            lambda self, tid=i: thread_print(f"任务 {tid} 完成信号: {self._result}")
        )
        _thread.error_signal.connect(lambda e: thread_print(f"线程错误: {e}"))
        all_threads.append(_thread)
        
    thread_print(f"活动线程数: {QtThreadManager.get_active_count()}")
    
    # 等待所有线程完成
    results = QtThreadManager.wait_all_completed()
    thread_print(f"所有线程完成，结果: {results}")

    @run_in_qtthread
    def decorated_task(x: int) -> int:
        """被装饰的任务函数"""
        thread_print(f"装饰器任务开始: {x}")
        time.sleep(1)
        result = x * 2
        thread_print(f"装饰器任务完成: {result}")
        return result
    # 调用被装饰的函数
    thread = decorated_task(5)
    result = thread.get_result()
    thread_print(f"装饰器任务结果: {result}")

    # 测试单例线程
    thread_print("\n=== 测试单例线程 ===")

    def singleton_task(*args):
        """单例任务函数"""
        thread_print("单例任务执行中")
        time.sleep(1)
        return f"单例任务完成{args}"

    # 创建单例线程
    thread1 = SingletonQtThread(singleton_task,1,2,3)
    thread2 = SingletonQtThread(singleton_task,4,5,6)

    thread_print(f"线程1和线程2是同一个实例: {thread1 is thread2}")

    # 等待完成
    result1 = thread1.get_result()
    result2 = thread2.get_result()  # thread2 是同一个实例
    thread_print(f"线程1结果: {result1}, 线程2结果: {result2}")


    # 启动事件循环以确保信号被处理
    QTimer.singleShot(100, app.quit)  # 100ms后退出应用
    app.exec()