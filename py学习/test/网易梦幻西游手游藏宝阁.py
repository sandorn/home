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
@LastEditTime: 2019-09-04 13:50:41
'''

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    '''标准windows窗口'''

    def setupUi(self, MainWindow):
        # #状态栏、进度条
        self.statusBar = self.statusBar()
        self.setStyleSheet(
            "QLabel{color:rgb(100,100,100,250);font:bold 10pt 微软雅黑;}"
            "QPushButton{background-color:rgb(22,36,92);color:white;width:100%;height:35%;border-radius:10px;border:2px groove gray;border-style:outset;font:bold 10pt 微软雅黑;}"
            "QPushButton:hover{background-color:rgb(248,242,220);color: black;}"
            "QPushButton:pressed{background-color:rgb(163,159,147);border-style:inset;}"
            "QLineEdit{width:100% ;height:20%; border:2px groove gray;border-radius:10px;padding:2px 4px;background:lightBlue;color:Indigo; font: bold 11pt 等线;}")
        # #工具栏
        self.file_toolbar = self.addToolBar('File')
        self.la1 = QLabel('  \n\n\n',)
        self.l1 = QLabel("账号：")
        self.user = QLineEdit(self)
        self.l2 = QLabel("密码：")
        self.pwd = QLineEdit(self)
        self.la2 = QLabel('  \n\n\n')

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

        self.setWindowIcon(QIcon(os.path.dirname(__file__) + '/ico/1202624.png'))
        self.btn_init()
        self.toolbar_init()
        self.Layout_init()
        self.browser_init()
        # @  关键，用于自动绑定信号和函数
        QMetaObject.connectSlotsByName(MainWindow)

    def browser_init(self):
        self.browser.load(QUrl('https://my.cbg.163.com'))
        # self.browser.urlChanged.connect(lambda: self.url_le.setText(self.browser.url().toDisplayString()))
        self.browser.titleChanged.connect(lambda: self.setWindowTitle(self.browser.title()))
        self.browser.iconChanged.connect(lambda: self.setWindowIcon(QIcon(self.browser.icon())))
        self.show()



    def btn_init(self):

        def btnUI(self, btn, ico, sht=None, msg=None, name=None):
            _path = os.path.dirname(__file__) + '/'
            btn.setIcon(QIcon(_path + ico))
            btn.setIconSize(QSize(36, 36))
            # btn.setFont(QFont('微软雅黑', 10,QFont.Bold))
            if sht:
                btn.setShortcut(sht)
            if msg:
                btn.setToolTip(msg)
                btn.setStatusTip(msg)
            if name:
                btn.setObjectName(name)  # @用于自动绑定信号和函数

        self.btnUI(self.zoom_in_btn, 'ico/1075665.png', 'Ctrl+=', '放大页面\tCtrl+=')
        self.btnUI(self.reload_btn, 'ico/1075667.png', 'Ctrl+0', '复原页面\tCtrl+0')
        self.btnUI(self.zoom_out_btn, 'ico/1075664.png', 'Ctrl+-', '缩小页面\tCtrl+-')
        self.zoom_in_btn.clicked.connect(lambda: self.browser.setZoomFactor(
            self.browser.zoomFactor() + 0.1))
        self.reload_btn.clicked.connect(lambda: self.browser.setZoomFactor(1))
        self.zoom_out_btn.clicked.connect(lambda: self.browser.setZoomFactor(
            self.browser.zoomFactor() - 0.1))

        self.btnUI(self.login_btn, 'ico/1142198.png', 'Ctrl+L', '登陆交易账号\tCtrl+L', "login_O")
        self.btnUI(self.fliter_btn, 'ico/583565.png', 'Ctrl+R', '筛选账号\tCtrl+R', "fliter_O")
        self.btnUI(self.buy_btn, 'ico/1142184.png', 'Ctrl+B', '购买账号\tCtrl+B', "buy_O")
        self.btnUI(self.close_action, 'ico/1186301.png', 'Ctrl+Q', 'Close the window')
        self.close_action.clicked.connect(QApplication.quit)

    def toolbar_init(self):
        self.file_toolbar.setOrientation(Qt.Vertical)
        self.file_toolbar.setToolButtonStyle(2)  # @左右同时显示文字和图标，3为上下
        self.file_toolbar.setFixedWidth(160)

        self.file_toolbar.addWidget(self.la1)
        self.file_toolbar.addWidget(self.l1)
        self.file_toolbar.addWidget(self.user)
        self.file_toolbar.addWidget(self.l2)
        self.file_toolbar.addWidget(self.pwd)
        self.file_toolbar.addSeparator()  # 分隔线
        self.file_toolbar.addWidget(self.la2)
        self.file_toolbar.addWidget(self.login_btn)
        self.file_toolbar.addSeparator()  # 分隔线
        self.js = QTextEdit(self)
        self.file_toolbar.addWidget(self.js)
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
        vlayout = QVBoxLayout()
        hlayout.setSpacing(0)
        hlayout.addWidget(self.browser)
        # hlayout.addStretch(1)
        hlayout.addWidget(self.file_toolbar)
        vlayout.addLayout(hlayout)
        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.browser.loadFinished.connect(self.onDone)

    def onDone(self):
        ttt = self.browser.url()  # .toDisplayString()
        print(ttt)

    @pyqtSlot()
    def on_login_O_clicked(self):
        self.browser.load(QUrl('https://my.cbg.163.com/cgi/show_login?back_url=https%3A%2F%2Fmy.cbg.163.com'))
        js_string = '''
        //window.location.href="/cgi/mweb/user";//指定要跳转到的目标页面

        var int=self.setInterval(function(){  //延迟执行大括号里的方法
            alert('setInterval');
            document.querySelector('.btn.primary').click();
        },5000) //这里5000代表两秒

        '''
        self.browser.page().runJavaScript(js_string)

    @pyqtSlot()
    def on_fliter_O_clicked(self):
        js_string = self.js.toPlainText()
        # jQuery相关语句
        '''
        self.browser.load(QUrl(
            'https://my.cbg.163.com/cgi/show_login?back_url=https%3A%2F%2Fmy.cbg.163.com%2Fcgi%2Fmweb%2Fuser'
            'https://my.cbg.163.com/cgi/mweb/user'
            ))  # 'icon.icon-footer-mine'

        self.browser.triggerAction（QWebPage :: Copy）;
        body > div.page-app > div > div.page-loading.vpa-router-view.child-view > div > div.site-content > div.user-header > p.login > a
        /html/body/div[1]/div/div[1]/div/div[2]/div[1]/p[2]/a
        # document.querySelector('.btn.primary').click();
        # <div data-action="goEmailLogin" class="u-head1 j-head" id="auto-id-1561096233059">网易邮箱帐号登录</div>
        <div data-action="goEmailLogin" class="u-head1 j-head" id="auto-id-1561516270426">网易邮箱帐号登录</div>
        #innerHTML,innerText,outerHTML,outerText的区别 - ...
        # alert("hello,world！")
        # .exist()
        # document.getElementById('kw').value='减肥';
        # document.getElementById('su').click();
        #document.querySelector('.u-head1 j-head').click();
        $('.btn').trigger('click')
        $('.btn').eq(0).trigger('click')
        document.getElementById('img1').onload = function(e){
            e.stopPropagation();
            alert(1);}

        function sleep(delay) {
            var start = (new Date()).getTime();
            while ((new Date()).getTime() - start < delay) {
                continue;
            }
        };
        window.location.href="/cgi/mweb/user";//指定要跳转到的目标页面
        //document.querySelector('.icon.icon-footer-mine').click();

        function re() {
            var i = 1
            while ( !document.querySelector('.btn.primary').complete ){
                sleep(500)
                console.log(i)
                i++
            };

            document.querySelector('.btn.primary').click();
        };

        re();

        //document.querySelector('.btn.primary').onload = function(e){
        //    document.querySelector('.btn.primary').click();
        //    alert(1);
        //}

        '''
        self.browser.page().runJavaScript(js_string)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    DEMO = MyWindow()
    sys.exit(app.exec_())
