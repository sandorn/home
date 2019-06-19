# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-18 15:28:01
@LastEditors: Even.Sand
@LastEditTime: 2019-06-19 20:00:34
'''

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Ui_MainWindow(object):
    '''标准windows窗口'''

    def setupUi(self, MainWindow):
        # #状态栏、进度条
        self.statusBar = self.statusBar()
        # #工具栏
        self.file_toolbar = self.addToolBar('File')
        self.l1 = QLabel("账号：")
        self.l1.setFont(QFont('微软雅黑', 10))
        self.user = QLineEdit(self)
        self.l2 = QLabel("密码：")
        self.l2.setFont(QFont('微软雅黑', 10))
        self.pwd = QLineEdit(self)

        self.zoom_in_btn = QPushButton('Zoom In', self)
        self.reload_btn = QPushButton('Zoom 1:1', self)
        self.zoom_out_btn = QPushButton('Zoom Out', self)
        self.login_btn = QPushButton('Login', self)
        self.fliter_btn = QPushButton('Fliter', self)
        self.buy_btn = QPushButton('BuyNow', self)
        self.close_action = QPushButton('Close', self)

        # #窗口大小位置
        (_weith, _height) = (960, 720)
        screen = QDesktopWidget().screenGeometry()
        self.setMinimumSize(_weith, _height)
        self.setGeometry((screen.width() - _weith) / 2,
                         (screen.height() - _height) / 2, _weith, _height)

        self.browser = QWebEngineView()

        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/ico/ico.ico'))
        self.setWindowTitle('网易藏宝阁助手')
        self.btn_init()
        self.toolbar_init()
        self.Layout_init()
        self.browser_init()
        # 这个函数用于关联转化空间名字
        QMetaObject.connectSlotsByName(MainWindow)  # @  关键，用于自动绑定信号和函数

    def browser_init(self):
        self.browser.load(QUrl('https://my.cbg.163.com'))
        #self.browser.urlChanged.connect(lambda: self.url_le.setText(self.browser.url().toDisplayString()))
        self.browser.loadFinished.connect(lambda: self.statusBar.showMessage(
            self.browser.title() + '加载完毕！'))
        self.show()

    def btnUI(self, btn, ico, sht=None, msg=None, name=None):
        _path = os.path.dirname(__file__) + '/'
        btn.setIcon(QIcon(_path + ico))
        #btn.setIconSize(QSize(24, 24))
        #btn.setFont(QFont('微软雅黑', 10))
        #btn.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset")
        btn.setStyleSheet("QPushButton{background-color:black;color: white;width:100% ;height:35%;border-radius: 10px;  border: 2px groove gray;border-style: outset;font: bold 10pt 微软雅黑}""QPushButton:hover{background-color:white; color: black;}""QPushButton:pressed{background-color:rgb(85, 170, 255);border-style: inset;}")
        if sht:
            btn.setShortcut(sht)
        if msg:
            btn.setToolTip(msg)
            btn.setStatusTip(msg)
        if name:
            btn.setObjectName(name)  # @用于自动绑定信号和函数

    def btn_init(self):
        self.btnUI(self.zoom_in_btn, 'ico/1075665.png', 'Ctrl+=',
                   '放大页面\tCtrl+=')
        self.btnUI(self.reload_btn, 'ico/1075664.png', 'Ctrl+0', '复原页面\tCtrl+0')
        self.btnUI(self.zoom_out_btn, 'ico/1075667.png', 'Ctrl+-',
                   '缩小页面\tCtrl+-')
        self.zoom_in_btn.clicked.connect(lambda: self.browser.setZoomFactor(
            self.browser.zoomFactor() + 0.1))
        self.reload_btn.clicked.connect(lambda: self.browser.setZoomFactor(1))
        self.zoom_out_btn.clicked.connect(lambda: self.browser.setZoomFactor(
            self.browser.zoomFactor() - 0.1))

        self.btnUI(self.login_btn, 'ico/1142198.png', 'Ctrl+L',
                   '登陆交易账号\tCtrl+L', "login_O")
        self.btnUI(self.fliter_btn, 'ico/583565.png', 'Ctrl+R', '筛选账号\tCtrl+R',
                   "fliter_O")
        self.btnUI(self.buy_btn, 'ico/1142184.png', 'Ctrl+B', '购买账号\tCtrl+B',
                   "buy_O")
        self.btnUI(self.close_action, 'ico/1186301.png', 'Ctrl+Q',
                   'Close the window')
        self.close_action.clicked.connect(QApplication.quit)

    def toolbar_init(self):
        self.user.setStyleSheet(
            "width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 9pt 等线"
        )
        self.pwd.setStyleSheet(
            "width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 9pt 等线"
        )

        self.file_toolbar.setOrientation(Qt.Vertical)
        self.file_toolbar.setToolButtonStyle(2)  # @左右同时显示文字和图标，3为上下
        self.file_toolbar.setFixedWidth(160)

        self.file_toolbar.addWidget(self.l1)
        self.file_toolbar.addWidget(self.user)
        self.file_toolbar.addWidget(self.l2)
        self.file_toolbar.addWidget(self.pwd)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.login_btn)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.fliter_btn)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.buy_btn)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.close_action)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.zoom_in_btn)
        self.file_toolbar.addWidget(self.reload_btn)
        self.file_toolbar.addWidget(self.zoom_out_btn)

    def Layout_init(self):
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.browser)
        hlayout.setSpacing(0)
        hlayout.addWidget(self.file_toolbar)
        widget = QWidget()
        widget.setLayout(hlayout)
        self.setCentralWidget(widget)


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DEMO = MyWindow()
    sys.exit(app.exec_())
