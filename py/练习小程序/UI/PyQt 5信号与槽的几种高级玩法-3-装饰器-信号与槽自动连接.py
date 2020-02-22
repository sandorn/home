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
@LastEditTime: 2019-06-22 19:30:13
'''

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton


class CustWidget(QWidget):

    def __init__(self, parent=None):
        super(CustWidget, self).__init__(parent)

        self.okButton = QPushButton("OK", self)
        self.noButton = QPushButton("NO", self)
        # 使用setObjectName设置对象名称
        self.okButton.setObjectName("okButton")
        self.noButton.setObjectName("noButton")
        layout = QHBoxLayout()
        layout.addWidget(self.okButton)
        self.setLayout(layout)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.okButton.clicked.connect(self.okButton_clicked)

    def okButton_clicked(self):
        print("单击了OK按钮")

    @QtCore.pyqtSlot()
    def on_noButton_clicked(self):
        print("单击了NO按钮")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustWidget()
    win.show()
    sys.exit(app.exec_())
