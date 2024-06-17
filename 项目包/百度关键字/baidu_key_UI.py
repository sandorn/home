# !/usr/bin/env python
"""
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-21 14:40:30
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-13 11:44:34
"""

import os

from PyQt6.QtCore import QMetaObject, Qt
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QProgressBar, QSpinBox, QStatusBar, QTableWidget, QVBoxLayout, QWidget
from xt_Ui.part import xt_QTableWidget


class Ui_MainWindow(QMainWindow):
    """标准windows窗口"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        # #标题、图标、状态栏、进度条
        self.resize(1024, 768)
        _path = os.path.dirname(__file__) + '/'
        self.setWindowIcon(QIcon(_path + 'ico/ico.ico'))
        self.setWindowTitle('百度关键字检索')
        # #状态栏、进度条
        self.statusBar = self.statusBar()
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Ready to compose')
        self.pbar = QProgressBar()
        self.setStyleSheet(
            'QProgressBar{border: 1px solid grey;text-align: center;font:bold 8pt 微软雅黑}'
            'QLabel{color:rgb(100,100,250);font:bold 10pt 微软雅黑;}'
            'QPushButton{background-color:rgb(22,36,92);color:white;width:100%;height:35%;border-radius:10px;border:2px groove gray;border-style:outset;font:bold 10pt 微软雅黑;}'
            'QPushButton:hover{background-color:rgb(248,242,220);color: black;}'
            'QPushButton:pressed{background-color:rgb(163,159,147);border-style:inset;}'
            'QLineEdit{width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 11pt 等线;}'
        )

        self.label = QLabel('进度： ')
        self.statusBar.addPermanentWidget(self.status_bar, stretch=85)
        self.statusBar.addPermanentWidget(self.label, stretch=25)
        self.statusBar.addPermanentWidget(self.pbar, stretch=100)
        self.status_bar.setStyleSheet('background-color:DarkSeaGreen;color:Navy;font:bold 10pt 微软雅黑')
        # #菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 全平台一致的效果
        self.file_menu = menubar.addMenu('File')
        # #工具栏
        self.file_toolbar = self.addToolBar('File')
        # self.file_toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # @同时显示文字和图标
        self.file_toolbar.setStyleSheet('QToolBar{spacing: 8px;}')
        self.file_toolbar.setFixedHeight(64)
        # #QAction
        # _path = os.path.dirname(__file__) + '/'
        self.open_action = QAction(QIcon(_path + 'ico/open.ico'), 'Open', self)
        self.save_action = QAction(QIcon(_path + 'ico/save.ico'), 'Save', self)
        self.run_action = QAction(QIcon(_path + 'ico/run.ico'), 'Run', self)
        self.open_action.setObjectName('openObject')  # !必须,关键，用于自动绑定信号和函数
        self.save_action.setObjectName('saveObject')  # !必须,关键，用于自动绑定信号和函数
        self.run_action.setObjectName('runObject')  # !必须,关键，用于自动绑定信号和函数
        self.close_action = QAction(QIcon(_path + 'ico/close.ico'), 'Close', self)

        self.creatkeysTable()  # 创建关键字表格
        self.creatresultTable()  # 创建搜索结果表格
        self.retranslateUi()  # 关联转化空间名字
        QMetaObject.connectSlotsByName(MainWindow)  # @  关键，用于自动绑定信号和函数
        self.show()

    def creatkeysTable(self):
        # #列表
        self.keysTable = xt_QTableWidget([0, 1])  # 列示keys
        self.keysTable.setStyleSheet('selection-background-color:pink')
        self.keysTable.setHorizontalHeaderLabels(
            [
                '关键字',
            ]
        )
        self.keysTable.horizontalHeader().setStyleSheet('QHeaderView::section{background-color:CadetBlue;color:LemonChiffon;font:bold 10pt 微软雅黑}')
        QTableWidget.resizeColumnsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配

    def creatresultTable(self):
        # #列表2
        self.resultTable = xt_QTableWidget([0, 5])  # 列示texts
        # self.resultTable.setShowGrid(True)
        # self.tableWidget.setColumnCount(5)
        self.resultTable.setHorizontalHeaderLabels(['关键字', '页码', '序号', '标题', '网址'])
        self.resultTable.setColumnWidth(0, 100)
        self.resultTable.setColumnWidth(1, 40)
        self.resultTable.setColumnWidth(2, 40)
        self.resultTable.setColumnWidth(3, 200)

    def retranslateUi(self):
        # #设置窗口布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.keysTable)
        # hlayout.addStretch(1) #插入缩放缝隙
        hlayout.addWidget(self.resultTable)
        # hlayout各控件的比例
        hlayout.setStretchFactor(self.keysTable, 1)
        hlayout.setStretchFactor(self.resultTable, 3)
        # hlayout.setSpacing(2)  # 设置控件间距
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        # #menu_init(self):
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.run_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)
        # #toolbar_init(self):
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.lb1 = QLabel(' 搜索页数：', self)
        self.lb1.setFont(QFont('微软雅黑', 12, weight=1))
        self.file_toolbar.addWidget(self.lb1)
        self.lineEdit = QSpinBox()
        self.lineEdit.setRange(1, 200)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setStyleSheet('width:50px ;height:30%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 10pt 微软雅黑')
        self.file_toolbar.addWidget(self.lineEdit)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.run_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.close_action)
        self.file_toolbar.addSeparator()  # 分隔线

        self.open_action.setShortcut('Ctrl+O')
        self.save_action.setShortcut('Ctrl+S')
        self.run_action.setShortcut('Ctrl+R')
        self.open_action.setFont(QFont('微软雅黑', 9, weight=1))
        self.save_action.setFont(QFont('微软雅黑', 9, weight=1))
        self.run_action.setFont(QFont('微软雅黑', 9, weight=1))
        self.close_action.setFont(QFont('微软雅黑', 9, weight=1))
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(QApplication.quit)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    w = Ui_MainWindow()
    sys.exit(app.exec())
