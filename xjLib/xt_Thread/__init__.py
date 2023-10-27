# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 23:33:24
FilePath     : /CODE/xjLib/xt_Thread/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
'''
from .futures import FuncInThreadPool, ProcessPool, ThreadPool
from .manage import WorkManager, thread_pool
from .Process import CustomProcess, Do_CustomProcess
from .Singleon import (
    Singleton_Meta,
    Singleton_Mixin,
    singleton_wrap,
    singleton_wrap_class,
    singleton_wrap_return_class,
)
from .thread import (
    CustomThread,
    CustomThread_Queue,
    SigThread,
    SigThreadQ,
    SingletonThread,
    stop_thread,
)
from .wraps import (
    QThread_wrap,
    Thread_wrap,
    Thread_wrap_class,
    create_mixin_class,
    run_in_threadpool,
    thread_print,
    thread_safe,
)
