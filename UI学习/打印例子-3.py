# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-21 20:44:30
#LastEditTime : 2020-05-21 20:46:49
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFormLayout, QDialog, QWidget, QAction
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QTextCursor, QTextDocument, QImage, QPixmap

#需要打印的文字
text = '11111111111wwwwwwwwwww呜呜呜呜呜呜呜呜无无无无'


class printDemo(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('打印demo')
        self.setGeometry(300, 300, 300, 200)
        self.createBar()

    #设置menuBar
    def createBar(self):
        bar = self.menuBar()
        printmenu = bar.addMenu('打印')

        #直接打印不显示
        printAction1 = QAction('直接打印不显示', self)
        printmenu.addAction(printAction1)
        printAction1.triggered.connect(self.no_showPrinter)

        #打印弹出设置对话框
        printAction2 = QAction('打印弹出设置', self)
        printmenu.addAction(printAction2)
        printAction2.triggered.connect(self.show_steupPrinter)
        #打印弹出预览对话框
        printAction3 = QAction('打印弹出预览', self)
        printmenu.addAction(printAction3)
        printAction3.triggered.connect(self.show_previewPrinter)
        #打印输出pdf
        printAction4 = QAction('打印输出pdf', self)
        printmenu.addAction(printAction4)
        printAction4.triggered.connect(self.show_pdfPrinter)

#打印不显示

    def no_showPrinter(self):
        printer = QPrinter()
        self.handlePaintRequest(printer)

#打印显示设置

    def show_steupPrinter(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer)
        if printDialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(printer)

#打印预览
#  ------------------这个比较特殊-----------------------------------

    def show_previewPrinter(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()


#输出pdf格式不打印

    def show_pdfPrinter(self):
        printer = QPrinter()
        # printDialog = QPrintDialog(printer)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName('a.pdf')
        self.handlePaintRequest(printer)

    #打印函数
    def handlePaintRequest(self, printer):
        #流程将文本或图片，其他写入QTextdocument中，然后调用print函数
        document = QTextDocument()
        cursor = QTextCursor(document)
        cursor.insertText(text)
        document.print(printer)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = printDemo()
    demo.show()
    sys.exit(app.exec())
