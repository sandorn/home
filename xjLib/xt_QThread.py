# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-28 21:06:12
#LastEditTime : 2020-07-13 12:30:53
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from threading import Lock
from PyQt5.QtCore import QThread


class CustomQThread(QThread):
    """单例多线程，继承自threading.Thread"""

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
        self.result_list = []
        self.start()

    def run(self):
        # 调用线程函数，并将元组类型的参数值分解为单个的参数值传入线程函数
        self.Result = self._target(*self._args, **self._kwargs)
        # 获取结果
        self.result_list.append(self.Result)

    def __del__(self):
        # 线程状态改变与线程终止
        self._running = False
        self.wait()  # # 线程不退出

    def stop(self):
        self._running = False
        self.terminate()  # #强制结束线程
        # # quit()  exit() 均无效


if __name__ == "__main__":

    def f(*args):
        print(*args)

    from PyQt5 import QtWidgets
    import sys
    app = QtWidgets.QApplication(sys.argv)

    a = CustomQThread(f, 4)
    b = CustomQThread(f, 6)
    print(a is b, id(a), id(b), a, b)

    nowthread = QThread()
    nowthread.run = f
    nowthread.run(1, 2, 3)
    sys.exit(app.exec_())
