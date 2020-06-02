# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-25 11:55:19
@LastEditors: Even.Sand
@LastEditTime: 2019-05-25 12:18:05
'''
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox, QGridLayout, QPushButton, QProgressBar)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPixmap
import sys


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle("QProgressBar进度条")
        gridLayout = QGridLayout()
        self.btn1 = QPushButton("外圈跑马灯")
        self.btn2 = QPushButton("内圈跑马灯")
        self.pb11 = QProgressBar()
        self.pb12 = QProgressBar()
        self.pb13 = QProgressBar()
        self.pb14 = QProgressBar()
        self.pb21 = QProgressBar()
        self.pb22 = QProgressBar()
        self.pb11.setOrientation(Qt.Vertical)
        self.pb12.setOrientation(Qt.Horizontal)
        self.pb13.setOrientation(Qt.Vertical)
        self.pb14.setOrientation(Qt.Horizontal)
        self.pb21.setOrientation(Qt.Horizontal)
        self.pb22.setOrientation(Qt.Horizontal)
        gridLayout.addWidget(self.pb11, 0, 0, 6, 1)
        gridLayout.addWidget(self.pb12, 0, 1, 1, 6)
        gridLayout.addWidget(self.pb13, 0, 6, 6, 1)
        gridLayout.addWidget(self.pb14, 5, 1, 1, 6)
        gridLayout.addWidget(self.pb21, 1, 2, 1, 4)
        gridLayout.addWidget(self.btn1, 2, 3, 1, 1)
        gridLayout.addWidget(self.btn2, 3, 3, 1, 1)
        gridLayout.addWidget(self.pb22, 4, 2, 1, 4)
        self.setLayout(gridLayout)
        self.pb11.setStyleSheet("QProgressBar{border: 1px solid grey;text-align: center;font:bold 8pt 微软雅黑}"
                                "QProgressBar::chunk{background-color:skyblue;}")
        self.timer = QBasicTimer()
        self.step = 0
        self.pb21.setFormat("%v")
        self.pb22.setInvertedAppearance(True)
        self.btn1.clicked.connect(self.running)
        self.btn2.clicked.connect(self.doAction)

    def running(self):
        self.pb11.setMinimum(0)
        self.pb11.setMaximum(0)
        self.pb12.setMinimum(0)
        self.pb12.setMaximum(0)
        self.pb13.setMinimum(0)
        self.pb13.setMaximum(0)
        self.pb13.setInvertedAppearance(True)
        self.pb14.setMinimum(0)
        self.pb14.setMaximum(0)
        self.pb14.setInvertedAppearance(True)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            QMessageBox.information(self, "信息提示框", "内圈进度收工了！")
            self.btn2.setText("再来一次吧！")
            self.step = 0
            return
        self.step = self.step + 1
        self.pb21.setValue(self.step)
        self.pb22.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn2.setText("继续")
        else:
            self.timer.start(100, self)
            self.btn2.setText("停止")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
