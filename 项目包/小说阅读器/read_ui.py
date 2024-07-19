# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-06-19 16:05:53
FilePath     : /CODE/项目包/小说阅读器/read_ui.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from PyQt6 import QtWidgets
from PyQt6.QtCore import QMetaObject, Qt
from PyQt6.QtWidgets import QHBoxLayout, QSplitter, QVBoxLayout
from xt_pyqt.part import xt_QCheckBox, xt_QLabel, xt_QLineEdit, xt_QListWidget, xt_QPushButton, xt_QTextBrowser
from xt_pyqt.wins import QIcon, xt_QMainWindow


class Ui_Window(xt_QMainWindow):
    def __init__(self):
        super().__init__("小说阅读器", tool=True, menu=True, status=True)
        self.setupUi()
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def setupUi(self):
        self.basepath = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(f"{self.basepath}/book.png"))
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.lineEdit = xt_QLineEdit()
        self.okB = xt_QPushButton("&OK 确定")
        self.okB.setObjectName("okB")
        self.listWidget = xt_QListWidget()
        self.listWidget.setObjectName("listWidget")
        self.QTextEdit = xt_QTextBrowser()
        self.readB = xt_QPushButton("&Read")
        self.readB.setObjectName("readB")
        self.upB = xt_QPushButton("上一章")
        self.upB.setObjectName("upB")
        self.downB = xt_QPushButton("下一章")
        self.downB.setObjectName("downB")
        self.jiaB = xt_QPushButton("＋")
        self.jiaB.setObjectName("jiaB")
        self.jianB = xt_QPushButton("－")
        self.jianB.setObjectName("jianB")
        self.checkbox = xt_QCheckBox("自动翻页")
        self.splitter = QSplitter(self)

    def retranslateUi(self):
        self.file_toolbar.addWidget(self.lineEdit)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.okB)

        ht_1 = QHBoxLayout()
        ht_1.addWidget(self.label, stretch=0)
        ht_1.addSpacing(10)
        ht_1.addStretch(2)
        ht_1.addWidget(self.jiaB, stretch=1)
        ht_1.addWidget(self.jianB, stretch=1)
        ht_1.addWidget(self.checkbox, stretch=1)
        ht_1.addWidget(self.readB, stretch=1)
        ht_1.addWidget(self.upB, stretch=1)
        ht_1.addWidget(self.downB, stretch=1)

        self.splitter.addWidget(self.listWidget)
        self.splitter.setStretchFactor(0, 2)  # 设定比例
        self.splitter.addWidget(self.QTextEdit)
        self.splitter.setStretchFactor(1, 5)  # 设定比例
        # Qt.Vertical 垂直   Qt.Horizontal 水平
        self.splitter.setOrientation(Qt.Horizontal)

        vt_0 = QVBoxLayout()
        vt_0.addLayout(ht_1)
        vt_0.addWidget(self.splitter)
        self.centralwidget.setLayout(vt_0)
        self.setCentralWidget(self.centralwidget)
        self.listWidgetCurrentRow = 0
