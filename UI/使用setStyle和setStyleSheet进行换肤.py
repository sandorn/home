# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-15 16:12:04
#LastEditTime : 2020-05-15 18:04:51
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
PyQt5学习笔记9_使用setStyle和setStyleSheet进行换肤_Python_yy123xiang的专栏-CSDN博客
https://blog.csdn.net/yy123xiang/article/details/86771131
'''

import sys
from os.path import join, dirname, abspath
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyleFactory, QPushButton, QVBoxLayout, QWidget
import qdarkstyle
from xjLib.xt_ui import xt_QPushButton
# _UI = join(dirname(abspath(__file__)), 'mainwindow.ui')


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.actionWindows = QPushButton('actionWindows', self)
        self.actionWindowsXP = xt_QPushButton('actionWindowsXP', self)
        self.actionWindowsVista = xt_QPushButton('actionWindowsVista', self)
        self.actionFusion = xt_QPushButton('actionFusion', self)
        self.actionQdarkstyle = xt_QPushButton('actionQdarkstyle', self)
        #uic.loadUi(_UI, self)
        # #设置窗口布局
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(self.actionWindows)
        vlayout1.addWidget(self.actionWindowsXP)
        vlayout1.addWidget(self.actionWindowsVista)
        vlayout1.addWidget(self.actionFusion)
        vlayout1.addWidget(self.actionQdarkstyle)
        widget = QWidget()
        widget.setLayout(vlayout1)
        self.setCentralWidget(widget)


class Application(QApplication):

    def __init__(self, argv):
        QApplication.__init__(self, argv)

    def _slot_setStyle(self):
        app.setStyleSheet('')
        tmp = self.sender().objectName()  # [6:]
        if tmp in QStyleFactory.keys():
            app.setStyle(tmp)
        elif tmp == 'Qdarkstyle':
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


if __name__ == '__main__':
    app = Application(sys.argv)
    w = MainWindow()
    w.actionWindows.clicked.connect(app._slot_setStyle)
    w.actionWindowsXP.clicked.connect(app._slot_setStyle)
    w.actionWindowsVista.clicked.connect(app._slot_setStyle)
    w.actionFusion.clicked.connect(app._slot_setStyle)
    w.actionQdarkstyle.clicked.connect(app._slot_setStyle)
    w.show()
    sys.exit(app.exec_())
