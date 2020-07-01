# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-30 15:56:32
#FilePath     : /项目包/百度关键字/UI单一完整文件.py
#LastEditTime : 2020-06-30 15:59:05
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import os
import sys
import time
from urllib.parse import unquote

import requests
from PyQt5.QtCore import QEventLoop, QMetaObject, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
                             QDesktopWidget, QFileDialog, QHBoxLayout,
                             QHeaderView, QLabel, QMainWindow, QProgressBar,
                             QSpinBox, QStatusBar, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget, qApp)

from xt_Ahttp import ahttpGetAll


def savefile(_filename, _list_texts, br=''):
    '''
    函数说明:将多层次的list 或 tupl写入文件,迭代多层
    br为元素结束标志，可以用'\t'  '\n'  等
    '''
    if not isinstance(_list_texts, (list, tuple)):
        return

    with open(_filename, 'w', encoding='utf-8') as file:
        file.write(_filename + '\n')

        def each(data):
            for index, value in enumerate(data):
                if isinstance(value, (list, tuple)):
                    each(value)
                else:
                    file.write(str(value) + br)

            # # 最后一个元素已处理完毕，添加换行
            file.write('\n')

        each(_list_texts)

    print(f'[{_filename}]保存完成。')


def parse_get(url, *args, **kwargs):
    attempts = 0
    response = None
    elapsed = 0

    while attempts < 6:
        try:
            response = requests.get(url, *args, **kwargs)
            response.raise_for_status()
            # $ assert response.status_code in [200, 201, 302]
        except Exception as err:
            attempts += 1
            print(
                f'parse_get:<{url}>; {attempts} times; Err:{repr(err)}; total_seconds:{response.elapsed.total_seconds()}'
            )
        else:
            # #返回正确结果
            new_res = response
            return new_res
    # #返回非正确结果
    new_res = response
    return new_res


class Ui_MainWindow(QMainWindow):
    '''标准windows窗口'''
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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
        self.close_action = QAction(QIcon(_path + 'ico/close.ico'), 'Close',
                                    self)
        # #窗口大小位置
        (_weith, _height) = (760, 540)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(_weith, _height)
        self.setGeometry(int((screen.width() - _weith) / 2),
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


class MyWindow(Ui_MainWindow):
    _signal = pyqtSignal(list)
    _step = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.keys = []  # 关键字
        self.urls = []  # url_list
        self._name = ''  # 文件名
        self.texts = []  # 用于存放结果
        self.step = 0
        self._step.connect(self.step_valueChanged)
        self._signal.connect(self.update)

    def step_valueChanged(self):
        self.pbar.setValue(int(self.step))
        self.label.setText("进度：{}/{}".format(self.step, self.pbar.maximum()))
        pass

    def update(self, item):
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        QApplication.setOverrideCursor(Qt.WaitCursor)  # 显示等待中的鼠标样式

        RowCont = self.resultTable.rowCount()
        self.resultTable.insertRow(RowCont)
        self.resultTable.setItem(RowCont, 0, QTableWidgetItem(item[0]))
        self.resultTable.setItem(RowCont, 1, QTableWidgetItem(str(item[1])))
        self.resultTable.setItem(RowCont, 2, QTableWidgetItem(str(item[2])))
        self.resultTable.setItem(RowCont, 3, QTableWidgetItem(item[3]))
        self.resultTable.setItem(RowCont, 4, QTableWidgetItem(item[4]))
        self.resultTable.scrollToBottom()  # 滚动到最下
        qApp.processEvents()  # 交还控制权

        QApplication.restoreOverrideCursor()  # 恢复鼠标样式

    @pyqtSlot()
    def on_openObject_triggered(self):
        # #打开关键字文件并导入
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file')

        if filename:
            [
                self.keysTable.removeRow(0)
                for _ in range(self.keysTable.rowCount())
            ]
            self.status_bar.showMessage('导入关键字......')
            self._name = filename.split('.')[0:-1][0]  # 文件名，含完整路径，去掉后缀

            with open(filename) as myFile:
                # @名称排序且去重去空
                self.keys = sorted(
                    set([row.strip() for row in myFile if row.strip()]))

            # 写入QTableWidget
            for item in self.keys:
                RowCont = self.keysTable.rowCount()
                self.keysTable.insertRow(RowCont)
                self.keysTable.setItem(RowCont, 0, QTableWidgetItem(item))
                self.keysTable.scrollToBottom()  # 滚动到最下面
        self.status_bar.showMessage('导入关键字完毕!')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)

    @pyqtSlot()
    def on_runObject_triggered(self):
        if len(self.keys) == 0:
            self.status_bar.showMessage('没有导入关键字！！！')
            return
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        self.resultTable.clearContents()
        self.resultTable.setRowCount(0)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        # 构建urls
        pages = self.lineEdit.value()

        self.urls = [
            f"https://www.baidu.com/s?wd={key}&pn={page * 10}"
            for key in self.keys for page in range(pages)
        ]

        self.status_bar.showMessage('抓取百度检索信息......')

        self.texts = []  # #清空结果库
        resp_list = ahttpGetAll(self.urls, pool=200)
        self.getdatas(resp_list)
        self.texts.sort(key=lambda x: x[0])  # #排序

        self.status_bar.showMessage('抓取百度检索信息完毕')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)
        QApplication.restoreOverrideCursor()  # 恢复鼠标样式

    # ! 多线程运行，as_completed 等待各子线程结束，将各子线程运行结果返回给主线程
    # ! 子线程全部启动后，在逐一退出时会有卡顿

    def getdatas(self, resp_list):
        _max = len(resp_list)
        self.step = 0
        self.pbar.setMaximum(_max)
        self._step.emit()  # 传递更新进度条信号
        self.label.setText("进度：{}/{}".format(self.step, _max))
        for response in resp_list:
            url = str(response.url)
            key = unquote(
                url.split("?")[1].split("&")[0].split('=')[1]).replace(
                    '+', ' ')
            pages = url.split("?")[1].split("&")[1].split('=')[1]

            搜索结果 = response.element.xpath("//h3/a")
            for index, each in enumerate(搜索结果):
                # #获取显示字符和网页链接
                href = each.xpath("@href")[0]
                title = each.xpath("string(.)").strip()
                # # 剔除百度自营内容
                if '百度' in title or not href.startswith(
                        'http') or href.startswith(
                            "http://www.baidu.com/baidu.php?"):
                    continue

                # #获取真实网址
                real_url = parse_get(
                    href, allow_redirects=False).headers['Location']  # 网页原始地址
                if real_url.startswith(
                        'http') and '.baidu.com' not in real_url:
                    _item = [key, pages, index, title, real_url]
                    self._signal.emit(_item)  # 传递更新结果数据表信号
                    self.texts.append(_item)
            self.step += 1
            self._step.emit()  # 传递更新进度条信号
            self.label.setText("进度：{}/{}".format(self.step, _max))

        QApplication.processEvents()
        time.sleep(0.02)

    @pyqtSlot()
    def on_saveObject_triggered(self):
        if len(self.texts) == 0:
            self.status_bar.showMessage('没有发现需要保存的内容！！！')
            return
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        savefile(self._name + '_百度词频.txt', self.texts, br='\t')
        self.texts = []
        self.status_bar.showMessage(f'[{self._name}_百度词频.txt]保存完成。')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = MyWindow()
    sys.exit(app.exec_())
