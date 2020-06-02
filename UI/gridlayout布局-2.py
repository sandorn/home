# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software :   VSCode
@File     :   gridlayout布局-2.py
@Time     :   2019/05/06 16:45:29
@Author   :   Even Sand
@Version  :   1.0
@Contact  :   sandorn@163.com
@License  :   (C)Copyright 2009-2019, NewSea
PyQt5学习教程10：再议Grid Layout - snmplink的博客 - CSDN博客
https://blog.csdn.net/qingwufeiyang12346/article/details/78381246
'''

import sys
from PyQt5.QtWidgets import QWidget, \
                              QPushButton, \
                              QToolTip, \
                              QMessageBox, \
                              QApplication, \
                              QDesktopWidget, \
                              QMainWindow, \
                              QAction, \
                              qApp, \
                              QTextEdit, \
                              QLabel, \
                              QGridLayout, \
                              QLineEdit
from PyQt5.QtGui import QFont, \
                          QIcon


# QMainWindow是QWidget的派生类
class CMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ToolTip设置
        QToolTip.setFont(QFont('华文楷体', 10))

        # statusBar设置
        self.statusBar().showMessage('准备就绪')

        # 退出Action设置
        exitAction = QAction(QIcon('1.png'), '&Exit', self)
        exitAction.setShortcut('ctrl+Q')
        exitAction.setStatusTip('退出应用程序')
        exitAction.triggered.connect(
            qApp.quit)  # qApp就相当于QCoreApplication.instance()

        # menuBar设置
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # toolBar设置
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # Label设置
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        # LineEdit设置
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        # GridLayout布局
        grid = QGridLayout()
        grid.setSpacing(10)  # 设置控件的间隙为10
        widget = QWidget()
        self.setCentralWidget(widget)  # 建立的widget在窗体的中间位置
        widget.setLayout(grid)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.resize(500, 300)
        self.center()
        self.setFont(QFont('华文楷体', 10))
        self.setWindowTitle('PyQt5应用教程（snmplink编著）')
        self.setWindowIcon(QIcon('10.png'))
        self.show()

    def center(self):
        # 得到主窗体的框架信息
        qr = self.frameGeometry()
        # 得到桌面的中心
        cp = QDesktopWidget().availableGeometry().center()
        # 框架的中心与桌面中心对齐
        qr.moveCenter(cp)
        # 自身窗体的左上角与框架的左上角对齐
        self.move(qr.topLeft())

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'PyQt5应用教程（snmplink编著）',
                                     "是否要退出应用程序？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = CMainWindow()
    sys.exit(app.exec_())
