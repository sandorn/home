# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-22 10:13:04
#LastEditTime : 2020-05-22 11:24:15
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import sys
from PyQt5.QtWidgets import *
from xjLib.xt_ui import xt_QMainWindow


class MyWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('嵌套布局实例')

        #全局布局（2中）：这里选择水平布局
        wlayout = QHBoxLayout()

        #局部布局：水平，垂直，网格，表单
        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()
        glayout = QGridLayout()
        flayout = QFormLayout()

        #为局部布局添加控件
        hlayout.addWidget(QPushButton(str(10)))
        hlayout.addWidget(QPushButton(str(1)))

        vlayout.addWidget(QPushButton(str(20)))
        vlayout.addWidget(QPushButton(str(21)))

        glayout.addWidget(QPushButton(str(30)), 0, 0)
        glayout.addWidget(QPushButton(str(31)), 0, 1)
        glayout.addWidget(QPushButton(str(32)), 1, 0)
        glayout.addWidget(QPushButton(str(33)), 1, 1)

        flayout.addWidget(QPushButton(str(40)))
        flayout.addWidget(QPushButton(str(41)))
        flayout.addWidget(QPushButton(str(42)))
        flayout.addWidget(QPushButton(str(43)))

        #准备四个控件
        hwg = QWidget()
        vwg = QWidget()
        gwg = QWidget()
        fwg = QWidget()

        #!使用四个控件设置局部布局
        hwg.setLayout(hlayout)
        vwg.setLayout(vlayout)
        gwg.setLayout(glayout)
        fwg.setLayout(flayout)

        #将四个控件添加到全局布局中
        wlayout.addWidget(hwg)
        wlayout.addWidget(vwg)
        wlayout.addWidget(gwg)
        wlayout.addWidget(fwg)

        #将窗口本身设置为全局布局
        # self.setLayout(wlayout)  #继承自QWidget

        widget = QWidget()
        widget.setLayout(wlayout)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
