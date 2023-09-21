# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-05 12:06:28
LastEditTime : 2022-12-05 12:06:28
FilePath     : /项目包/小说阅读器/main.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from read_ui import Ui_Window
from xt_Alispeech.Play import Synt_Read_QThread
from xt_Ls_Bqg import get_contents, get_download_url
from xt_String import str2list
from xt_Thread import Thread_wrap
from xt_Ui import EventLoop


class NyWindow(Ui_Window):

    def __init__(self):
        super().__init__()
        self.baseurl = 'https://www.biqukan8.cc/'
        self.urls = []  # 章节链接列表
        self.titles = []  # 章节名称列表
        self.setWindowTitle('小说阅读器')
        self.setWindowOpacity(0.9)  # 设置窗口透明度

        self.lineEdit.textChanged.connect(self.setnum)
        self.pushButton_read.clicked.connect(self.read_Button_event)
        self.pushButton_3.clicked.connect(self.previous)
        self.pushButton_4.clicked.connect(self.nextpage)

    @pyqtSlot()
    @EventLoop
    def on_Run_triggered(self, *args, **kwargs):
        ...

    @pyqtSlot()
    def on_Do_triggered(self):
        ...

    def setnum(self):
        self.book_number = self.lineEdit.text()

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
        self.listWidget.clean()

        try:
            self.getlist(f'{self.baseurl}/{self.book_number}/')
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
        newText = str2list(self.QTextEdit.toPlainText())  # 处理字符串
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
        self.setWindowTitle(f'{self.title}--{self.bookname}')
        return

    @EventLoop
    @Thread_wrap
    def getcontent(self, url):
        _, title, content = get_contents(1, url)
        return f"《{self.bookname}->{title}" + "》\n\n" + content

    # 将文件显示在List列表中(图表显示)
    @EventLoop
    def bindList(self):
        self.listWidget.addItems([self.titles[index] for index in range(len(self.titles))])
        self.listWidget.scrollToTop()  # scrollToBottom()

    # List列表单击方法，用来打开选中的项
    @EventLoop
    def currentRowChanged_event(self, row):
        self.listWidgetCurrentRow = row
        self.QTextEdit.clear()
        _qh = self.getcontent(self.urls[row])
        _text = _qh.getResult()
        # nowthread = QThread()
        # nowthread.run = self.getcontent
        # _text = nowthread.run(self.urls[row])

        self.QTextEdit.setFontPointSize(16)  # 设置字号
        self.QTextEdit.setText(_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = NyWindow()
    sys.exit(app.exec())
