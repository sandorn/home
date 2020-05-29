# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-28 19:03:16
#LastEditTime : 2020-05-28 19:03:20
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from PyQt5.QtWidgets import *
import sys


class QlabelDemo(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLabel快键键例子")
        nameLb1 = QLabel('&Name', self)  #建立快捷键
        nameEd1 = QLineEdit(self)  #建立单行文本输入框
        nameLb1.setBuddy(nameEd1)
        #可以使用快捷键快速定位到相关位置
        #Alt+N：定位到NAME文本输入框

        nameLb2 = QLabel('&Password', self)
        nameEd2 = QLineEdit(self)
        nameLb2.setBuddy(nameEd2)

        btnOk = QPushButton('&OK')
        btnCancel = QPushButton('&Cancel')
        mainLayout = QGridLayout()
        mainLayout.addWidget(nameLb1, 0, 0)
        mainLayout.addWidget(nameEd1, 0, 1, 1, 2)
        mainLayout.addWidget(nameLb2, 1, 0)
        mainLayout.addWidget(nameEd2, 1, 1, 1, 2)
        mainLayout.addWidget(btnOk, 2, 1)
        mainLayout.addWidget(btnCancel, 2, 2)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    labelDemo = QlabelDemo()
    labelDemo.show()
    sys.exit(app.exec_())
