# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-28 20:41:05
#LastEditTime : 2020-05-28 21:02:53
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()

        self.button = QPushButton('开始', self)
        self.button.clicked.connect(self.count_func)  ##按钮绑定函数
        self.button_2 = QPushButton('停止', self)
        self.button_2.clicked.connect(self.stop_count_func)  #%按钮绑定函数

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.my_thread = MyThread()  #实例化线程对象
        self.my_thread.my_signal.connect(self.set_label_func)
        # @线程自定义信号连接的槽函数

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button_2)
        self.v_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def stop_count_func(self):
        self.my_thread.is_on = False  #%结束线程
        self.my_thread.count = 0

    def count_func(self):
        self.my_thread.is_on = True
        self.my_thread.start()  ##启动线程

    def set_label_func(self, num):
        self.label.setText(num)
        # @接收MyThread发送来的自定义信号


class MyThread(QThread):  #线程类
    my_signal = pyqtSignal(str)  #自定义信号对象。参数str就代表这个信号可以传一个字符串

    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0
        self.is_on = True

    def run(self):  #线程执行函数
        while self.is_on:
            print(self.count)
            self.count += 1
            self.my_signal.emit(str(self.count))
            # @发送自定义信号

            self.sleep(1)  #本线程睡眠n秒【是QThread函数】


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
