# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   webkit嵌入式浏览器3.py
@Time    :   2019/05/05 11:05:52
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
使用PyQt5.QtWebEngineWidgets加载网页 - 探索无止境 - 博客园
http://www.cnblogs.com/xxgis/p/10044225.html
使用PyQt5.QtWebEngineWidgets加载网页
'''

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('My Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('toolbar.bmp'))
        # 设置窗口大小900*600
        self.resize(900, 600)
        self.show()

        # 设置浏览器
        self.browser = QWebEngineView()
        url = 'http://www.baidu.com'
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)

        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        #添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('/wb4/back.png'), 'Back', self)
        next_button = QAction(QIcon('/wb4/forward.png'), 'Forward', self)
        stop_button = QAction(QIcon('/wb4/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('/wb4/reload.png'), 'reload', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        #添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)
        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)
        # 显示窗口
        self.show()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


# 创建应用
app = QApplication(sys.argv)
app.setWindowIcon(QIcon('toolbar.bmp'))
# 创建主窗口
window = MainWindow()
# 运行应用，并监听事件
sys.exit(app.exec_())
