# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 11:12:10
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 11:13:29
'''
import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.show()
        pass

    def initUI(self):
        _path = os.path.dirname(__file__) + '/'
        self.setWindowIcon(QIcon(_path + 'ico/ico.ico'))
        self.setWindowTitle('setWindowTitle')
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready to compose')

        # 创建一个垂直布局器
        win1Dock = self.getDock("win1")
        win2Dock = self.getDock("win2")
        self.addDockWidget(Qt.LeftDockWidgetArea, win1Dock)
        self.addDockWidget(Qt.RightDockWidgetArea, win2Dock)
        # 实现任意嵌套
        self.setDockNestingEnabled(True)
        # 实现分隔 (可水平 / 垂直 / 垂直+水平 从而实现任意效果)
        self.splitDockWidget(win1Dock, win2Dock, Qt.Horizontal)
        # self.splitDockWidget(win1Dock, win4Dock, Qt.Vertical)
        # 窗口大小位置
        (_weith, _height) = (788, 548)
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry((screen.width() - _weith) / 2,
                         (screen.height() - _height) / 2, _weith, _height)

    def getDock(self, name):
        w = QWidget()
        dock = QDockWidget(name)
        dock.setWidget(w)
        dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable)
        return dock


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
