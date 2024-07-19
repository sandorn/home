# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 11:34:22
FilePath     : /CODE/xjLib/xt_thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import QThread
from xt_singleon import SingletonDecoratorClass, SingletonMixin
from xt_thread import create_mixin_class


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


@SingletonDecoratorClass
class QThread_wrap_class(CustomQThread): ...


class QThread_Singleton_Mixin(SingletonMixin, CustomQThread): ...


SingletonQThread = create_mixin_class("SingletonQThread", SingletonMixin, CustomQThread)

if __name__ == "__main__":

    def f(*args):
        return sum(args)

    a = SingletonQThread(f, 4, 5, 6)
    print(a.getResult())
    b = SingletonQThread(f, 7, 8, 9)
    print(a is b, b.getResult())
