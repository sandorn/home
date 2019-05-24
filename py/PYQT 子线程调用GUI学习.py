# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
PYQT 子线程调用GUI学习记录---添加文档到textbrowser - monkeyfx的博客 - CSDN博客
https://blog.csdn.net/monkeyfx/article/details/58602502
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 13:47:31
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 18:41:12
'''
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets


class Ui_Calc(object):
    def setupUi(self, Form):

        self.inputSpinBox1 = QtWidgets.QSpinBox(Form)
        self.inputSpinBox1.setGeometry(QtCore.QRect(1, 26, 46, 25))
        self.inputSpinBox1.setObjectName("in1")  # 必须

        self.inputSpinBox2 = QtWidgets.QSpinBox(Form)
        self.inputSpinBox2.setGeometry(QtCore.QRect(70, 26, 46, 25))
        self.inputSpinBox2.setObjectName("in2")  # 必须

        self.outputWidget = QtWidgets.QLabel(Form)
        self.outputWidget.setGeometry(QtCore.QRect(140, 24, 36, 27))
        self.outputWidget.setObjectName("outputWidget")  # 必须

        self.pushButton_getip = QtWidgets.QPushButton(Form)
        self.pushButton_getip.setGeometry(QtCore.QRect(210, 24, 80, 27))
        self.pushButton_getip.setObjectName("pg")  # 必须

        QtCore.QMetaObject.connectSlotsByName(Form)  # 必须


class MainWindow(QMainWindow, Ui_Calc):
    #_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setGeometry(200, 200, 600, 200)
        self.show()

    @pyqtSlot()
    def on_pg_clicked(self):
        self.outputWidget.setText(str(self.inputSpinBox1.value() * self.inputSpinBox2.value()))  # 按下按钮需要完成的的任务
        # execute.test(self)  # 按下按钮需要完成的的任务

    @pyqtSlot(int)
    def on_in1_valueChanged(self, value):
        self.outputWidget.setText(str(value + self.inputSpinBox2.value()))

    @pyqtSlot(int)
    def on_in2_valueChanged(self, value):
        self.outputWidget.setText(str(value + self.inputSpinBox1.value()))

    def chengfa(self, string):  # 接到信号完成添加任务
        self.outputWidget.setText(str(self.inputSpinBox1.value() * self.inputSpinBox2.value()))  # 按下按钮需要完成的的任务


class execute(QMainWindow, Ui_Calc):
    def test(self):
        add = MainWindow()  # c#中的类的实例化，方便调用
        add._signal.connect(self.chengfa)  # 连接信号
        add._signal.emit("aaaa")  # 传递要添加数据的信号


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = MainWindow()
    sys.exit(app.exec_())
