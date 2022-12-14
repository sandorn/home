# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-19 11:38:38
@LastEditors: Even.Sand
@LastEditTime: 2019-06-19 11:40:23
'''
from PyQt5.QtGui import QFont, QTextDocument, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSizePolicy, QAction, QDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import sys

the_text = """
《描写雪的诗句》赏析
不知庭霰今朝落，疑是林花昨夜开《苑中遇雪》
忽如一夜春风来，千树万树梨花开《白雪歌送武》
白雪却嫌春色晚，故穿庭树作飞花《春雪》
雪似梅花，梅花似雪。似和不似都奇绝《踏莎行》
千峰笋石千株玉，万树松萝万朵银《南秦雪》
六出飞花入户时，坐看青竹变琼枝《对雪》
地白风色寒，雪花大如手《嘲王历阳不肯饮酒》
燕山雪花大如席，片片吹落轩辕台《北风行》
白雪纷纷何所似？撒盐空中差可拟《咏雪联句》
才见岭头云似盖，已惊岩下雪如尘《南秦雪》
"""


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("打印功能")

        # 创建文本框
        self.label = QLabel()
        self.label.setFont(QFont("微软雅黑", 14, QFont.Bold))
        self.label.setText(the_text)
        self.setCentralWidget(self.label)

        # 创建菜单栏
        self.createMenus()

    def createMenus(self):
        # 创建动作一
        self.printAction1 = QAction(self.tr("打印无预览"), self)
        self.printAction1.triggered.connect(self.on_printAction1_triggered)

        # 创建动作二
        self.printAction2 = QAction(self.tr("打印有预览"), self)
        self.printAction2.triggered.connect(self.on_printAction2_triggered)

        # 创建动作三
        self.printAction3 = QAction(self.tr("直接打印"), self)
        self.printAction3.triggered.connect(self.on_printAction3_triggered)

        # 创建动作四
        self.printAction4 = QAction(self.tr("打印到PDF"), self)
        self.printAction4.triggered.connect(self.on_printAction4_triggered)

        # 创建菜单，添加动作
        self.printMenu = self.menuBar().addMenu(self.tr("打印"))
        self.printMenu.addAction(self.printAction1)
        self.printMenu.addAction(self.printAction2)
        self.printMenu.addAction(self.printAction3)
        self.printMenu.addAction(self.printAction4)

    # 动作一：打印，无预览
    def on_printAction1_triggered(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(printer)

    # 动作二：打印，有预览
    def on_printAction2_triggered(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    # 动作三：直接打印
    def on_printAction3_triggered(self):
        printer = QPrinter()
        self.handlePaintRequest(printer)

    # 动作四：打印到pdf
    def on_printAction4_triggered(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("D:/pdf打印测试.pdf")
        self.handlePaintRequest(printer)

    ## 打印函数
    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        cursor.insertText(self.label.text())
        document.print(printer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
