# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-03-02 17:16:22
FilePath     : /CODE/py学习/UI学习/自定义标题栏.py
Github       : https://github.com/sandorn/home
==============================================================
CustomTitleBar/python at master · grayondream/CustomTitleBar
https://github.com/grayondream/CustomTitleBar/tree/master/python
'''

import sys

from TitleBar import *


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.InitializeWindow()

    def InitializeWindow(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.InitializeViews()
        self.setStyleSheet(str(self.LoadStyleFromQss(WINDOW_QSS)))

    def InitializeViews(self):
        self.titleBar = TitleBar(self)
        self.client = QWidget(self)
        self.center = QWidget(self)

        self.setCentralWidget(self.center)

        self.lay = QVBoxLayout(self)
        self.center.setLayout(self.lay)

        self.lay.addWidget(self.titleBar)
        self.lay.addWidget(self.client)
        self.lay.setStretch(1, 100)
        self.lay.setSpacing(0)
        self.lay.setContentsMargins(0, 0, 0, 0)

        self.titleBar.SetIcon(QPixmap(WINDOW_ICON))
        self.titleBar.SetTitle(WINDOW_TITLE)

    def LoadStyleFromQss(self, f):
        with open(f) as file:
            lines = file.readlines()
        return ''.join(lines)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
