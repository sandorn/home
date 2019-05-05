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
@Desc    :   None
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView


################################################
#######创建主窗口
################################################
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('My Browser')
        self.size = (720, 1080)  # 窗口大小
        #self.showMaximized()  # 窗口最大化

        self.webview = WebEngineView()
        import os
        filename = os.path.join(os.path.dirname(__file__), 'index.html')
        filename = ('file:///' + filename).replace('\\', '/')
        #filename = QUrl(QFileInfo("index.html").absoluteFilePath())
        #filename = QUrl(os.path.abspath("./index.html"))
        print(filename)
        self.webview.load(QUrl(filename))
        '''with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        self.webview.setHtml(html)'''
        self.setCentralWidget(self.webview)
        self.show()

    def __del__(self):
        self.webview.deleteLater()


################################################
#######创建浏览器
################################################
class WebEngineView(QWebEngineView):
    windowList = []

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        #new_window.show()
        self.windowList.append(new_window)  # 注：没有这句会崩溃！！！
        return new_webview


################################################
#######程序入门
################################################
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
