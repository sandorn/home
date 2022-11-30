# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-29 21:19:57
FilePath     : /UI学习/PyQt5实现split分隔栏.py
LastEditTime : 2022-11-29 21:19:58
Github       : https://github.com/sandorn/home
==============================================================
'''
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QListWidget,
    QMainWindow,
    QSplitter,
    QTextEdit,
    QTreeWidget,
)

# QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("utf8"))


class Csplitter(QMainWindow):

    def __init__(self, parent=None):
        super(Csplitter, self).__init__(parent)
        self.resize(400, 400)
        self.setWindowTitle('Pyqt Qsplitter')
        self.textedit = QTextEdit()
        self.textedit.setText("This is a TextEdit!")
        self.listwidget = QListWidget()
        self.listwidget.addItem("This is  a \nListWidget!")
        self.listwidget.addItem("aaaaaaaaaaaaaaa")
        self.treewidget = QTreeWidget()
        self.treewidget.setHeaderLabels(['This', 'is', 'a', 'TreeWidgets!'])
        splitter = QSplitter(self)
        splitter.addWidget(self.textedit)
        splitter.addWidget(self.listwidget)
        splitter.addWidget(self.treewidget)
        splitter.setOrientation(Qt.Horizontal)  # Qt.Vertical 垂直   Qt.Horizontal 水平
        self.setCentralWidget(splitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Csplitter()
    main.show()
    sys.exit(app.exec())
