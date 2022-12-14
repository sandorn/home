# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-21 10:03:43
@LastEditors: Even.Sand
@LastEditTime: 2019-06-21 10:34:38
'''
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
################################################
# 创建主窗口
################################################


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('My Browser')
        self.showMaximized()

        # 放入WebEngineView
        self.webview = WebEngineView()
        self.webview.load(QUrl("https://www.baidu.com"))
        self.setCentralWidget(self.webview)

        # web页面加载完毕，调用函数
        self.webview.page().loadFinished.connect(self.run_js)
        # self.webview.page().loadFinished.connect(self.run_js2)

    ########运行js脚本，没有回调########

    def run_js(self):
        # '''alert("hello,world！");'''
        js_string = '''
            document.getElementById('kw').value='减肥';
            document.getElementById('su').click();
        '''

        self.webview.page().runJavaScript(js_string)

    ########运行js脚本，有回调########

    def run_js2(self):
        js_string = '''
        function myFunction()
        {
            return document.body.scrollWidth;
        }

        myFunction();
        '''

        self.webview.page().runJavaScript(js_string, self.js_callback)

    # 回调函数

    def js_callback(self, result):
        print(result)
        QMessageBox.information(self, "提示", str(result))


################################################
# 创建浏览器
################################################
class WebEngineView(QWebEngineView):
    windowList = []

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        new_window = MainWindow()
        new_window.setCentralWidget(new_webview)
        # new_window.show()
        self.windowList.append(new_window)  # 注：没有这句会崩溃
        return new_webview


################################################
# 程序入门
################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
