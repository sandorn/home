# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-17 16:19:28
#FilePath     : /xjLib/test/ui-test.py
#LastEditTime : 2020-06-18 10:09:19
#Github       : https://github.com/sandorn/home
#==============================================================
"""

import sys
from xt_pyqt import EventLoop, xt_QLabel, xt_QLineEdit, xt_QListWidget, xt_QMainWindow, xt_QPushButton, xt_QTableView, xt_QTabWidget, xt_QTextBrowser, xt_QCheckBox, xt_QTreeWidget, xt_QTableWidget
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, qApp, QWidget
from PyQt5.QtCore import QMetaObject, QThread, pyqtSlot
import random
from pysnooper import snoop
from xt_Log import log

log = log()
snooper = snoop(log.filename)
print = log.debug


class Example(xt_QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_UI()
        self.retranslateUi()

    def create_UI(self):
        self.btn = xt_QPushButton("Start==", self)
        self.btn1 = xt_QPushButton("Start!=", self)
        self.btn3 = xt_QPushButton("<-Start->", self)
        self.tree = xt_QTreeWidget(["aaa", "b", "cc"])
        self.tree.addItem(["child1", "name11", "name22"])
        for index in range(1, 20):
            self.tree.addItem(["child" + str(index * 10), "name1" + str(index * 10)])
        self.table = xt_QTableWidget([1, 2, 3], 10, 5)
        self.tabw = xt_QTabWidget(2)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.tabls)
        self.btn1.clicked.connect(self.tabls2)
        self.btn3.clicked.connect(self.getDatas)

    def retranslateUi(self):
        # #设置窗口布局
        vlayout1 = QVBoxLayout()
        vlayout1.addWidget(self.btn)
        vlayout1.addWidget(self.btn1)
        vlayout1.addWidget(self.btn3)
        vlayout1.addWidget(self.tree)
        vlayout1.addWidget(self.tabw)
        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout1)
        hlayout.addWidget(self.table)
        # hlayout各控件的比例
        hlayout.setStretchFactor(vlayout1, 1)
        hlayout.setStretchFactor(self.table, 3)
        hlayout.setSpacing(1)  # 设置控件间距
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def getDatas(self):
        for i in range(50):
            self.pbar.step.emit("adfrgagaew")
            self.pbar.step.emit(None)

        QThread.msleep(200)
        self.pbar.step.emit(0)
        QThread.msleep(200)
        self.pbar.step.emit(60)
        QThread.msleep(200)
        self.pbar.step.emit(120)
        QThread.msleep(200)
        self.pbar.step.emit(30)

    def tabls(self):
        self.table.empty()
        self.table.appendItem(["1", "记录一"])
        self.table.appendItem(["2", "记录2", 2, 3, 4, 5])
        self.table.appendItems([["3", "记录3"], ["4", "记录4"], ["5", "记录5", "djahd", "ihviairh" * 5, "ohv7384" * 3]])
        r = []
        for i in range(10):
            ran_str = "".join(random.sample("zyxwvutsrqponmlkjihgfedcba0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()", 5))
            ran_str_2 = "".join(random.sample("zyxwvutsrqponmlkjihgfedcba0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()", 27))
            r.append([i * 10, "记录" + ran_str, ran_str_2])
            # self.table.appendItem([i * 10, '记录' + str(i * 10)])
        # print(r)
        self.table.appendItems(r)
        self.table.setColumnName(0, "张三")
        self.table.setRowName(0, "张4")
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(3, 80)

    def tabls2(self):
        # self.table.columnsNameShow()
        self.table.setColumnsName(["A", "B", "C", "DD"])
        self.table.setRowsName(["A", "B", "C", "DDDDDDDDDD"])


app = QApplication(sys.argv)
ex = Example()
# ex = xt_QMainWindow()
sys.exit(app.exec_())
