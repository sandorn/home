# !/usr/bin/env python
"""
==============================================================
Description  : 进程池管理模块 - 提供高效的并行任务处理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 11:36:53
LastEditTime : 2025-09-06 20:00:00
FilePath     : /CODE/xjLib/xt_thread/process.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- CustomProcess：自定义进程类，支持任务分片和结果收集
- Do_CustomProcess：高级并行处理函数，简化多进程任务分发和结果汇总

主要特性：
- 基于Python内置multiprocessing模块，提供更易用的接口
- 支持任务分片处理，提高多核CPU利用率
- 统一的结果收集机制，保持任务执行顺序
- 完整的异常捕获和处理，确保程序稳定性
- 进程数量控制，避免资源耗尽
- 适用于IO密集型和CPU密集型任务

## 基本判断
process.py 库可以用于爬虫，但更适合作为爬虫框架中的并发处理组件，而非完整的爬虫解决方案。
## 优势与适用场景
1. 1.多进程并行能力 ：通过 run_custom_process 函数可以轻松实现URL列表的并行爬取，充分利用多核CPU
2. 2.任务分片处理 ：自动将大量URL任务分片，提高处理效率
3. 3.统一结果收集 ：按原始顺序收集爬取结果，方便后续数据处理
4. 4.异常隔离处理 ：单个爬取任务失败不会影响整个进程，增强稳定性
5. 5.跨平台兼容性 ：显式使用 spawn 上下文，特别是针对Windows平台做了优化
6. 6.资源控制 ：通过 max_workers 参数可限制最大进程数，避免资源耗尽
## 局限性
1. 1.无网络IO优化 ：不包含请求重试、超时控制、代理池等爬虫常用功能
2. 2.不支持异步IO ：纯多进程模型，对于高IO密集型爬虫（如大量小请求）效率可能不如异步IO
3. 3.缺少爬虫特有功能 ：不提供自动限速、请求头管理、Cookie处理等爬虫专用功能
4. 4.序列化限制 ：在Windows平台下对函数有序列化要求，嵌套函数无法直接使用
## 使用建议
如果要用此库进行爬虫开发，建议：
1. 1.将其作为底层并发组件，结合 requests 或 httpx 等HTTP库使用
2. 2.为爬虫函数添加错误重试、超时控制等功能
3. 3.针对大量小请求的场景，可考虑搭配异步IO库使用
4. 4.对于简单的批量数据爬取任务，此库可以快速实现并发处理
总结： process.py 是一个优秀的并行处理库，可以作为爬虫开发中的并发组件，但需要结合其他库或自行实现爬虫特有的功能来构建完整的爬虫解决方案。
==============================================================
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from multiprocessing import Manager, Process, Semaphore, get_context
from typing import Any, ClassVar, TypeVar

T = TypeVar('T')  # 输入参数类型
R = TypeVar('R')  # 返回结果类型


class CustomProcess(Process):
    """
    自定义进程类，扩展标准Process，支持任务分片和结果收集
    
    用于在多进程环境中并行处理一系列任务，并将结果收集到共享字典中
    
    Args:
        *args: 位置参数列表，每个参数应为等长的列表，包含每个任务的参数
        result_dict: 共享字典，用于存储任务结果
        semaphore: 信号量，用于控制并发进程数量
        func: 要执行的目标函数
        start_idx: 任务起始索引
        end_idx: 任务结束索引（不包含）
        **kwargs: 传递给目标函数的关键字参数
        
    Example:
        >>> from multiprocessing import Manager, Semaphore
        >>> with Manager() as manager:
        >>>     result_dict = manager.dict()
        >>>     semaphore = Semaphore(4)  # 限制4个并发进程
        >>>     # 创建进程处理索引0-10的任务
        >>>     process = CustomProcess([[1,2,3]], result_dict=result_dict, 
        >>>                            semaphore=semaphore, func=lambda x: x*2, 
        >>>                            start_idx=0, end_idx=3)
        >>>     process.join()  # 等待进程完成
        >>>     print(result_dict)  # 输出: {0: 2, 1: 4, 2: 6}
    """
    
    _context = get_context('spawn')  # 显式使用spawn上下文，提高跨平台兼容性
    all_processes: ClassVar[list[CustomProcess]] = []  # 跟踪所有创建的进程

    def __init__(
        self,
        *args: list[list[Any]],
        result_dict: dict[int, Any],
        semaphore: Semaphore,
        func: Callable[..., Any],
        start_idx: int,
        end_idx: int,
        **kwargs,
    ):
        """
        初始化自定义进程
        
        Args:
            *args: 位置参数列表，每个参数应为等长的列表，包含每个任务的参数
            result_dict: 共享字典，用于存储任务结果
            semaphore: 信号量，用于控制并发进程数量
            func: 要执行的目标函数
            start_idx: 任务起始索引
            end_idx: 任务结束索引（不包含）
            **kwargs: 传递给目标函数的关键字参数
        """
        super().__init__()
        self.result_dict = result_dict 
        self.semaphore = semaphore
        self.func = func
        self.args = args
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.kwargs = kwargs  # 单独保存函数关键字参数
        self.daemon = True  # 设为守护进程，主进程结束时自动终止
        CustomProcess.all_processes.append(self)
        self.start()  # 自动启动进程

    def run(self) -> None:
        """
        进程执行入口，处理指定范围内的任务
        
        获取信号量后，遍历指定索引范围内的所有任务，执行目标函数并收集结果
        异常情况下会将错误信息存入结果字典
        """
        with self.semaphore:
            for idx in range(self.start_idx, self.end_idx):
                try:
                    # 为当前索引准备参数
                    args_for_idx = [arg[idx] for arg in self.args]
                    # 执行目标函数并获取结果
                    result = self.func(*args_for_idx, **self.kwargs) 
                    # 存储结果
                    self.result_dict[idx] = result
                except Exception as e:
                    # 异常处理，将错误信息存入结果字典
                    self.result_dict[idx] = f'Error processing index {idx}: {e!s}'

    @classmethod
    def wait_completed(cls) -> None:
        """
        等待所有已创建的进程完成执行
        
        复制当前进程列表，清空原始列表，然后等待所有进程完成
        """
        processes = cls.all_processes.copy()
        cls.all_processes.clear()
        for process in processes:
            process.join()  # 等待进程完成


def run_custom_process[T, R](func: Callable[..., R], *args: list[T], **kwargs) -> list[R]:
    """
    高级并行处理函数，简化多进程任务分发和结果汇总
    
    自动将任务分片并分配给多个进程执行，最后按照原始顺序返回所有结果
    
    Args:
        func: 要并行执行的目标函数
        *args: 每个参数应为等长的列表，包含每个任务的参数
        **kwargs: 传递给目标函数的关键字参数，其中max_workers用于控制最大进程数
        
    Returns:
        List: 按照原始顺序排列的任务结果列表
        
    Raises:
        ValueError: 当输入参数列表长度不一致时抛出
        
    Example:
        >>> def square(x):
        >>>     return x * x
        >>> 
        >>> # 并行计算多个数的平方
        >>> results = Do_CustomProcess(square, [1, 2, 3, 4, 5], max_workers=3)
        >>> print(results)  # 输出: [1, 4, 9, 16, 25]
        
        >>> # 多参数示例
        >>> def add(x, y):
        >>>     return x + y
        >>> 
        >>> results = Do_CustomProcess(add, [1, 2, 3], [4, 5, 6])
        >>> print(results)  # 输出: [5, 7, 9]
    """
    # Windows平台特殊处理，确保函数可以在子进程中被正确序列化
    if sys.platform == 'win32':
        import __main__
        func_name = getattr(func, '__name__', str(id(func)))
        __main__.__dict__[func_name] = func

    # 获取最大进程数，默认为12
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
        chunks = [
            (i, min(i + chunk_size, total_tasks))
            for i in range(0, total_tasks, chunk_size)
        ]

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


# 测试示例请参考：/CODE/项目包/ProessPool-8星.py
