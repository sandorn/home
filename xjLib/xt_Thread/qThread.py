# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-24 23:51:15
FilePath     : /xjLib/xt_Thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from threading import Lock

from PyQt5.QtCore import QThread
from xt_Class import repr_Mixin


class CustomQThread(QThread, repr_Mixin):
    """单例多线程,继承自threading.Thread"""

    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

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


if __name__ == "__main__":

    def f(*args):
        print(*args)

    import sys

    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    a = CustomQThread(f, 4)
    print(111111111111, a)
    b = CustomQThread(f, 6)
    print(a is b, id(a), id(b), a, b)

    nowthread = QThread()
    nowthread.run = f
    nowthread.run(7, 8, 9)
    sys.exit(app.exec_())
