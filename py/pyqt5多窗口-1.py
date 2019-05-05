# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   webkit嵌入式浏览器3.py
@Time    :   2019/05/05 11:05:52
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
PyQt5实现多窗口切换的框架 - shangxiaqiusuo1的博客 - CSDN博客
https://blog.csdn.net/shangxiaqiusuo1/article/details/85253264
'''

import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class one(QMainWindow):
    sig_1 = pyqtSignal()

    def __init__(self):
        super(one, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(300, 200)
        self.setWindowTitle('1')
        self.btn_1 = QPushButton(self)
        self.btn_1.setText('Emit')
        self.btn_1.setGeometry(100, 80, 100, 40)
        self.btn_1.clicked.connect(self.slot_btn_1)
        self.sig_1.connect(self.sig_1_slot)

    def slot_btn_1(self):
        self.sig_1.emit()

    def sig_1_slot(self):
        self.t = two()
        self.t.show()


class two(QMainWindow):

    def __init__(self):
        super(two, self).__init__()
        self.resize(500, 100)
        self.setWindowTitle('two')


def ui_main():
    app = QApplication(sys.argv)
    w = one()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    ui_main()
