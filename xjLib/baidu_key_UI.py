# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-21 14:40:30
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-11 13:27:31
'''
import os

from PyQt5.QtCore import QMetaObject, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
                             QDesktopWidget, QHBoxLayout, QHeaderView, QLabel,
                             QMainWindow, QProgressBar, QSpinBox, QStatusBar,
                             QTableWidget, QVBoxLayout, QWidget, qApp)


class Ui_MainWindow(object):
    '''标准windows窗口'''

    def setupUi(self, MainWindow):
        # #标题、图标、状态栏、进度条
        _path = os.path.dirname(__file__) + '/'
        self.setWindowIcon(QIcon(_path + 'ico/ico.ico'))
        self.setWindowTitle('百度关键字检索')
        # #状态栏、进度条
        self.statusBar = self.statusBar()
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Ready to compose')
        self.pbar = QProgressBar()
        self.setStyleSheet(
            "QProgressBar{border: 1px solid grey;text-align: center;font:bold 8pt 微软雅黑}"
            "QLabel{color:rgb(100,100,250);font:bold 10pt 微软雅黑;}"
            "QPushButton{background-color:rgb(22,36,92);color:white;width:100%;height:35%;border-radius:10px;border:2px groove gray;border-style:outset;font:bold 10pt 微软雅黑;}"
            "QPushButton:hover{background-color:rgb(248,242,220);color: black;}"
            "QPushButton:pressed{background-color:rgb(163,159,147);border-style:inset;}"
            "QLineEdit{width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 11pt 等线;}"
        )
        '''
        self.pbar.setStyleSheet("QProgressBar{border: 1px solid grey;border-radius: 5px;text-align: center;font:bold 8pt 微软雅黑}"
                                "QProgressBar::chunk{background-color: #CD96CD;width: 10px;margin: 0.5px;}")# 斑马线,色条

        # self.pbar.setInvertedAppearance(True) # 逆序
        # self.pbar.setOrientation(Qt.Vertical) #垂直
        '''
        self.label = QLabel("进度： ")
        self.statusBar.addPermanentWidget(self.status_bar, stretch=85)
        self.statusBar.addPermanentWidget(self.label, stretch=25)
        self.statusBar.addPermanentWidget(self.pbar, stretch=100)
        self.status_bar.setStyleSheet(
            "background-color:DarkSeaGreen;color:Navy;font:bold 10pt 微软雅黑")
        # #菜单栏
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 全平台一致的效果
        self.file_menu = menubar.addMenu('File')
        # #工具栏
        self.file_toolbar = self.addToolBar('File')
        self.file_toolbar.setToolButtonStyle(3)  # @同时显示文字和图标
        self.file_toolbar.setStyleSheet("QToolBar{spacing: 8px;}")
        self.file_toolbar.setFixedHeight(64)
        # #QAction
        # _path = os.path.dirname(__file__) + '/'
        self.open_action = QAction(QIcon(_path + 'ico/open.ico'), 'Open', self)
        self.save_action = QAction(QIcon(_path + 'ico/save.ico'), 'Save', self)
        self.run_action = QAction(QIcon(_path + 'ico/run.ico'), 'Run', self)
        self.open_action.setObjectName("openObject")  # !必须,关键，用于自动绑定信号和函数
        self.save_action.setObjectName("saveObject")  # !必须,关键，用于自动绑定信号和函数
        self.run_action.setObjectName("runObject")  # !必须,关键，用于自动绑定信号和函数
        self.close_action = QAction(
            QIcon(_path + 'ico/close.ico'), 'Close', self)
        # #窗口大小位置
        (_weith, _height) = (760, 540)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(_weith, _height)
        self.setGeometry(
            int((screen.width() - _weith) / 2),
            int((screen.height() - _height) / 2), _weith, _height)

        self.creatkeysTable()  # 创建关键字表格
        self.creatresultTable()  # 创建搜索结果表格
        self.retranslateUi()  # 关联转化空间名字
        QMetaObject.connectSlotsByName(MainWindow)  # @  关键，用于自动绑定信号和函数
        self.show()
        pass

    def creatkeysTable(self):
        # #列表
        self.keysTable = QTableWidget(0, 1)  # 列示keys
        # self.keysTable.setShowGrid(True)
        self.keysTable.setStyleSheet("selection-background-color:pink")
        self.keysTable.setHorizontalHeaderLabels([
            '关键字',
        ])
        self.keysTable.horizontalHeader().setStyleSheet(
            "QHeaderView::section{background-color:CadetBlue;color:LemonChiffon;font:bold 10pt 微软雅黑}"
        )
        self.keysTable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # 将表格设置为禁止编辑
        self.keysTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.keysTable.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # 选中整行
        QTableWidget.resizeColumnsToContents(
            self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(
            self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        self.keysTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.keysTable.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def creatresultTable(self):
        # #列表2
        self.resultTable = QTableWidget(0, 5)  # 列示texts
        # self.resultTable.setShowGrid(True)
        # self.tableWidget.setColumnCount(5)
        self.resultTable.setHorizontalHeaderLabels(
            ['关键字', '页码', '序号', '标题', '网址'])
        self.resultTable.horizontalHeader().setStyleSheet(
            "QHeaderView::section{background:CornflowerBlue;color:LemonChiffon; font:bold 10pt 微软雅黑}"
        )
        self.resultTable.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # 将表格设置为禁止编辑
        # self.resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.resultTable.horizontalHeader().setResizeContentsPrecision(
            QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.resultTable.horizontalHeader().setStretchLastSection(
            True)  # 设置最后一列自动填充表格
        self.resultTable.setSelectionBehavior(
            QAbstractItemView.SelectRows)  # 选中整行
        QTableWidget.resizeColumnsToContents(
            self.resultTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(
            self.resultTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        self.resultTable.setColumnWidth(0, 100)
        self.resultTable.setColumnWidth(1, 40)
        self.resultTable.setColumnWidth(2, 40)
        self.resultTable.setColumnWidth(3, 200)
        self.resultTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resultTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.resultTable.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

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
        self.lb1.setFont(QFont('微软雅黑', 12, QFont.Bold))
        self.file_toolbar.addWidget(self.lb1)
        self.lineEdit = QSpinBox()
        self.lineEdit.setRange(1, 200)
        self.lineEdit.setAlignment(Qt.AlignCenter)
        self.lineEdit.setStyleSheet(
            "width:50px ;height:30%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 10pt 微软雅黑"
        )
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
        self.open_action.setFont(QFont('微软雅黑', 9, QFont.Bold))
        self.save_action.setFont(QFont('微软雅黑', 9, QFont.Bold))
        self.run_action.setFont(QFont('微软雅黑', 9, QFont.Bold))
        self.close_action.setFont(QFont('微软雅黑', 9, QFont.Bold))
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(qApp.quit)


if __name__ == "__main__":

    class MyWindow(QMainWindow, Ui_MainWindow):

        def __init__(self, parent=None):
            super(MyWindow, self).__init__(parent)
            self.setupUi(self)

    import sys
    app = QApplication(sys.argv)

    w = MyWindow()
    sys.exit(app.exec_())
