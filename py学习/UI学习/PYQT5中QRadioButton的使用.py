# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-13 15:26:40
#LastEditTime : 2020-05-13 15:32:56
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
https://blog.csdn.net/zhulove86/article/details/52413767
'''

from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QStyleFactory, QVBoxLayout
import sys


class RadioButton(QWidget):

    def __init__(self):
        super(RadioButton, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("RadioButton")
        self.setGeometry(400, 400, 300, 260)

        self._xpButton = QRadioButton("WindowsXP")
        self._vistaButton = QRadioButton("WindowsVista")
        self._windowSButton = QRadioButton("Windows")
        self._xpButton.toggled.connect(lambda: self.changeStyle("WindowsXP"))
        self._vistaButton.toggled.connect(
            lambda: self.changeStyle("WindowsVista"))
        self._windowSButton.toggled.connect(lambda: self.changeStyle("Windows"))

        layout = QVBoxLayout()
        layout.addWidget(self._xpButton)
        layout.addWidget(self._vistaButton)
        layout.addWidget(self._windowSButton)
        layout.addStretch(1)

        self.setLayout(layout)
        self._xpButton.setChecked(True)
        self.changeStyle("Windows")

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RadioButton()
    sys.exit(app.exec_())
