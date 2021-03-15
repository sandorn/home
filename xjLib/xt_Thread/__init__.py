# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-03-02 09:07:36
FilePath     : /xjLib/xt_Thread/__init__.py
LastEditTime : 2021-01-04 14:14:07
#Github       : https://github.com/sandorn/home
#==============================================================
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
from .Custom import stop_thread, CustomThread, CustomThread_Queue, SingletonThread, SigThread, SigThreadQ, CustomThread_Singleton, CustomThread_Queue_Singleton
# #引入装饰器
from .wraps import thread_wrap_class, thread_wrap, thread_safe
# #引入自定义thread pool
from .manage import WorkManager, thread_pool

from .futures import T_Map, T_Sub, T_Pool, P_Map, P_Sub, P_Pool
