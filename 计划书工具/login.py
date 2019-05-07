# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software:   VSCode
@File    :   login.py
@Time    :   2019/05/05 09:08:48
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
'''

import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


# 创建主窗口
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 退出Action设置
        exitAction = QAction(
            QIcon(os.path.join(os.path.dirname(__file__), './ico/exit.ico')),
            '&Exit', self)
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

        #self.showMaximized()
        # 设置窗体无边框
        #self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景透明
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.status = self.statusBar()
        self.status.showMessage("准备就绪")

        self.webview = WebEngineView()

        # GridLayout布局
        grid = QGridLayout()
        grid.setSpacing(10)  # 设置控件的间隙为10
        self.setCentralWidget(self.webview)  # 建立的widget在窗体的中间位置
        self.setLayout(grid)
        #grid.addWidget(title, 1, 0)

        filename = os.path.join(os.path.dirname(__file__), 'index.html')
        if os.path.exists(filename):
            filename = 'file:///' + filename.replace('\\', '/')
            self.webview.load(QUrl(filename))
            '''with open(filename, "r", encoding="utf-8") as f:
                html = f.read()
            self.webview.setHtml(html)'''
        else:
            print('index.html文件未找到')

        #1. 设置应用窗口固定大小显示，实现代码：
        # self.setFixedSize(788,468)
        #2. 设置应用窗口以最大、最小显示，实现代码：
        self.setMinimumSize(788, 468)
        # self.setMaximumSize(360, 150)
        #设置窗口位置和大小
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry((screen.width() - 788) / 2,
                         (screen.height() - 468) / 2, 788, 468)

        self.setWindowTitle('代宝宝')
        self.setWindowIcon(
            QIcon(os.path.join(os.path.dirname(__file__), './ico/dbb.ico')))
        self.show()

    def __del__(self):
        self.webview.deleteLater()
        #程序退出
        #app = QApplication.instance()
        qApp.quit()  # qApp就相当于 QCoreApplication.instance()


# 创建浏览器
class WebEngineView(QWebEngineView):
    # windowList = []
    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        #self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
'''
# 创建一个按钮去调用 JavaScript代码
button = QPushButton('设置全名')

def js_callback(result):
    print(result)


def complete_name():
    view.page().runJavaScript('completeAndReturnName();', js_callback)


# 按钮连接 'complete_name'槽，当点击按钮是会触发信号
button.clicked.connect(complete_name)

# 把QWebView和button加载到layout布局中
layout.addWidget(view)
layout.addWidget(button)

# 显示窗口和运行app
win.show()
sys.exit(app.exec_())
'''
