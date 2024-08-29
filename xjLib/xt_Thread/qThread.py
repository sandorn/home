# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-26 15:33:16
FilePath     : /CODE/xjLib/xt_thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import QThread, pyqtSignal
from xt_singleon import SingletonMixin


class CustomQThread(QThread):
    """多线程,继承自QThread"""

    all_QThread = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用
    finished = pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._isRunning = True
        # self.finished.connect(self.on_finished)  # 连接信号到槽函数
        self._target = func
        self._args = args
        self._kwargs = kwargs
        self.all_QThread.append(self)
        self.start()

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)

    def __del__(self):
        # 线程状态改变与线程终止
        self.join()  # 等待线程执行完毕
        self.stop()

    def stop(self):
        self._isRunning = False
        self.terminate()  # 线程终止

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.join()
            return self.Result
        except Exception:
            return None

    def join(self):
        """等待线程执行完毕"""
        self.wait()

    @classmethod
    def stop_all(cls):
        """停止线程池, 所有线程停止工作"""
        while cls.all_QThread:
            _thread = cls.all_QThread.pop()
            _thread.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        try:
            cls.stop_all()
            res, cls.result_list = cls.result_list, []
            return res
        except Exception:
            return None

    @classmethod
    def getAllResult(cls):
        """利用enumerate,根据类名判断线程结束,返回结果"""
        cls.wait_completed()


class SingletonQThread(SingletonMixin, CustomQThread): ...


if __name__ == "__main__":

    def fn(*args):
        return sum(args)

    a = SingletonQThread(fn, 4, 5, 6)
    print(a.getResult())
    b = SingletonQThread(fn, 7, 8, 9)
    print(a is b, b.wait_completed(), b.getResult())
