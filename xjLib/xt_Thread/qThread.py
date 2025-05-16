# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-05-16 10:00:49
FilePath     : /CODE/xjLib/xt_thread/qThread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6.QtCore import QThread, pyqtSignal
from xt_singleon import singleton_decorator_factory


class CustomQThread(QThread):
    """多线程,继承自QThread"""

    all_QThread = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用
    finished = pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self._isRunning = True
        self.finished.connect(self.on_finished)  # 连接信号到槽函数
        self._target = func
        self._args = args
        self._kwargs = kwargs
        self.all_QThread.append(self)
        self.start()

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.result_list.append(self.Result)
        self.finished.emit()  # 线程任务完成后发射信号

    def stop(self):
        if self._isRunning:
            self._isRunning = False
            self.quit()  # 改用安全退出方式
            self.wait(1000)  # 等待1秒线程结束
        # self.terminate()  # 线程终止

    @classmethod
    def result(cls):
        """获取所有线程"""
        return cls.getResult()

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
        """停止线程池，安全版本"""
        while cls.all_QThread:
            _thread = cls.all_QThread.pop()
            _thread.stop()  # 显式调用stop方法


    @classmethod
    def wait_completed(cls):
        """等待全部线程结束,返回结果"""
        try:
            cls.stop_all()
            res = cls.result_list  # 获取结果列表
            cls.result_list = []  # 清空结果列表
            return res
        except Exception:
            return None
        
    getAllResult = wait_completed  # 别名

    def on_finished(self):
        """线程完成时的回调函数"""
        print(f"Thread {self._target.__name__} finished with result: {self.Result}")
        return self.result

SingletonQThread = singleton_decorator_factory(CustomQThread)


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)


    def fn(*args):
        return sum(args)

    a = CustomQThread(fn, 4, 5, 6)
    b = CustomQThread(fn, 7, 8, 9)
    c = SingletonQThread(fn, 10, 11, 12)
    d = SingletonQThread(fn, 13, 14, 15,reinit=True)

    # 保证主线程不退出，等待线程完成
    sys.exit(app.exec())
