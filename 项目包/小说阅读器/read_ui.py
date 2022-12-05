# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
LastEditTime : 2022-12-05 12:14:35
FilePath     : /项目包/小说阅读器/read_ui.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtWidgets import QHBoxLayout, QSplitter, QVBoxLayout
from xt_Ui import (
    xt_QCheckBox,
    xt_QLabel,
    xt_QLineEdit,
    xt_QListWidget,
    xt_QMainWindow,
    xt_QPushButton,
    xt_QTextBrowser,
)


class Ui_Window(xt_QMainWindow):

    def __init__(self):
        super().__init__('小说阅读器', status=True, tool=True)
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.lineEdit = xt_QLineEdit('38_38165')
        self.book_number = self.lineEdit.text()
        self.lineEdit.setObjectName('lineEditobj')
        self.pushButton = xt_QPushButton("&OK 确定")
        self.pushButton.setObjectName('OK')
        self.listWidget = xt_QListWidget()
        self.QTextEdit = xt_QTextBrowser()

        self.pushButton_read = xt_QPushButton("&Read")
        self.pushButton_3 = xt_QPushButton("上一章")
        self.pushButton_4 = xt_QPushButton("下一章")
        self.checkbox = xt_QCheckBox('自动翻页')
        self.splitter = QSplitter(self)

    def retranslateUi(self):
        ht_1 = QHBoxLayout()
        ht_1.addWidget(self.label, stretch=0)
        ht_1.addWidget(self.lineEdit, stretch=2)
        ht_1.addWidget(self.pushButton)
        ht_1.addSpacing(10)
        ht_1.addStretch(2)
        ht_1.addWidget(self.checkbox, stretch=1)
        ht_1.addWidget(self.pushButton_read, stretch=1)
        ht_1.addWidget(self.pushButton_3, stretch=1)
        ht_1.addWidget(self.pushButton_4, stretch=1)

        self.splitter.addWidget(self.listWidget)
        self.splitter.setStretchFactor(0, 2)  # 设定比例
        self.splitter.addWidget(self.QTextEdit)
        self.splitter.setStretchFactor(1, 5)  # 设定比例
        self.splitter.setOrientation(Qt.Horizontal)  # Qt.Vertical 垂直   Qt.Horizontal 水平

        vt_0 = QVBoxLayout()
        vt_0.addLayout(ht_1)
        vt_0.addWidget(self.splitter)
        self.centralwidget.setLayout(vt_0)
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)  # @  关键，用于自动绑定信号和函数
        self.listWidgetCurrentRow = 0
