#!/usr/bin/env python
"""
==============================================================
Description  : 进程池管理模块 - 提供高效的并行任务处理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-10-09 15:00:00
Github       : https://github.com/sandorn/nsthread

本模块提供以下核心功能：
- ProcessBase：增强型进程基类,提供结果获取、安全停止和资源清理功能
- SafeProcess：安全进程类,提供异常捕获和重试机制
- ProcessManager：进程管理器,用于管理所有进程实例
- CustomProcess：自定义进程类,支持任务分片和结果收集
- run_custom_process：高级并行处理函数,简化多进程任务分发和结果汇总

主要特性：
- 基于Python内置multiprocessing模块,提供更易用的接口
- 支持任务分片处理,提高多核CPU利用率
- 统一的结果收集机制,保持任务执行顺序
- 完整的异常捕获和处理,确保程序稳定性
- 进程数量控制,避免资源耗尽
- 适用于IO密集型和CPU密集型任务
==============================================================
"""

from __future__ import annotations

import contextlib
import queue
import sys
import threading
import weakref
from collections.abc import Callable
from multiprocessing import Event, Manager, Process, Queue, Semaphore, get_context
from multiprocessing.synchronize import Event as EventType
from typing import Any, ClassVar

from xtlog import mylog

from .exception import safe_call
from .singleton import SingletonMixin


# 定义模块级别的包装函数，使其可以在子进程中被pickle序列化
def _target_wrapper(original_target: Callable[..., Any], args: tuple, kwargs: dict, callback: Callable[..., Any] | None, stop_event: EventType, result_queue: Queue) -> None:
    """进程目标函数包装器，用于在进程间传递结果和异常

    Args:
        original_target: 原始的目标函数
        args: 传递给目标函数的位置参数
        kwargs: 传递给目标函数的关键字参数
        callback: 进程执行完成后的回调函数
        stop_event: 用于安全停止进程的事件对象
        result_queue: 用于传递结果和异常的队列
    """
    result = exception = None

    try:
        if stop_event.is_set():
            return

        result = original_target(*args, **kwargs)
        if callable(callback):
            result = callback(result)

    except Exception as e:
        mylog.error('进程执行异常: {}', e)
        exception = e

    finally:
        # 安全地向队列写入结果
        _safe_queue_put(result_queue, (result, exception))


def _safe_queue_put(queue: Queue, item: Any) -> None:
    """安全地向队列写入数据"""
    try:
        queue.put(item)
    except (ValueError, OSError) as e:
        mylog.warning('无法向队列写入结果,队列可能已关闭: {}', e)
    except Exception as e:
        mylog.error('向队列写入结果时发生未知错误: {}', e)
    finally:
        with contextlib.suppress(Exception):
            queue.close()


class ProcessBase(Process):
    """增强型进程基类，提供结果获取、安全停止和资源清理功能

    Args:
        target: 进程执行的目标函数
        *args: 传递给目标函数的位置参数
        daemon: 是否为守护进程，默认为True
        **kwargs: 传递给目标函数的关键字参数，可包含callback回调函数
    """

    def __init__(self, target: Callable[..., Any], *args: Any, name: str | None = None, daemon: bool = True, **kwargs: Any):
        # 提取回调函数和进程名称
        self.callback = kwargs.pop('callback', None)
        process_name = name or target.__name__

        # 保存原始参数
        self._original_target = target
        self._original_args = args
        self._original_kwargs = kwargs

        # 初始化父类
        super().__init__(target=self._dummy_target, name=process_name, daemon=daemon)

        # 初始化状态变量
        self._is_running = False
        self._process_started = False
        self._stop_event = Event()
        self._result_queue: Queue | None = None

    def _dummy_target(self) -> None:
        """临时的目标函数，仅用于初始化"""
        pass

    def __enter__(self) -> ProcessBase:
        """上下文管理器入口 - 自动启动进程"""
        if not self._process_started:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """上下文管理器出口 - 自动停止进程"""
        if self.is_running():
            self.stop()
        return False  # 不抑制异常

    def start(self) -> None:
        """启动进程，确保进程只被启动一次"""
        if self._process_started:
            return

        self._result_queue = Queue()

        # 设置实际的target和参数
        self._target = _target_wrapper
        self._args = (self._original_target, self._original_args, self._original_kwargs, self.callback, self._stop_event, self._result_queue)
        self._kwargs = {}

        super().start()
        self._process_started = True
        self._is_running = True

    def get_result(self, timeout: float | None = None) -> Any:
        """获取进程执行结果

        Args:
            timeout: 等待进程完成的最大时间（秒），None表示无限等待

        Returns:
            进程执行的结果，如果超时或发生异常则返回None
        """
        if not self._process_started:
            raise RuntimeError("Cannot get result from a process that hasn't been started")

        try:
            # 等待进程完成
            self.join(timeout)
            if timeout and self.is_alive():
                mylog.warning('进程 {} 超时未完成', self.name)
                return None

            # 获取结果
            return self._retrieve_result()

        except Exception as e:
            mylog.error('获取进程结果失败: {}', e)
            return None
        finally:
            self._is_running = False

    def _retrieve_result(self) -> Any:
        """从队列中获取结果"""
        if self._result_queue is None:
            mylog.warning('进程 {} 没有返回结果', self.name)
            return None

        try:
            result, exception = self._result_queue.get(timeout=0.1)
            if exception:
                mylog.error('进程 {} 执行异常: {}', self.name, exception)
                return None
            return result

        except queue.Empty:
            mylog.warning('进程 {} 结果队列为空', self.name)
        except (EOFError, BrokenPipeError, OSError) as e:
            mylog.warning('队列通信错误: {}', e)

        return None

    def stop(self, timeout: float | None = None) -> bool:
        """安全停止进程

        Args:
            timeout: 等待进程停止的最大时间（秒），None表示无限等待

        Returns:
            进程是否成功停止
        """
        if not self._is_running:
            return True

        self._stop_event.set()
        self._is_running = False

        if timeout is not None:
            self.join(timeout)
            return not self.is_alive()

        self.join()
        return True

    def is_running(self) -> bool:
        """检查进程是否正在运行"""
        return self._is_running and self.is_alive()

    def __del__(self):
        """对象销毁时自动清理资源"""
        if hasattr(self, '_is_running') and self._is_running:
            with contextlib.suppress(Exception):
                self.stop(timeout=1.0)


class SafeProcess(ProcessBase):
    """安全进程类，提供异常捕获和重试机制"""

    def __init__(self, target: Callable, *args: Any, max_retries: int = 0, retry_delay: float = 1.0, name: str | None = None, daemon: bool = True, **kwargs: Any):
        process_name = name or target.__name__
        self.max_retries = max_retries
        self.retry_count = 0
        self.retry_delay = retry_delay

        super().__init__(target=self._safe_target_wrapper, daemon=daemon, name=process_name, original_target=target, original_args=args, original_kwargs=kwargs)

    def _safe_target_wrapper(self, original_target: Callable, original_args: tuple, original_kwargs: dict) -> Any:
        """安全目标函数包装器，实现重试逻辑"""
        assert self._result_queue is not None, '结果队列未初始化'

        for attempt in range(self.max_retries + 1):
            if self._stop_event.is_set():
                break

            try:
                result = original_target(*original_args, **original_kwargs)
                if callable(self.callback):
                    result = self.callback(result)
                return result

            except Exception as e:
                self.retry_count = attempt + 1
                if attempt < self.max_retries:
                    mylog.warning('安全进程 {} 第 {} 次重试: {}', self.name, self.retry_count, e)
                    self._stop_event.wait(self.retry_delay)
                else:
                    mylog.error('安全进程 {} 执行失败,已达最大重试次数: {}', self.name, e)
                    _safe_queue_put(self._result_queue, (None, e))
                    return None

        _safe_queue_put(self._result_queue, (None, None))
        return None


class ProcessManager(SingletonMixin):
    """进程管理器，用于管理所有进程实例

    采用单例模式，确保全局只有一个进程管理器实例

    主要功能：
    - 创建和启动新进程
    - 跟踪所有进程的状态
    - 提供安全的进程停止机制
    - 收集所有进程的执行结果
    """

    _lock = threading.RLock()
    _processes: ClassVar[dict[int, weakref.ref[ProcessBase]]] = {}

    def __init__(self):
        """初始化线程管理器"""
        super().__init__()

    @classmethod
    def create_process(cls, target: Callable, *args, **kwargs) -> ProcessBase:
        """创建并启动普通进程,自动添加到管理器

        Args:
            target: 进程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        Returns:
            ProcessBase: 创建的进程实例
        """
        process = ProcessBase(target, *args, **kwargs)

        with cls._lock:
            cls._processes[id(process)] = weakref.ref(process)

        process.start()
        return process

    @classmethod
    def create_safe_process(cls, target: Callable, *args, **kwargs) -> SafeProcess:
        """创建并启动安全进程,自动添加到管理器

        Args:
            target: 进程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数,可包含max_retries和retry_delay

        Returns:
            SafeProcess: 创建的安全进程实例
        """
        process = SafeProcess(target, *args, **kwargs)

        with cls._lock:
            cls._processes[id(process)] = weakref.ref(process)

        process.start()
        return process

    @classmethod
    def add_process(cls, process: ProcessBase) -> None:
        """将已存在的进程添加到管理器

        Args:
            process: 已创建的进程实例
        """
        with cls._lock:
            cls._processes[id(process)] = weakref.ref(process)

    @classmethod
    def stop_all(cls, timeout: float | None = None) -> None:
        """停止所有管理的进程

        Args:
            timeout: 等待进程停止的最大时间（秒）,None表示无限等待
        """
        try:
            with cls._lock:
                processes_to_stop = []
                for process_id, process_ref in list(cls._processes.items()):
                    process = process_ref()
                    if process is not None and process.is_running():
                        processes_to_stop.append(process)
                    else:
                        del cls._processes[process_id]

                for process in processes_to_stop:
                    process.stop(timeout)

                cls._processes.clear()
        except Exception as e:
            mylog.error('停止所有进程失败: {}', e)
            raise  # 重新抛出异常，让调用者知道操作失败

    @classmethod
    def wait_all_completed(cls, timeout: float | None = None) -> dict[int, Any]:
        """等待所有进程完成并返回结果

        Args:
            timeout: 等待进程完成的最大时间（秒）,None表示无限等待

        Returns:
            dict[int, Any]: 进程ID到执行结果的映射
        """
        tmp_all_results = {}

        with cls._lock:
            for process_id, process_ref in list(cls._processes.items()):
                try:
                    process = process_ref()
                    if process is not None:
                        result = process.get_result(timeout)
                        tmp_all_results[process_id] = result
                    else:
                        del cls._processes[process_id]
                except Exception as e:
                    mylog.error('获取进程结果失败: {}', e)
                    tmp_all_results[process_id] = None

        with cls._lock:
            cls._processes.clear()

        return tmp_all_results

    @classmethod
    def get_active_count(cls) -> int:
        """获取当前活动的进程数量

        Returns:
            int: 当前活动的进程数量
        """
        with cls._lock:
            # 清理已经结束的进程引用
            active_count = 0
            for process_id, process_ref in list(cls._processes.items()):
                process = process_ref()
                if process is not None and process.is_running():
                    active_count += 1
                else:
                    del cls._processes[process_id]
            return active_count

    @classmethod
    def get_process_by_id(cls, process_id: int) -> ProcessBase | None:
        """根据ID获取进程实例

        Args:
            process_id: 进程ID

        Returns:
            ProcessBase | None: 对应的进程实例，如果不存在则返回None
        """
        with cls._lock:
            process_ref = cls._processes.get(process_id)
            return process_ref() if process_ref else None

    @classmethod
    def get_process_by_name(cls, name: str) -> list[ProcessBase]:
        """根据名称获取进程实例列表

        Args:
            name: 进程名称

        Returns:
            list[ProcessBase]: 名称匹配的进程实例列表
        """
        result = []
        with cls._lock:
            for process_ref in cls._processes.values():
                process = process_ref()
                if process and process.name == name:
                    result.append(process)
        return result

    @classmethod
    def stop_process(cls, process_id: int, timeout: float | None = None) -> bool:
        """停止指定进程

        Args:
            process_id: 进程ID
            timeout: 等待进程停止的最大时间（秒），None表示无限等待

        Returns:
            bool: 进程是否成功停止
        """
        process = cls.get_process_by_id(process_id)
        if process and process.is_running():
            return process.stop(timeout)
        return False


class CustomProcess(ProcessBase):
    """自定义进程类,扩展ProcessBase,支持任务分片和结果收集

    用于在多进程环境中并行处理一系列任务,并将结果收集到共享字典中

    Args:
        *args: 位置参数列表,每个参数应为等长的列表,包含每个任务的参数
        result_dict: 共享字典,用于存储任务结果
        semaphore: 信号量,用于控制并发进程数量
        func: 要执行的目标函数
        start_idx: 任务起始索引
        end_idx: 任务结束索引（不包含）
        **kwargs: 传递给目标函数的关键字参数

    Example:
        >>> from multiprocessing import Manager, Semaphore
        >>> with Manager() as manager:
        >>>     result_dict = manager.dict()
        >>>     semaphore = Semaphore(4)  # 限制4个并发进程
        >>> # 创建进程处理索引0-10的任务
        >>>     process = CustomProcess([[1,2,3]], result_dict=result_dict,
        >>>                            semaphore=semaphore, func=lambda x: x*2,
        >>>                            start_idx=0, end_idx=3)
        >>>     process.join()  # 等待进程完成
        >>>     print(result_dict)  # 输出: {0: 2, 1: 4, 2: 6}
    """

    _context = get_context('spawn')  # 显式使用spawn上下文,提高跨平台兼容性
    all_processes: ClassVar[list[CustomProcess]] = []  # 跟踪所有创建的进程

    def __init__(self, *args: Any, result_dict: Any, semaphore: Any, func: Callable[..., Any], start_idx: int, end_idx: int, name: str | None = None, daemon: bool = True, **kwargs: Any):
        """
        初始化自定义进程

        Args:
            *args: 位置参数列表,每个参数应为等长的列表,包含每个任务的参数
            result_dict: 共享字典,用于存储任务结果
            semaphore: 信号量,用于控制并发进程数量
            func: 要执行的目标函数
            start_idx: 任务起始索引
            end_idx: 任务结束索引（不包含）
            name: 进程名称,默认使用目标函数名
            daemon: 是否设为守护进程,默认True
            **kwargs: 传递给目标函数的关键字参数
        """
        # 正确调用ProcessBase的初始化
        # 这里我们不使用原始的target参数，而是在自定义的run方法中实现逻辑
        process_name = name or func.__name__
        super().__init__(target=self._custom_run, name=process_name, daemon=daemon)

        # 保存自定义参数
        self.result_dict = result_dict
        self.semaphore = semaphore
        self.func = func
        self.args = args
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.kwargs = kwargs  # 单独保存函数关键字参数

        # 初始化ProcessBase中定义的属性
        self._is_running = False
        self._result = None
        self._exception = None
        self._stop_event = Event()
        self._process_started = False

        # 添加到进程跟踪列表
        CustomProcess.all_processes.append(self)

        # 自动启动进程
        self.start()

    def _custom_run(self):
        """内部运行函数，被ProcessBase调用"""
        pass  # 实际逻辑在下面的run方法中实现

    @safe_call()
    def run(self) -> None:
        """
        进程执行入口,处理指定范围内的任务

        获取信号量后,遍历指定索引范围内的所有任务,执行目标函数并收集结果
        异常情况下会将错误信息存入结果字典
        """
        self._is_running = True
        with self.semaphore:
            for idx in range(self.start_idx, self.end_idx):
                if self._stop_event.is_set():
                    break
                    
                self._process_single_index(idx)
        self._is_running = False

    def _process_single_index(self, idx: int) -> None:
        """
        处理单个索引的任务
        
        Args:
            idx: 当前处理的索引
        """
        try:
            # 准备参数并执行函数
            args = self._get_args_for_index(idx)
            result = self.func(*args, **self.kwargs)
            self.result_dict[idx] = result
            
        except Exception as e:
            error_msg = f'CustomProcess Error | index {idx} | {self.name} | {type(e).__name__}({e})'
            self.result_dict[idx] = error_msg
            mylog.error(error_msg)

    def _get_args_for_index(self, idx: int) -> list:
        """
        获取指定索引对应的参数
        
        Args:
            idx: 索引
            
        Returns:
            list: 参数列表
        """
        if not self.args:
            return []
        
        return [
            arg[idx] if isinstance(arg, (list, tuple)) and len(arg) > idx else arg
            for arg in self.args
        ]

    @classmethod
    def wait_completed(cls) -> None:
        """
        等待所有已创建的进程完成执行

        复制当前进程列表,清空原始列表,然后等待所有进程完成
        """
        processes = cls.all_processes.copy()
        cls.all_processes.clear()
        for process in processes:
            process.join()  # 等待进程完成


process_manager = ProcessManager()


def run_custom_process(func: Callable[..., Any], *args: Any, **kwargs: Any) -> list[Any]:
    """
    高级并行处理函数,简化多进程任务分发和结果汇总

    自动将任务分片并分配给多个进程执行,最后按照原始顺序返回所有结果

    Args:
        func: 要并行执行的目标函数
        *args: 每个参数应为等长的列表,包含每个任务的参数
        **kwargs: 传递给目标函数的关键字参数,其中max_workers用于控制最大进程数

    Returns:
        list: 按照原始顺序排列的任务结果列表

    Raises:
        ValueError: 当输入参数列表长度不一致时抛出

    Example:
        >>> def square(x):
        >>>     return x * x
        >>> # 并行计算多个数的平方
        >>> results = run_custom_process(square, [1, 2, 3, 4, 5], max_workers=3)
        >>> print(results)  # 输出: [1, 4, 9, 16, 25]

        >>> # 多参数示例
        >>> def add(x, y):
        >>>     return x + y
        >>> results = run_custom_process(add, [1, 2, 3], [4, 5, 6])
        >>> print(results)  # 输出: [5, 7, 9]
    """
    # Windows平台特殊处理,确保函数可以在子进程中被正确序列化
    if sys.platform == 'win32':
        import __main__

        func_name = getattr(func, '__name__', str(id(func)))
        __main__.__dict__[func_name] = func

    # 获取最大进程数,默认为12
    max_workers = kwargs.pop('max_workers', 12)

    # 参数校验：确保所有参数列表长度一致
    if not args:
        raise ValueError('至少需要提供一个参数列表')

    base_length = len(args[0])
    for i, arg in enumerate(args[1:], 2):
        if len(arg) != base_length:
            raise ValueError(f'第{i}个参数列表长度与第一个参数列表长度不一致')

    with Manager() as manager:
        # 创建共享字典存储结果
        result_dict = manager.dict()
        # 创建信号量控制最大并发进程数
        global_semaphore = Semaphore(max_workers)

        # 计算任务总数和每个进程处理的任务数
        total_tasks = base_length
        chunk_size = max(1, total_tasks // max_workers)
        # 生成分片索引
        chunks = [(i, min(i + chunk_size, total_tasks)) for i in range(0, total_tasks, chunk_size)]

        # 创建并启动进程处理每个分片
        for start_idx, end_idx in chunks:
            CustomProcess(
                *args,
                result_dict=result_dict,
                semaphore=global_semaphore,
                func=func,
                start_idx=start_idx,
                end_idx=end_idx,
                **kwargs,  # 传递函数关键字参数
            )

        # 等待所有进程完成
        CustomProcess.wait_completed()

        # 按照原始顺序收集并返回结果
        return [result_dict[i] for i in range(total_tasks)]


__all__ = ['CustomProcess', 'ProcessBase', 'ProcessManager', 'SafeProcess', 'process_manager', 'run_custom_process']
