# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-12 11:31:03
#LastEditTime : 2020-06-05 23:15:11
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMessageBox, QVBoxLayout, qApp

from xt_Ls_Bqg import get_contents, get_title_url
from xt_Alispeech.xt_Pygame import ReqSynthesizer_QThread_read
from xt_String import string_split_join_with_maxlen_list
from xt_Ui import EventLoop, xt_QLabel, xt_QLineEdit, xt_QListWidget, xt_QMainWindow, xt_QPushButton, xt_QTableView, xt_QTabWidget, xt_QTextBrowser, xt_QCheckBox

from pysnooper import snoop

from xt_Log import log
print = log().debug


class Ui_MainWindow(xt_QMainWindow):
    def __init__(self):
        super().__init__('小说阅读器')
        self.baseurl = 'https://www.biqukan.com'
        self.list = []  # 章节列表

        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.lineEdit = xt_QLineEdit('0_790')
        self.book_number = self.lineEdit.text()
        self.lineEdit.textChanged.connect(self.setnum)
        self.lineEdit.setObjectName('lineEditobj')
        self.pushButton = xt_QPushButton("&OK 确定")
        self.pushButton.setObjectName('ok_button')

        self.tabWidget = xt_QTabWidget(["列表显示", "图表显示"])
        self.tableWidget = xt_QTableView(['书号', '章节', '链接'])
        self.tabWidget.lay[0].addWidget(self.tableWidget)
        self.listWidget = xt_QListWidget()
        self.tabWidget.lay[1].addWidget(self.listWidget)
        self.tabWidget.setCurrentIndex(1)

        self.QTextEdit = xt_QTextBrowser()

        self.pushButton_read = xt_QPushButton("&Read")
        self.pushButton_read.clicked.connect(self.read_Button_event)
        self.pushButton_3 = xt_QPushButton("上一章")
        self.pushButton_3.clicked.connect(self.previous)
        self.pushButton_4 = xt_QPushButton("下一章")
        self.pushButton_4.clicked.connect(self.next)
        self.checkbox = xt_QCheckBox('自动翻页')

    def setnum(self):
        self.book_number = self.lineEdit.text()

    def retranslateUi(self):
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(self.pushButton)
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.tabWidget)
        vlayout1 = QVBoxLayout()
        vlayout1.addLayout(hlayout)
        vlayout1.addLayout(hlayout1)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.checkbox)
        hlayout2.addWidget(self.pushButton_read)
        hlayout2.addWidget(self.pushButton_3)
        hlayout2.addWidget(self.pushButton_4)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(self.QTextEdit)
        vlayout2.addLayout(hlayout2)

        hlayout3 = QHBoxLayout()
        hlayout3.addLayout(vlayout1)
        hlayout3.addLayout(vlayout2)

        vlayout3 = QVBoxLayout()
        vlayout3.addLayout(hlayout3)
        self.centralwidget.setLayout(vlayout3)
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)  # @  关键，用于自动绑定信号和函数
        self.tabWidget.currentChanged.connect(self.currentChanged_event)
        self.listWidgetCurrentRow = 0

    def currentChanged_event(self, index):
        if index == 0:
            self.pushButton_read.setHidden(True)
            self.pushButton_3.setHidden(True)
            self.pushButton_4.setHidden(True)
        else:
            self.pushButton_read.setHidden(False)
            self.pushButton_3.setHidden(False)
            self.pushButton_4.setHidden(False)
        pass

    def previous(self):
        if self.listWidgetCurrentRow == 0:
            return
        if self.listWidgetCurrentRow > 0:
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow - 1)

    def next(self):
        if self.listWidgetCurrentRow == 0:
            return
        if self.listWidgetCurrentRow + 1 < self.listWidget.count():
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow + 1)

    # 抓取所有数据
    @pyqtSlot()
    def on_ok_button_clicked(self):
        self.QTextEdit.clear()
        self.tableWidget.clean()
        self.listWidget.empty()   # clear()

        try:
            # # 设置书本初始地址,执行主方法
            self.getlist(self.baseurl + '/' + self.book_number + '/')
        except Exception as err:
            QMessageBox.warning(None, "警告", f"没有数据，请检查：{err}", QMessageBox.Ok)
        else:
            self.bindTable()  # 对表格进行填充
            self.bindList()  # 对列表进行填充

            self.listWidget.currentRowChanged.connect(self.currentRowChanged_event)
            self.tableWidget.clicked.connect(self.tableClick_event)  # @绑定表格单击方法

        # @交还控制权,恢复鼠标样式
        qApp.processEvents()
        QApplication.restoreOverrideCursor()
        return

    def read_Button_event(self):
        (self.read_read if self.pushButton_read.text() == '&Read' else self.read_stop)()
        # (func1 if y == 1 else func2)(arg1, arg2)
        # 如果y等于1,那么调用func1(arg1,arg2)否则调用func2(arg1,arg2)

    def read_stop(self):
        self.pushButton_read.setText('&Read')
        self.runthread.stop()
        qApp.processEvents()

    def read_read(self):
        self.pushButton_read.setText('&STOP')
        qApp.processEvents()
        # 处理字符串
        newText = string_split_join_with_maxlen_list(self.QTextEdit.toPlainText())
        self.runthread = ReqSynthesizer_QThread_read(newText, format='mp3')
        # #绑定ReqSynthesizer_QThread_read中定义的finished信号
        self.runthread._signal.connect(self.playdone)

    def playdone(self):
        self.read_stop()
        if self.checkbox.isChecked():
            self.next()
            self.read_read()

    @EventLoop
    def getlist(self, url):
        self.bookname, self.list = get_title_url(url)
        self.setWindowTitle(self.title + '--' + self.bookname)
        return
        # # 下载文件
        for title, articleUrl in enumerate(self.list):
            article_content = self.getcontent(articleUrl)
            fileName = self.bookname + '/' + title + '.txt'  # 设置保存路径
            with open(fileName, "w") as newFile:  # 打开或者创建文件
                newFile.write(article_content)  # 向文件中写入内容

    # 从网页提取数据
    @EventLoop
    def getcontent(self, url):
        index, title, content = get_contents(target=url)
        return "《" + self.bookname + '->' + title + "》\n\n" + content

    # 将文件显示在Table中（列表显示）
    @EventLoop
    def bindTable(self):
        res = [[self.book_number, self.list[index][0], self.list[index][1]] for index in range(len(self.list))]
        self.tableWidget.appendItems(res)
        self.tableWidget.scrollToTop()

    # 将文件显示在List列表中（图表显示）
    @EventLoop
    def bindList(self):
        self.listWidget.addItems([self.list[index][0] for index in range(len(self.list))])
        # self.listWidget.scrollToBottom()
        self.listWidget.scrollToTop()

    # 表格单击方法，用来打开选中的项
    @EventLoop
    def tableClick_event(self, item):
        self.QTextEdit.clear()
        QModelIndex = self.tableWidget.model.index(item.row(), 2)
        # _text = self.getcontent(QModelIndex.data())
        nowthread = QThread()
        nowthread.run = self.getcontent
        _text = nowthread.run(QModelIndex.data())

        # self.QTextEdit.setHtml(_text)
        self.QTextEdit.setText(_text)

    # 列表单击方法，用来打开选中的项
    @EventLoop
    def currentRowChanged_event(self, row):
        self.listWidgetCurrentRow = row
        self.QTextEdit.clear()
        # _text = self.getcontent(self.list[row][1])
        nowthread = QThread()
        nowthread.run = self.getcontent
        _text = nowthread.run(self.list[row][1])

        _text = '<font size="4">' + _text.replace("\n", "<br>") + '</font>'
        self.QTextEdit.setText(_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.QTextEdit.setText('根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。')
    sys.exit(app.exec_())  # 程序关闭时退出进程
