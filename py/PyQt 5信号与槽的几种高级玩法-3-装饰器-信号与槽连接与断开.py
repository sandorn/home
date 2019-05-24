# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
PyQt 5信号与槽的几种高级玩法 - 博文视点（北京）官方博客 - CSDN博客
https://blog.csdn.net/broadview2006/article/details/80132757
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 19:42:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 20:02:26
'''
from PyQt5.QtCore import QObject, pyqtSignal


class SignalClass(QObject):

     # 声明无参数的信号
    signal1 = pyqtSignal()

    # 声明带一个int类型参数的信号
    signal2 = pyqtSignal(int)

    def __init__(self, parent=None):
        super(SignalClass, self).__init__(parent)

        # 将信号signal1连接到sin1Call和sin2Call这两个槽函数
        self.signal1.connect(self.sin1Call)
        self.signal1.connect(self.sin2Call)

        # 将信号signal2连接到信号signal1
        self.signal2.connect(self.signal1)

        # 发射信号
        self.signal1.emit()
        self.signal2.emit(1)

        # 断开signal1、signal2信号与各槽函数的连接
        self.signal1.disconnect(self.sin1Call)
        self.signal1.disconnect(self.sin2Call)
        self.signal2.disconnect(self.signal1)

        # 将信号signal1和signal2连接到同一个槽函数sin1Call
        self.signal1.connect(self.sin1Call)
        self.signal2.connect(self.sin1Call)

        # 再次发射信号
        self.signal1.emit()
        self.signal2.emit(1)

    def sin1Call(self):
        print("signal-1 emit")

    def sin2Call(self):
        print("signal-2 emit")


if __name__ == '__main__':
    signal = SignalClass()
