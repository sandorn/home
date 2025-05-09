# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-29 11:40:57
FilePath     : /CODE/xjLib/xt_thread/thread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import ctypes
import inspect
from threading import Thread
from time import sleep

from xt_singleon import SingletonMixin


class ThreadBase(Thread):
    def __init__(self, target, *args, **kwargs):
        super().__init__(target=target,name=target.__name__, args=args, kwargs=kwargs)
        self._isRunning = True
        self.Result = None
    def getResult(self):
        try:
            self.join()
            return self.Result
        except Exception as e:
            print(f"获取线程结果失败: {e}")
            return None

    def stop(self):
        if self._isRunning:
            self._isRunning = False
            print(f"线程 {self.name} 已停止")

    def __del__(self):
        # 线程状态改变与线程终止
        if self._isRunning:
            self.stop()
        self.join()
        print(f"线程 {self.name} 资源已清理")

    def run(self):
        try:
            self.Result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            print(f"线程执行失败: {e}")
            self.Result = None


class ThreadManager:
    all_Thread = []
    result_list = []

    @classmethod
    def stop_all(cls):
        while cls.all_Thread:
            _thread = cls.all_Thread.pop()
            _thread.join()

    @classmethod
    def wait_completed(cls):
        try:
            cls.stop_all()
            res, cls.result_list = cls.result_list, []
            return res
        except Exception as e:
            print(f"线程等待失败: {e}")
            return None


def stop_thread(thread):
    """外部停止线程"""

    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    _async_raise(thread.ident, SystemExit)

class CustomThread(ThreadBase):
    def __init__(self, target, *args, **kwargs):
        super().__init__(target, *args, **kwargs)
        ThreadManager.all_Thread.append(self)
        self.start()

class SigThread(SingletonMixin, CustomThread): ...

if __name__ == "__main__":

    def func(*arg, **kwargs):
        # thread_print(*arg, **kwargs)
        sleep(0.2)
        return arg

    def func2(*arg, **kwargs):
        # thread_print(*arg, **kwargs)
        sleep(0.2)
        return arg

    a = CustomThread(func, 111111111111111)
    print(22222222222,a.name, a.getResult(), type(a))

    b = SigThread(func2, 2, 3)
    print(33333333333, b.name, b.getResult(),type(b))

    c = SigThread(func, 6666666666666)
    print(66666666666, c.name, c.getResult(), type(c))