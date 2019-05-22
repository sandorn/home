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
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 18:44:03
'''
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor  # 线程池模块
from concurrent.futures import as_completed

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import main


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urls = []  # url_list
        self._name = ''  # 文件名
        self.texts = []  # 用于存放结果
        self.step = 0
        self.initUI()
        self.menu_init()
        self.toolbar_init()
        self.action_init()
        self.show()
        pass

    def initUI(self):
        _path = os.path.dirname(__file__) + '/'
        self.ready = False
        self.setWindowIcon(QIcon(_path + 'ico/ico.ico'))
        self.setWindowTitle('百度关键字检索')
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready to compose')
        self.pbar = QProgressBar(self)
        self.pbar.setMaximum(100)
        self.pbar.setMinimum(0)
        self.pbar.setValue(self.step)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # 全平台一致的效果
        self.file_menu = menubar.addMenu('File')
        self.file_toolbar = self.addToolBar('File')
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.run_action = QAction('Run', self)
        self.close_action = QAction('Close', self)
        # 窗口大小位置
        (_weith, _height) = (1080, 720)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(_weith, _height)
        self.setGeometry((screen.width() - _weith) / 2,
                         (screen.height() - _height) / 2, _weith, _height)

        self.keysTable = QTableWidget(0, 1)  # 存放keys
        self.keysTable.setStyleSheet("selection-background-color:pink")
        self.keysTable.setHorizontalHeaderLabels(['关键字', ])
        self.keysTable.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: green;color: yellow; font: 12pt '微软雅黑'}")
        self.keysTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格设置为禁止编辑
        self.keysTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.keysTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        QTableWidget.resizeColumnsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        self.keysTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.resultTable = QTableWidget(0, 5)  # 显示texts
        # self.tableWidget.setColumnCount(5)
        self.resultTable.setHorizontalHeaderLabels(['关键字', '页码', '序号', '标题', '网址'])
        self.resultTable.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: blue;color: yellow; font: 12pt '微软雅黑'}")
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格设置为禁止编辑
        # self.resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.resultTable.horizontalHeader().setStretchLastSection(True)  # 关键
        self.resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        QTableWidget.resizeColumnsToContents(self.resultTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(self.resultTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        self.resultTable.setColumnWidth(0, 100)
        self.resultTable.setColumnWidth(1, 40)
        self.resultTable.setColumnWidth(2, 40)
        self.resultTable.setColumnWidth(3, 200)
        self.resultTable.setContextMenuPolicy(Qt.CustomContextMenu)
        self.resultTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # 设置窗口的布局
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
        vlayout.addWidget(self.pbar)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def menu_init(self):
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.run_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)

    def toolbar_init(self):
        self.file_toolbar.addAction(self.open_action)
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addSeparator()  # 分隔线
        self.lb1 = QLabel('输入要搜索的页数：', self)
        self.file_toolbar.addWidget(self.lb1)
        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText('只能是数字')
        # 实例化整型验证器，并设置范围为1-99
        pIntvalidator = QIntValidator(self)
        pIntvalidator.setRange(1, 99)
        self.lineEdit.setValidator(pIntvalidator)
        # 设置文本水平方向居中对齐
        # self.lineEdit.setAlignment(Qt.AlignCenter)  #会影响提示显示
        # 设置文本的字体和字号大小  self.lineEdit.setFont(QFont('Arial', 12))
        self.file_toolbar.addWidget(self.lineEdit)
        self.file_toolbar.addAction(self.run_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addSeparator()
        self.file_toolbar.addAction(self.close_action)

    def action_init(self):
        _path = os.path.dirname(__file__) + '/'

        self.open_action.setIcon(QIcon(_path + 'ico/open.ico'))
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.setToolTip('Open an text file')
        self.open_action.setStatusTip('Open an text file')
        self.open_action.triggered.connect(self.open_func)

        self.save_action.setIcon(QIcon(_path + 'ico/save.ico'))
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setToolTip('Save the file')
        self.save_action.setStatusTip('Save the file')
        self.save_action.triggered.connect(self.save_func)

        self.run_action.setIcon(QIcon(_path + 'ico/run.jpg'))
        self.run_action.setShortcut('Ctrl+R')
        self.run_action.setToolTip('Serch the keys')
        self.run_action.setStatusTip('Serch the keys')
        self.run_action.triggered.connect(self.run_func)

        self.close_action.setIcon(QIcon(_path + 'ico/close.ico'))
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(qApp.quit)

    def __del__(self):
        qApp.quit()

    def open_func(self):
        self.keysTable.setRowCount(0)
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if filename:
            self._name = filename.split('.')[0:-1][0]  # 文件名，含完整路径，去掉后缀
            self.keys = main.make_keys(filename, 10)
            # 写入QTableWidget
            for item in self.keys:
                RowCont = self.keysTable.rowCount()
                self.keysTable.insertRow(RowCont)
                self.keysTable.setItem(RowCont, 0, QTableWidgetItem(item))
            self.ready = True
            self.status_bar.showMessage('获取关键字完毕')

    def run_func(self):
        self.pbar.setValue(0)
        self.resultTable.setRowCount(0)
        if not self.ready:
            return

        if self.lineEdit.text() == '':
            pages = 1
            self.lineEdit.setText('1')
        else:
            pages = int(self.lineEdit.text())

        self.urls = [(key, page, "https://www.baidu.com/s?wd={}&pn={}".format(key, page * 10)) for key in self.keys for page in range(pages)]

        with ThreadPoolExecutor(20) as p:
            future_tasks = [p.submit(main.getkeys, url) for url in self.urls]
        self.pbar.setMaximum(len(future_tasks))
        for obj in as_completed(future_tasks):
            if obj.done():
                try:
                    res = obj.result()
                    QApplication.processEvents()
                    self.step += 1
                    self.pbar.setValue(int(self.step))
                    if len(res) != 0:
                        self.texts.append(res)
                except Exception as e:
                    print("obj.result()error:", e)

        # 写入QTableWidget
        self.texts.sort()
        for index, lists_line in enumerate(self.texts):
            for item in lists_line:
                RowCont = self.resultTable.rowCount()
                self.resultTable.insertRow(RowCont)
                self.resultTable.setItem(RowCont, 0, QTableWidgetItem(item[0]))
                self.resultTable.setItem(RowCont, 1, QTableWidgetItem(str(item[1])))
                self.resultTable.setItem(RowCont, 2, QTableWidgetItem(str(item[2])))
                self.resultTable.setItem(RowCont, 3, QTableWidgetItem(item[3]))
                self.resultTable.setItem(RowCont, 4, QTableWidgetItem(item[4]))
        self.status_bar.showMessage('抓取百度检索信息完毕')

    def save_func(self):
        main.savefile(self._name + '_百度词频.txt', self.texts)
        self.status_bar.showMessage("threadPool cost all time: %s 秒" % (time.time() - start))


if __name__ == "__main__":
    start = time.time()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
