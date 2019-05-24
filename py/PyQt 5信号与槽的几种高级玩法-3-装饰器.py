# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
PyQt 5信号与槽的几种高级玩法 - 博文视点（北京）官方博客 - CSDN博客
https://blog.csdn.net/broadview2006/article/details/80132757
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 19:42:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 19:58:57
'''
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
import sys


class CustWidget(QWidget):

    def __init__(self, parent=None):
        super(CustWidget, self).__init__(parent)

        self.okButton = QPushButton("OK", self)
        # 使用setObjectName设置对象名称
        self.okButton.setObjectName("okButton111")
        layout = QHBoxLayout()
        layout.addWidget(self.okButton)
        self.setLayout(layout)
        QtCore.QMetaObject.connectSlotsByName(self)

    @QtCore.pyqtSlot()
    def on_okButton111_clicked(self):
        print("单击了OK按钮")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustWidget()
    win.show()
    app.exec_()
