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
from PyQt6.QtWidgets import QMessageBox
from read_ui import Ui_Window
from xt_alitts.play import Synt_Read_QThread
from xt_ls_bqg import get_contents, get_download_url
from xt_pyqt import event_loop
from xt_str import str2list
from xt_thread import thread_decorator


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
        self.runthread = None

        self.QTextEdit.scroll_to_top_event = self.on_upB_clicked
        self.QTextEdit.scroll_to_bottom_event = self.on_downB_clicked
        self.lineEdit.textChanged.connect(self.setnum)
        self.lineEdit.returnPressed.connect(self.on_okB_clicked)
        self.jiaB.clicked.connect(self.QTextEdit.increase_text_size)
        self.jianB.clicked.connect(self.QTextEdit.decrease_text_size)

    def setnum(self):
        self.book_number = self.lineEdit.text()

    @pyqtSlot()
    @event_loop
    def on_upB_clicked(self):
        if self.listWidgetCurrentRow == 0:
            return
        self.listWidget.setCurrentRow(self.listWidgetCurrentRow - 1)

    @pyqtSlot()
    @event_loop
    def on_downB_clicked(self):
        if self.listWidgetCurrentRow + 1 == self.listWidget.count():
            return
        self.listWidget.setCurrentRow(self.listWidgetCurrentRow + 1)

    @pyqtSlot()
    @event_loop
    def on_okB_clicked(self):
        self.listWidget.clean()
        self.QTextEdit.clear()

        try:
            self.getlist(f"{self.baseurl}/{self.book_number}/")
        except Exception as err:
            QMessageBox.warning(
                None, "警告", f"没有数据，请检查：{err}", QMessageBox.Ok
            )
        else:
            self.bindList()  # 对列表进行填充
        return

    @pyqtSlot()
    def on_readB_clicked(self):
        (self.read_read if self.readB.text() == "&Read" else self.read_stop)()

    @event_loop
    def read_read(self):
        self.readB.setText("&STOP")
        newText = str2list(self.QTextEdit.toPlainText())  # 处理字符串
        self.runthread = Synt_Read_QThread(newText)
        # #绑定Synt_Read_QThread中定义的信号
        self.runthread._signal.connect(self.playdone)

    @event_loop
    def read_stop(self):
        self.readB.setText("&Read")
        if self.runthread is not None:
            self.runthread.stop()

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
        return

    @event_loop
    @thread_decorator
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
    # @pyqtSlot(int)  # 参数与func一致  #有没有都行
    @event_loop
    def on_listWidget_currentRowChanged(self, row):
        self.listWidgetCurrentRow = row
        self.QTextEdit.clear()
        _text = self.getcontent(
            self.urls[row]
        ).getResult()  # 获取thread_decorator线程返回值
        # nowthread = QThread()
        # nowthread.run = self.getcontent
        # _text = nowthread.run(self.urls[row])

        self.QTextEdit.setText(_text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = NyWindow()
    sys.exit(app.exec())
