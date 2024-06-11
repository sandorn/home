# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-11 10:15:15
FilePath     : /CODE/xjLib/xt_Thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import QThread
from xt_Thread import Singleton_Mixin, create_mixin_class, singleton_wrap_class


class CustomQThread(QThread):
    """多线程,继承自QThread"""

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._target = func
        self._isRunning = True
        self._args = args
        self._kwargs = kwargs
        self.start()

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)

    def __del__(self):
        # 线程状态改变与线程终止
        self.wait()  # 等待线程执行完毕
        self.stop()

    def stop(self):
        self._isRunning = False
        self.terminate()  # 线程终止

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.wait()
            return self.Result
        except Exception:
            return None

    def join(self):
        """等待线程执行完毕"""
        self.wait()


@singleton_wrap_class
class QThread_wrap_class(CustomQThread): ...


class QThread_Singleton_Mixin(Singleton_Mixin, CustomQThread): ...


SingletonQThread = create_mixin_class(
    "SingletonQThread", Singleton_Mixin, CustomQThread
)

if __name__ == "__main__":

    def f(*args):
        return sum(args)

    a = SingletonQThread(f, 4, 5, 6)
    print(a.getResult())
    b = SingletonQThread(f, 7, 8, 9)
    print(a is b, b.getResult())
