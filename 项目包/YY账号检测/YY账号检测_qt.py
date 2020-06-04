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
#LastEditTime : 2020-06-04 13:53:22
'''
from xt_Requests import parse_get
from xt_Log import log
from pyquery import PyQuery
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed  # 线程池模块

import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    '''标准windows窗口'''

    def setupUi(self, MainWindow):
        # #标题、图标、状态栏、进度条
        _path = os.path.dirname(__file__) + '/'
        self.setWindowIcon(QIcon(_path + 'ico/ico.ico'))
        self.setWindowTitle('YY账号检测')
        # #状态栏、进度条
        self.statusBar = self.statusBar()
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Ready to compose')
        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("QProgressBar{border: 1px solid grey;text-align: center;font:bold 8pt 微软雅黑}")
        self.label = QLabel("进度： ")
        self.statusBar.addPermanentWidget(self.status_bar, stretch=85)
        self.statusBar.addPermanentWidget(self.label, stretch=25)
        self.statusBar.addPermanentWidget(self.pbar, stretch=100)
        self.status_bar.setStyleSheet("background-color:DarkSeaGreen;color:Navy;font:bold 10pt 微软雅黑")
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
        _path = os.path.dirname(__file__) + '/'
        self.open_action = QAction(QIcon(_path + 'ico/open.ico'), '导入', self)
        self.save_action = QAction(QIcon(_path + 'ico/save.ico'), '保存', self)
        self.run_action = QAction(QIcon(_path + 'ico/run.ico'), '检测', self)
        self.open_action.setObjectName("openObject")  # @必须,关键，用于自动绑定信号和函数
        self.save_action.setObjectName("saveObject")  # @必须,关键，用于自动绑定信号和函数
        self.run_action.setObjectName("runObject")  # @必须,关键，用于自动绑定信号和函数
        self.close_action = QAction(QIcon(_path + 'ico/close.ico'), 'Close', self)
        # #窗口大小位置
        (_weith, _height) = (760, 540)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(_weith, _height)
        self.setGeometry((screen.width() - _weith) / 2,
                         (screen.height() - _height) / 2, _weith, _height)

        self.retranslateUi()  # 这个函数用于关联转化空间名字
        QMetaObject.connectSlotsByName(MainWindow)  # @  关键，用于自动绑定信号和函数
        self.show()
        pass

    def retranslateUi(self):
        # #列表
        self.keysTable = QTableWidget(0, 3)  # 列示keys
        # self.keysTable.setShowGrid(True)
        self.keysTable.setStyleSheet("selection-background-color:pink")
        self.keysTable.setHorizontalHeaderLabels(['账号', '密码', '状态'])
        self.keysTable.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:CadetBlue;color:LemonChiffon;font:bold 10pt 微软雅黑}")
        self.keysTable.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格设置为禁止编辑
        self.keysTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格头为伸缩模式
        self.keysTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选中整行
        QTableWidget.resizeColumnsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        QTableWidget.resizeRowsToContents(self.keysTable)  # 将行与列的宽度高度与文本内容的宽高相匹配
        self.keysTable.setColumnWidth(0, 100)
        self.keysTable.setColumnWidth(1, 100)
        self.keysTable.setColumnWidth(2, 40)
        self.keysTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.keysTable.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # #设置窗口布局
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.keysTable)
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
        self.file_toolbar.addAction(self.run_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.save_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addAction(self.close_action)
        self.file_toolbar.addSeparator()  # 分隔线

        self.open_action.setShortcut('Ctrl+O')
        self.save_action.setShortcut('Ctrl+S')
        self.run_action.setShortcut('Ctrl+R')
        self.open_action.setFont(QFont('微软雅黑', 9))
        self.save_action.setFont(QFont('微软雅黑', 9))
        self.run_action.setFont(QFont('微软雅黑', 9))
        self.close_action.setFont(QFont('微软雅黑', 9))
        self.close_action.setShortcut('Ctrl+Q')
        self.close_action.setToolTip('Close the window')
        self.close_action.setStatusTip('Close the window')
        self.close_action.triggered.connect(qApp.quit)


class MyWindow(QMainWindow, Ui_MainWindow):
    _signal = pyqtSignal(list)
    _step = pyqtSignal()

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # #自用变量
        self.keys = []  # 账号信息
        self.step = 0
        self._step.connect(self.step_valueChanged)
        self._signal.connect(self.update)

    def step_valueChanged(self):
        self.pbar.setValue(int(self.step))
        pass

    def update(self, _res):
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        QApplication.setOverrideCursor(Qt.WaitCursor)  # 显示等待中的鼠标样式
        '''for item in _res:
            RowCont = self.resultTable.rowCount()
            self.resultTable.insertRow(RowCont)
            self.resultTable.setItem(RowCont, 0, QTableWidgetItem(item[0]))
            self.resultTable.setItem(RowCont, 1, QTableWidgetItem(str(item[1])))
            self.resultTable.setItem(RowCont, 2, QTableWidgetItem(str(item[2])))
            self.resultTable.setItem(RowCont, 3, QTableWidgetItem(item[3]))
            self.resultTable.setItem(RowCont, 4, QTableWidgetItem(item[4]))
            self.resultTable.scrollToBottom()  # 滚动到最下'''
        qApp.processEvents()  # 交还控制权
        QApplication.restoreOverrideCursor()  # 恢复鼠标样式

    @pyqtSlot()
    def on_openObject_triggered(self):
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')

        if filename:
            [self.keysTable.removeRow(0) for _ in range(self.keysTable.rowCount())]
            self.status_bar.showMessage('导入关键字......')
            self._name = filename.split('.')[0:-1][0]  # 文件名，含完整路径，去掉后缀

            _k = []
            with open(filename) as myFile:
                # for row in myFile.readlines():
                for row in myFile:
                    row = row.strip()  # 默认删除空白符
                    if len(row) == 0:
                        continue  # len为0的行,跳出本次循环
                    _k.append(row.split('\t'))

            self.keys = _k

            self.step = 0
            _max = len(self.keys)
            self.pbar.setMaximum(_max)
            self._step.emit()  # 传递更新进度条信号
            # 写入QTableWidget
            for item in self.keys:
                RowCont = self.keysTable.rowCount()
                self.keysTable.insertRow(RowCont)
                self.keysTable.setItem(RowCont, 0, QTableWidgetItem(item[0]))
                self.keysTable.setItem(RowCont, 1, QTableWidgetItem(item[1]))
                self.keysTable.setItem(RowCont, 2, QTableWidgetItem('未检测'))
                self.keysTable.scrollToBottom()  # 滚动到最下面
                self.step += 1
                self.label.setText("进度：{}/{} ".format(self.step, _max))
                self._step.emit()  # 传递更新进度条信号
        self.status_bar.showMessage('导入关键字完毕!')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)

    @pyqtSlot()
    def on_runObject_triggered(self):
        if len(self.keys) == 0:
            self.status_bar.showMessage('没有导入账号信息！！！')
            return
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        # @检测

        QApplication.processEvents(QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        # 等待到所有线程结束
        for obj in as_completed(future_tasks):
            _res = obj.result()
            self.step += 1
            self._step.emit()  # 传递更新进度条信号
            self.label.setText("进度：{}/{}".format(self.step, _max))
            if len(_res) == 0:
                continue
            self.texts.append(_res)
            self._signal.emit(_res)  # 传递更新进度条信号
        self.status_bar.showMessage('检测YY账号密码完毕')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)
        QApplication.restoreOverrideCursor()  # 恢复鼠标样式

    def getkeys(self, target):
        QApplication.processEvents()
        return time.sleep(0.02)

    @pyqtSlot()
    def on_saveObject_triggered(self):
        _filename = QFileDialog.getSaveFileName(self, r'创建txt并保存', r'./', r'文本文件(*.txt);')[0]
        with open(_filename, 'w', encoding='utf-8') as myFile:
            myFile.write('账号\t密码\t状态\t\n')
            for currentRow in range(self.keysTable.rowCount()):
                for currentColumn in range(self.keysTable.columnCount()):
                    try:
                        teext = self.keysTable.item(currentRow, currentColumn).text()
                        myFile.write(teext + '\t')
                    except AttributeError:
                        pass
                myFile.write('\n')

        self.status_bar.showMessage('[' + _filename + ']保存完成。')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)


if __name__ == "__main__":
    log = log()
    app = QApplication(sys.argv)
    w = MyWindow()
    sys.exit(app.exec_())
