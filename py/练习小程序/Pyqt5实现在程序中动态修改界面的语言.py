# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-19 16:28:31
@LastEditors: Even.Sand
@LastEditTime: 2019-06-19 16:32:55

如何用Pyqt5实现在程序中动态修改界面的语言(英语转中文或者中文转英语) - Cholenm的博客 - CSDN博客
https://blog.csdn.net/CholenMine/article/details/80725088
'''
# Form implementation generated from reading ui file 'Window.ui'
# Created by: PyQt5 UI code generator 5.10.1
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(869, 751)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BtnHello = QtWidgets.QPushButton(self.centralwidget)
        self.BtnHello.setGeometry(QtCore.QRect(90, 110, 93, 28))
        self.BtnHello.setObjectName("BtnHello")
        self.BtnWorld = QtWidgets.QPushButton(self.centralwidget)
        self.BtnWorld.setGeometry(QtCore.QRect(300, 110, 93, 28))
        self.BtnWorld.setObjectName("BtnWorld")
        self.BtnCh = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCh.setGeometry(QtCore.QRect(480, 370, 93, 28))
        self.BtnCh.setObjectName("BtnCh")
        self.BtnEn = QtWidgets.QPushButton(self.centralwidget)
        self.BtnEn.setGeometry(QtCore.QRect(480, 430, 93, 28))
        self.BtnEn.setObjectName("BtnEn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 869, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BtnHello.setText(_translate("MainWindow", "Hello"))
        self.BtnWorld.setText(_translate("MainWindow", "world"))
        self.BtnCh.setText(_translate("MainWindow", "中文"))
        self.BtnEn.setText(_translate("MainWindow", "英文"))

#from Window import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from  PyQt5.QtGui import *
import sys

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        #  翻译家
        self.trans = QTranslator()
        # 连接到槽函数
        self.BtnEn.clicked.connect(self._trigger_english)
        self.BtnCh.clicked.connect(self._trigger_zh_cn)

    def _trigger_english(self):
        print("[MainWindow] Change to English")
        self.trans.load("en")
        _app = QApplication.instance()  # 获取app实例
        _app.installTranslator(self.trans)
        # 重新翻译界面
        self.retranslateUi(self)
        pass

    def _trigger_zh_cn(self):
        print("[MainWindow] Change to zh_CN")
        self.trans.load("zh_CN")
        _app = QApplication.instance()
        _app.installTranslator(self.trans)
        self.retranslateUi(self)
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())
