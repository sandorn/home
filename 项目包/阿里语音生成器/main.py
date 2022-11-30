# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-29 23:53:26
FilePath     : /项目包/阿里语音生成器/main.py
LastEditTime : 2022-12-01 00:42:58
Github       : https://github.com/sandorn/home
==============================================================
'''
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QSplitter
from xt_Alispeech.conf import VIOCE

# from pysnooper import snoop
from xt_Alispeech.ex_NSS import NSS_TTS
from xt_String import str_split_limited_list
from xt_Ui import EventLoop, xt_QLineEdit, xt_QMainWindow, xt_QTableView, xt_QTextEdit


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('阿里语音合成器')
        self.args_dict = {}  # 存参数
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setupUi()
        self.retranslateUi()
        self.bindTable()

    def setupUi(self):
        self.tableWidget = xt_QTableView(['名称', '参数值', '类型', '适用场景', '支持语言', '采样率', '时间戳', '儿化音', '声音品质'])
        self.FilePath = xt_QLineEdit()
        self.QTextEdit = xt_QTextEdit()
        self.splitter = QSplitter(self)

    def retranslateUi(self):
        self.splitter.addWidget(self.tableWidget)
        self.splitter.setStretchFactor(0, 4)  # 设定比例
        self.splitter.addWidget(self.QTextEdit)
        self.splitter.setStretchFactor(1, 6)  # 设定比例
        self.splitter.setOrientation(Qt.Horizontal)  # Qt.Vertical 垂直  # Qt.Horizontal 水平
        self.setCentralWidget(self.splitter)
        self.QTextEdit.textChanged.connect(self.textChanged_event)  # @绑定方法
        # self.open_action.triggered.connect(self.on_openObject_triggered)  # @绑定方法

    @EventLoop
    def bindTable(self):
        res = [[*item] for item in VIOCE]
        self.tableWidget.appendItems(res)
        self.tableWidget.scrollToTop()
        self.tableWidget.clicked.connect(self.tableClick_event)  # @绑定表格单击方法

    @EventLoop
    def tableClick_event(self, item):
        QModelIndex = self.tableWidget.model.index(item.row(), 1)
        _text = QModelIndex.data()
        self.args_dict.update({'vioce': _text})

    @pyqtSlot()
    @EventLoop
    def on_openObject_triggered(self, *args, **kwargs):
        self.args_dict.update({'savefile': False})
        res_list = NSS_TTS(self.text, self.args_dict)
        res_list.sort(key=lambda x: x[0])
        f = open('D:/test.mp3', "wb")
        for item in res_list:
            f.write(item[1])
        f.close()

    def textChanged_event(self):
        self.text = str_split_limited_list(self.QTextEdit.toPlainText())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.QTextEdit.setText('根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组')
    sys.exit(app.exec_())  # 程序关闭时退出进程
