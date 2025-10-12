# !/usr/bin/env python
"""
==============================================================
Description  : 线程与进程管理增强包 - 提供全面的并发编程解决方案
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-09-07 10:00:00
Github       : https://github.com/sandorn/nsthread

xt_thread包提供了全面的并发编程工具，包括线程管理、进程管理、生产者-消费者模式以及PyQt线程支持。

核心功能模块:
- 线程基础工具(thread.py): 提供线程安全装饰器、基础线程类、线程管理器等
- 线程池(futures.py): 实现多种线程池，支持异步任务处理和结果收集
- 多进程(process.py): 提供进程池管理和并行任务处理能力
- 生产者-消费者模式(production.py): 实现同步和异步版本的任务处理框架
- PyQt线程(qThread.py): 提供PyQt6相关的线程增强功能

使用场景:
- 简单并发任务: 使用ThreadBase或SafeThread
- 批量任务处理: 使用BaseThreadPool或EnhancedThreadPool
- 动态资源管理: 使用DynamicThreadPool或ThreadPoolManager
- 跨进程并行: 使用CustomProcess或run_custom_process
- UI响应式应用: 使用QtThreadBase或QtSafeThread
- 复杂任务流: 使用Production或AsyncProduction
==============================================================
"""

from __future__ import annotations

from .exception import handle_exception, safe_call
from .futures import AsyncThreadPool, BaseThreadRunner, DynamicThreadRunner, EnhancedThreadPool, FutureThreadPool, ThreadPoolManager
from .process import CustomProcess, ProcessBase, ProcessManager, SafeProcess, process_manager, run_custom_process
from .production import AsyncProduction, Production
from .qthread import ComposedSingletonQtThread, QtSafeThread, QtThreadBase, QtThreadManager, SingletonQtThread
from .thread import ComposedSingletonThread, SafeThread, SingletonThread, ThreadBase, ThreadManager
from .wraps import ThreadWrapsManager, parallelize_wraps, qthread_wraps, run_in_qtthread, run_in_thread, thread_print, thread_safe, thread_wraps

__all__ = (
    'AsyncThreadPool',
    'BaseThreadRunner',
    'ComposedSingletonQtThread',
    'ComposedSingletonThread',
    'CustomProcess',
    'DynamicThreadRunner',
    'EnhancedThreadPool',
    'FutureThreadPool',
    'ProcessBase',
    'ProcessManager',
    'Production',
    'QtSafeThread',
    'QtThreadBase',
    'QtThreadManager',
    'SafeProcess',
    'SafeThread',
    'SingletonQtThread',
    'SingletonThread',
    'ThreadBase',
    'ThreadManager',
    'ThreadPoolManager',
    'ThreadWrapsManager',
    'handle_exception',
    'parallelize_wraps',
    'process_manager',
    'qthread_wraps',
    'run_custom_process',
    'run_in_qtthread',
    'run_in_thread',
    'safe_call',
    'thread_print',
    'thread_safe',
    'thread_wraps',
)


__version__ = '0.0.7'
