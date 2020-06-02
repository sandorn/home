# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 14:53:03
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 14:53:03
'''
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MenuDemo(QMainWindow):
    def __init__(self, parent=None):
        super(MenuDemo, self).__init__(parent)

        # 水平布局
        layout = QHBoxLayout()

        # 实例化主窗口的QMenuBar对象
        bar = self.menuBar()
        # 向菜单栏中添加新的QMenu对象，父菜单
        file = bar.addMenu('File')
        # 向QMenu小控件中添加按钮，子菜单
        file.addAction('New')

        # 定义响应小控件按钮，并设置快捷键关联到操作按钮，添加到父菜单下
        save = QAction('Save', self)
        save.setShortcut('Ctrl+S')
        file.addAction(save)

        # 创建新的子菜单项，并添加孙菜单
        edit = file.addMenu('Edit')
        edit.addAction('Copy')
        edit.addAction('Paste')
        # 菜单栏中的操作按钮可以是字符串或QAction对象
        # 添加父菜单下
        quit = QAction('Quit', self)
        file.addAction(quit)

        # 单击任何Qmenu对象，都会发射信号，绑定槽函数
        file.triggered[QAction].connect(self.processtrigger)

        # 设置布局及标题
        self.setLayout(layout)
        self.setWindowTitle('menu例子')

    def processtrigger(self, q):
        # 输出那个Qmenu对象被点击
        print(q.text() + 'is triggeres')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MenuDemo()
    demo.show()
    sys.exit(app.exec_())
