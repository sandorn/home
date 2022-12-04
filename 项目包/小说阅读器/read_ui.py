# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
LastEditTime : 2022-12-03 16:35:20
FilePath     : /项目包/小说阅读器/read_ui.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, Qt, QThread, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QSplitter, QVBoxLayout
from xt_Alispeech.xt_Pygame import Synt_Read_QThread
from xt_Ls_Bqg import ahttp_get_contents, get_download_url
from xt_String import str_split_limited_list
from xt_Ui import (
    EventLoop,
    xt_QCheckBox,
    xt_QLabel,
    xt_QLineEdit,
    xt_QListWidget,
    xt_QMainWindow,
    xt_QPushButton,
    xt_QTextBrowser,
)


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('小说阅读器', status=True, tool=True)
        self.baseurl = 'https://www.biqukan8.cc/'
        self.urls = []  # 章节链接列表
        self.titles = []  # 章节名称列表
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.lineEdit = xt_QLineEdit('38_38165')
        self.book_number = self.lineEdit.text()
        self.lineEdit.textChanged.connect(self.setnum)
        self.lineEdit.setObjectName('lineEditobj')
        self.pushButton = xt_QPushButton("&OK 确定")
        self.pushButton.setObjectName('OK')
        self.listWidget = xt_QListWidget()
        self.QTextEdit = xt_QTextBrowser()

        self.pushButton_read = xt_QPushButton("&Read")
        self.pushButton_read.clicked.connect(self.read_Button_event)
        self.pushButton_3 = xt_QPushButton("上一章")
        self.pushButton_3.clicked.connect(self.previous)
        self.pushButton_4 = xt_QPushButton("下一章")
        self.pushButton_4.clicked.connect(self.nextpage)
        self.checkbox = xt_QCheckBox('自动翻页')
        self.splitter = QSplitter(self)

    @pyqtSlot()
    @EventLoop
    def on_Run_triggered(self, *args, **kwargs):
        ...

    @pyqtSlot()
    def on_Do_triggered(self):
        ...

    def setnum(self):
        self.book_number = self.lineEdit.text()

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

    def previous(self):
        if self.listWidgetCurrentRow == 0: return
        if self.listWidgetCurrentRow > 0:
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow - 1)

    def nextpage(self):
        if self.listWidgetCurrentRow + 1 == self.listWidget.count(): return
        if self.listWidgetCurrentRow + 1 < self.listWidget.count():
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow + 1)

    @pyqtSlot()
    @EventLoop
    def on_OK_clicked(self):
        self.QTextEdit.clear()
        # self.tableWidget.clean()
        self.listWidget.clean()

        try:
            self.getlist(self.baseurl + '/' + self.book_number + '/')
        except Exception as err:
            QMessageBox.warning(None, "警告", f"没有数据，请检查：{err}", QMessageBox.Ok)
        else:
            self.bindList()  # 对列表进行填充
            self.listWidget.currentRowChanged.connect(self.currentRowChanged_event)  # @绑定单击方法
        return

    def read_Button_event(self):
        (self.read_read if self.pushButton_read.text() == '&Read' else self.read_stop)()

    @EventLoop
    def read_stop(self):
        self.pushButton_read.setText('&Read')
        self.runthread.stop()

    @EventLoop
    def read_read(self):
        self.pushButton_read.setText('&STOP')
        newText = str_split_limited_list(self.QTextEdit.toPlainText())  # 处理字符串
        self.runthread = Synt_Read_QThread(newText)
        self.runthread._signal.connect(self.playdone)  # #绑定Synt_Read_QThread中定义的信号

    def playdone(self):
        self.read_stop()
        if self.checkbox.isChecked():
            QThread.msleep(100)
            self.nextpage()
            QThread.msleep(100)

            self.read_read()

    @EventLoop
    def getlist(self, url):
        self.bookname, self.urls, self.titles = get_download_url(url)
        self.setWindowTitle(self.title + '--' + self.bookname)
        return

    @EventLoop
    def getcontent(self, url):
        index, title, content = ahttp_get_contents((1, url))
        return "《" + self.bookname + '->' + title + "》\n\n" + content

    # 将文件显示在List列表中（图表显示）
    @EventLoop
    def bindList(self):
        self.listWidget.addItems([self.titles[index] for index in range(len(self.titles))])
        self.listWidget.scrollToTop()  # scrollToBottom()

    # List列表单击方法，用来打开选中的项
    @EventLoop
    def currentRowChanged_event(self, row):
        self.listWidgetCurrentRow = row
        self.QTextEdit.clear()
        nowthread = QThread()
        nowthread.run = self.getcontent  # type: ignore
        _text = nowthread.run(self.urls[row])

        self.QTextEdit.setFontPointSize(16)  # 设置字号
        self.QTextEdit.setText(_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec())
