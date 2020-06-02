# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-05 13:27:17
@LastEditors: Even.Sand
@LastEditTime: 2019-06-18 16:25:32

《快速掌握PyQt5》第三十章 网页交互QWebEngineView - La_vie_est_belle的博客 - CSDN博客
https://blog.csdn.net/La_vie_est_belle/article/details/84837174
'''

import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1080, 720)
        self.back_btn = QPushButton(self)
        self.forward_btn = QPushButton(self)
        self.reload_btn = QPushButton(self)
        self.zoom_in_btn = QPushButton(self)
        self.zoom_out_btn = QPushButton(self)
        self.url_le = QLineEdit(self)
        self.browser = QWebEngineView()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.layout_init()
        self.btn_init()
        self.le_init()
        self.browser_init()

    def layout_init(self):
        self.h_layout.setSpacing(0)
        self.h_layout.addWidget(self.back_btn)
        self.h_layout.addWidget(self.forward_btn)
        self.h_layout.addWidget(self.reload_btn)
        self.h_layout.addStretch(2)
        self.h_layout.addWidget(self.url_le)
        self.h_layout.addStretch(2)
        self.h_layout.addWidget(self.zoom_in_btn)
        self.h_layout.addWidget(self.zoom_out_btn)

        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.browser)

        self.setLayout(self.v_layout)

    def browser_init(self):
        self.browser.load(QUrl('https://baidu.com'))
        self.browser.urlChanged.connect(lambda: self.url_le.setText(
            self.browser.url().toDisplayString()))
        self.browser.loadFinished.connect(lambda: print(self.browser.title()))
        self.show()

    def btn_init(self):
        import os
        _path = os.path.dirname(__file__)
        back_filename = _path + '/wb4/back.png'
        forward_filename = _path + '/wb4/forward.png'
        reload_filename = _path + '/wb4/reload.png'
        zoom_in_filename = _path + '/wb4/zoom_in.png'
        zoom_out_filename = _path + '/wb4/zoom_out.png'
        self.back_btn.setIcon(QIcon(back_filename))
        self.forward_btn.setIcon(QIcon(forward_filename))
        self.reload_btn.setIcon(QIcon(reload_filename))
        self.zoom_in_btn.setIcon(QIcon(zoom_in_filename))
        self.zoom_out_btn.setIcon(QIcon(zoom_out_filename))

        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.reload_btn.clicked.connect(self.browser.reload)
        self.zoom_in_btn.clicked.connect(self.zoom_in_func)
        self.zoom_out_btn.clicked.connect(self.zoom_out_func)

    def le_init(self):
        self.url_le.setFixedWidth(400)
        self.url_le.setPlaceholderText('Search or enter website name')

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Return or QKeyEvent.key() == Qt.Key_Enter:
            if self.url_le.hasFocus():
                if self.url_le.text().startswith(
                        'https://') or self.url_le.text().startswith('http://'):
                    self.browser.load(QUrl(self.url_le.text()))
                else:
                    self.browser.load(QUrl('https://' + self.url_le.text()))

    def zoom_in_func(self):
        self.browser.setZoomFactor(self.browser.zoomFactor() + 0.1)

    def zoom_out_func(self):
        self.browser.setZoomFactor(self.browser.zoomFactor() - 0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DEMO = MainWindow()
    sys.exit(app.exec_())
