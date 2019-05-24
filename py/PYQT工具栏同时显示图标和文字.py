# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 17:36:02
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 17:38:53
'''
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        _path = os.path.dirname(__file__) + '/'
        exitAction1 = QAction(QIcon(_path + 'sign-out.png'), '退出1', self)
        exitAction2 = QAction(QIcon(_path + 'save.png'), '保存', self)

        # 快捷键设置
        exitAction1.setShortcut('Ctrl+Q')

        # 信号与槽的连接
        exitAction1.triggered.connect(qApp.quit)

        self.toolbar1 = self.addToolBar('退出1')
        self.toolbar2 = self.addToolBar('保存')

        # 在工具栏ToolBar里同时添加图标和文字，并设置图标和文字的相对位置；若没有下面的一行代码，则只显示图标或文字。
        # self.toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar1.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbar2.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.toolbar1.addAction(exitAction1)
        self.toolbar2.addAction(exitAction2)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('工具栏案例')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
