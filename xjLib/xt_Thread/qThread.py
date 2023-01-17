# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-17 23:59:15
FilePath     : /CODE/xjLib/xt_Thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from PyQt5.QtCore import QThread
from xt_Thread import Singleton_Mixin, create_mixin_class, singleton_wrap_class


class CustomQThread(QThread):
    """多线程,继承自QThread"""

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._target = func
        self._args = args
        self._kwargs = kwargs
        self._running = True
        self.start()

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)

    def __del__(self):
        # 线程状态改变与线程终止
        self._running = False
        self.wait()  # 等待线程执行完毕

    def stop(self):
        self._running = False
        self.terminate()  # 线程终止

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.wait()
            return self.Result
        except Exception:
            return None

    def join(self):
        '''等待线程执行完毕'''
        self.wait()


@singleton_wrap_class
class QThread_wrap_class(CustomQThread):
    ...


class QThread_Singleton_Mixin(Singleton_Mixin, CustomQThread):
    ...


SingletonQThread = create_mixin_class('SingletonQThread', Singleton_Mixin, CustomQThread)

if __name__ == "__main__":

    def f(*args):
        print(*args)

    import sys

    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    a = SingletonQThread(f, 4)
    print(111111111111, a)
    b = SingletonQThread(f, 6)
    print(a is b, id(a), id(b), a, b)

    sys.exit(app.exec_())
