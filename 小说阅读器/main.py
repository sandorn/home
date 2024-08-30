# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-10-09 10:33:48
FilePath     : /CODE/项目包/小说阅读器/main.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSlot
from read_ui import Ui_Window
from xt_alitts.play import QThreadPyaudioText as QThreadPlayText
from xt_ls_bqg import get_contents, get_download_url
from xt_pyqt import event_loop

"""
音质不好，有杂音；
朗读反应较慢；
"""


class NyWindow(Ui_Window):
    def __init__(self):
        super().__init__()
        self.baseurl = "https://www.bigee.cc/book/"
        self.lineEdit.setText("6909")
        self.book_number = self.lineEdit.text()
        self.urls = []  # 章节链接列表
        self.titles = []  # 章节名称列表
        self.bookname = ""  # 小说名称
        self.listWidgetCurrentRow = 0  # 当前选中的行
        self.reader_thread = None

        self.QTextEdit.scroll_to_top_event = self.on_upB_clicked
        self.QTextEdit.scroll_to_bottom_event = self.on_downB_clicked
        self.lineEdit.textChanged.connect(self.setnum)
        self.lineEdit.returnPressed.connect(self.on_okB_clicked)
        self.jiaB.clicked.connect(self.QTextEdit.increase_text_size)
        self.jianB.clicked.connect(self.QTextEdit.decrease_text_size)

    def setnum(self):
        self.book_number = self.lineEdit.text()
        self.okB.setEnabled(True)

    @pyqtSlot()
    @event_loop
    def on_upB_clicked(self):
        if self.listWidgetCurrentRow > 0:
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow - 1)

    @pyqtSlot()
    @event_loop
    def on_downB_clicked(self):
        if self.listWidgetCurrentRow + 1 < self.listWidget.count():
            self.listWidget.setCurrentRow(self.listWidgetCurrentRow + 1)

    @pyqtSlot()
    @event_loop
    def on_okB_clicked(self):
        self.okB.setEnabled(False)
        self.listWidget.clean()
        self.QTextEdit.clear()

        self.getlist(f"{self.baseurl}{self.book_number}/")
        self.bindList()  # 对列表进行填充

    @pyqtSlot()
    def on_readB_clicked(self):
        if self.readB.text() == "&Read":
            self.read_read()
        else:
            self.read_stop()

    @event_loop
    def read_read(self):
        self.readB.setText("&STOP")
        if self.listWidgetCurrentRow == 0:
            self.listWidget.setCurrentRow(0)
        newText = self.QTextEdit.toPlainText().split("\n")  # 处理字符串
        self.reader_thread = QThreadPlayText(newText)
        self.reader_thread._signal_done.connect(self.playdone)
        self.reader_thread.start()  # 外部启动线程，线程启动后就会执行线程的run方法，防锁死

    def read_stop(self):
        self.readB.setText("&Read")
        if self.reader_thread is not None:
            self.reader_thread.stop()

    def playdone(self):
        self.read_stop()
        if self.checkbox.isChecked():
            QThread.msleep(100)
            self.on_downB_clicked()
            QThread.msleep(100)
            self.read_read()

    @event_loop
    def getlist(self, url):
        self.bookname, self.urls, self.titles = get_download_url(url)
        self.setWindowTitle(f"{self.title}--{self.bookname}")

    @event_loop
    def getcontent(self, url):
        _, title, content = get_contents(1, url)
        return f"《{self.bookname}->{title}" + "》\n\n" + content

    # 将文件显示在List列表中(图表显示)
    @event_loop
    def bindList(self):
        self.listWidget.addItems(
            [self.titles[index] for index in range(len(self.titles))]
        )
        self.listWidget.scrollToTop()  # scrollToBottom()

    # List列表单击方法，用来打开选中的项
    @event_loop
    def on_listWidget_currentRowChanged(self, row):
        self.listWidgetCurrentRow = row
        self.QTextEdit.clear()
        nowthread = QThread()
        nowthread.run = self.getcontent
        _text = nowthread.run(self.urls[row])
        self.QTextEdit.setText(_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = NyWindow()
    sys.exit(app.exec())
