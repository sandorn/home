# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:53
LastEditTime : 2022-12-11 23:15:24
FilePath     : /xjLib/xt_Thread/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
'''
__doc__ = [
    'SingletonThread',  # 单例
    'SingletonThread_Queue',
    'CustomThread',  # 继承线程
    'Custom_Thread_Queue',
    'NoResultsPending',  # 任务均已处理
    'NoWorkersAvailable',  # 无工作线程可用
    'WorkManager',  # 线程池管理，参照htreadpool编写的自定义库
    'Work',  # 线程池任务结构，参照htreadpool编写的自定义库
    'thread_pool',  # 线程装饰器
    'WorkThread',  # 继承线程,利用queue；参照htreadpool编写的自定义库
    'my_pool',  # 装饰符方式
    'stop_thread',  # 外部停止线程
    'thread_wrap',  # 线程装饰器
    'thread_wraps',  # 线程装饰器,带参数
    'thread_wrap_class',  # 线程装饰器,获取结果
    'thread_wraps_class',  # 线程装饰器,带参数,获取结果
    'thread_safe',  # 线程安全锁，需要提供lock
]

# #引入自定义thread
from .Custom import (
    CustomThread,
    CustomThread_Queue,
    CustomThread_Queue_Singleton,
    CustomThread_Singleton,
    SigThread,
    SigThreadQ,
    SingletonThread,
    stop_thread,
)
from .futures import P_Map, P_Sub, ProcessPool, T_Map, T_Sub, ThreadPool

# #引入自定义thread pool
from .manage import WorkManager, thread_pool

# #引入装饰器
from .wraps import thread_safe, thread_wrap, thread_wrap_class
