# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 13:50:49
@LastEditors: Even.Sand
@LastEditTime: 2019-05-24 18:04:35
'''
# calc.py

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget

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
        self.outputWidget.setObjectName("outw")  # 必须

        self.pushButton_getip = QtWidgets.QPushButton(Form)
        self.pushButton_getip.setGeometry(QtCore.QRect(210, 26, 80, 40))
        self.pushButton_getip.setObjectName("pg")  # 必须

        QtCore.QMetaObject.connectSlotsByName(Form)  # 必须


'''
---------------------
1. 界面部件需要setObjectname ;
2. 最后必须 QtCore.QMetaObject.connectSlotsByName(Form)
作者：爱人BT,来源：CSDN
原文：https://blog.csdn.net/u011146423/article/details/86468087
版权声明：本文为博主原创文章，转载请附上博文链接！
'''


# 方式一
class MyCalc(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('MyCalc')
        self.ui = Ui_Calc()
        self.ui.setupUi(self)
        self.setGeometry(200, 200, 600, 200)
        self.show()

    @pyqtSlot(int)
    def on_in1_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox2.value()))

    @pyqtSlot(int)
    def on_in2_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox1.value()))

    @pyqtSlot(str)
    def on_outw_valueChanged(self, text):
        self.ui.pushButton_getip.setText(str(self.ui.outputWidget.value()))

    @pyqtSlot()
    def on_pg_clicked(self):  # 接到信号完成添加任务  triggered
        self.ui.outputWidget.setText(str(self.ui.inputSpinBox1.value() * self.ui.inputSpinBox2.value()))  # 按下按钮需要完成的的任务

# 方式二


class MyCalc2(QWidget, Ui_Calc):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('MyCalc2')
        self.setupUi(self)
        self.setGeometry(200, 600, 600, 200)
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

    @pyqtSlot(str)
    def on_outw_valueChanged(self, text):
        self.pushButton_getip.setText(str(self.outputWidget.value()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MyCalc()
    win2 = MyCalc2()
    sys.exit(app.exec_())

    '''
    装饰器信号与槽的定义格式
    @PyQt5.QtCore.pyqtSlot(参数)
    def on_发送者对象名称_发射信号名称(self, 参数):
        pass
    '''
