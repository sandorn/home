# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-12 11:31:03
#LastEditTime : 2020-05-29 17:56:16
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import pygame
from PyQt5 import QtWidgets
from PyQt5.QtCore import QMetaObject, pyqtSlot, QThread
from PyQt5.QtWidgets import (QHBoxLayout, QMessageBox, QVBoxLayout, qApp)

from xjLib.mystr import Ex_Re_Clean, Ex_Re_Sub
from xjLib.xt_ahttp import ahttpGet
from xjLib.xt_ui import (EventLoop, xt_QLabel, xt_QLineEdit, xt_QListWidget,
                         xt_QMainWindow, xt_QPushButton, xt_QTableView,
                         xt_QTabWidget, xt_QTextBrowser)
from xjLib.xt_ui.alispeak import get_ali_token, postRESTful

appkey = 'Ofm34215thIUdSIX'
token = get_ali_token()[0]

from io import BytesIO


class readthread(QThread):

    def __init__(self, textlist):
        super().__init__()
        self._running = True
        self.textlist = textlist
        self.start()

    def run(self):
        self.datas_list = []
        pygame.mixer.init(frequency=8000)  #!使用16000和默认,声音不行

        while True:
            if len(self.textlist) > 0:
                ##文本未空
                text = self.textlist.pop(0)
                thread = QThread()
                thread.run = postRESTful
                # @wav,无需  format
                data = thread.run(
                    appkey, token, text, format='mp3', speech_rate=-40)
                self.datas_list.append(data)

            if not self._running:
                ##停止标记
                print('self.py_mixer.stoping!!!!!!')
                # @wav, pygame.mixer.stop()
                pygame.mixer.music.stop()
                break

            if pygame.mixer.music.get_busy():
                # @wav, pygame.mixer.get_busy():
                ##正在播放，等待
                QThread.msleep(200)
                # print('self.py_mixer.playing......')
                continue
            else:
                QThread.msleep(200)
                if len(self.datas_list) > 0:
                    ##朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    pygame.mixer.music.load(BytesIO(_data))
                    # @wav,无需BytesIO，不能设置播放起止时间，pygame.mixer.Sound(_data).play()
                    pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer.new loading......')
                    continue
                else:
                    ##朗读完毕，且无未加载数据
                    self._running = False
                    print('all recod play finished!!!!!!')
                    # @wav, pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    break

    def stop(self):
        self._running = False


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('小说阅读器')
        self.baseurl = 'https://www.biqukan.com'
        self.list = []  #章节列表

        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.lineEdit = xt_QLineEdit('0_790')
        self.book_number = self.lineEdit.text()
        self.lineEdit.textChanged.connect(self.setnum)
        self.lineEdit.setObjectName('lineEditobj')
        self.pushButton = xt_QPushButton("&OK 确定")
        self.pushButton.setObjectName('ok_button')

        self.tabWidget = xt_QTabWidget(["列表显示", "图表显示"])
        self.tableWidget = xt_QTableView(['书号', '章节', '链接'])
        self.tabWidget.lay[0].addWidget(self.tableWidget)
        self.listWidget = xt_QListWidget()
        self.tabWidget.lay[1].addWidget(self.listWidget)
        self.tabWidget.setCurrentIndex(1)

        self.QTextEdit = xt_QTextBrowser()

        self.pushButton_read = xt_QPushButton("&Read")
        self.pushButton_read.clicked.connect(self.read)
        self.pushButton_3 = xt_QPushButton("上一页")
        self.pushButton_3.clicked.connect(self.previous)
        self.pushButton_4 = xt_QPushButton("下一页")
        self.pushButton_4.clicked.connect(self.next)

    def setnum(self):
        self.book_number = self.lineEdit.text()

    def retranslateUi(self):
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(self.pushButton)
        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.tabWidget)
        vlayout1 = QVBoxLayout()
        vlayout1.addLayout(hlayout)
        vlayout1.addLayout(hlayout1)
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.pushButton_read)
        hlayout2.addWidget(self.pushButton_3)
        hlayout2.addWidget(self.pushButton_4)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(self.QTextEdit)
        vlayout2.addLayout(hlayout2)

        hlayout3 = QHBoxLayout()
        hlayout3.addLayout(vlayout1)
        hlayout3.addLayout(vlayout2)

        vlayout3 = QVBoxLayout()
        vlayout3.addLayout(hlayout3)
        self.centralwidget.setLayout(vlayout3)
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)  # @  关键，用于自动绑定信号和函数
        self.tabWidget.currentChanged.connect(self.currentChanged_event)

    def currentChanged_event(self, index):
        if index == 0:
            self.pushButton_read.setHidden(True)
            self.pushButton_3.setHidden(True)
            self.pushButton_4.setHidden(True)
        else:
            self.pushButton_read.setHidden(False)
            self.pushButton_3.setHidden(False)
            self.pushButton_4.setHidden(False)
        pass

    def read(self):
        if self.pushButton_read.text() == '&Read':
            self.pushButton_read.setText('&STOP')
            qApp.processEvents()
            ##处理字符串
            newText = []
            _xt = ''

            QTextEditText = self.QTextEdit.toPlainText().strip().split('\n')
            QTextEditText[0] = QTextEditText[0] + '。'
            for index, text in enumerate(QTextEditText):
                if len(text) > 300:
                    temp = text.split('。')
                    long = round(len(temp) / 2)
                    newText.append('。'.join(temp[:long]) + '')
                    newText.append('。'.join(temp[long:]))
                    continue

                if len(_xt) < 300:
                    _xt += text

                if len(_xt) > 300:
                    temp = _xt.split('。')
                    long = round(len(temp) / 2)
                    newText.append('。'.join(temp[:long]))
                    newText.append('。'.join(temp[long:]))
                    _xt = ''
                    continue

            if _xt != '':
                ##退出for in后清理临时变量
                newText.append(_xt)
                _xt = ''
            self.runthread = readthread(newText)
        else:
            self.pushButton_read.setText('&Read')
            self.runthread.stop()
            qApp.processEvents()

    def previous(self):
        if self.row > 0:
            self.listWidget.setCurrentRow(self.row - 1)

    def next(self):
        if self.row + 1 < self.listWidget.count():
            self.listWidget.setCurrentRow(self.row + 1)

    # 抓取所有数据
    @pyqtSlot()
    def on_ok_button_clicked(self):
        self.QTextEdit.clear()
        self.tableWidget.clean()
        self.listWidget.clear()  # empty()

        try:
            # # 设置书本初始地址,执行主方法
            _url = self.baseurl + '/' + self.book_number + '/'
            self.list = self.getlist(_url)

            self.bindTable()  # 对表格进行填充
            self.bindList()  # 对列表进行填充

            self.listWidget.currentRowChanged.connect(
                self.currentRowChanged_event)
            self.tableWidget.clicked.connect(self.tableClick_event)  # @绑定表格单击方法

        except Exception as err:
            QMessageBox.warning(None, "警告", f"没有数据，请重新设置书号……:{err}",
                                QMessageBox.Ok)
            return

    # 抓取数据
    @EventLoop
    def getlist(self, url):
        _list = []
        _res = ahttpGet(url)
        element = _res.element

        self.bookname = element.xpath(
            '//meta[@property="og:title"]//@content')[0]
        self.setWindowTitle(self.title + '--' + self.bookname)

        全部章节节点 = element.xpath(
            '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a')

        for item in 全部章节节点:  # 遍历文章列表
            _href = item.xpath("@href")[0]
            _text = item.xpath("string(.)").strip()
            _list.append([_text, self.baseurl + _href])  # 获取遍历到的具体文章地址

        return _list

    # 从网页提取数据
    @EventLoop
    def getcontent(self, url):
        _res = ahttpGet(url)
        element = _res.element
        _title = "".join(element.xpath('//h1/text()'))
        _showtext = "".join(element.xpath('//*[@id="content"]/text()'))

        title = Ex_Re_Sub(_title, {' ': '', ' ': ''})
        text = Ex_Re_Sub(
            _showtext.strip("\n\r　  "), {
                '　　': '\n',
                '\r\r': '\n',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
                '    ': '\n    ',
            })
        temp_list = [
            '\u3000\u3000',
            '\xa0',
            "', '",
            '\u3000',
            '/&nbsp;',
            '\(https://www.biqukan.com/[0-9]{1,4}_[0-9]{3,8}/[0-9]{3,14}.html\)',
            'www.biqukan.com。',
            'wap.biqukan.com',
            'www.biqukan.com',
            'm.biqukan.com',
            'n.biqukan.com',
            '笔趣看;',
            '百度搜索“笔趣看小说网”手机阅读:',
            '请记住本书首发域名:',
            '请记住本书首发域名：',
            '笔趣阁手机版阅读网址:',
            '笔趣阁手机版阅读网址：',
            '\[\]',
            '<br />',
        ]

        article_content = Ex_Re_Clean(text.strip("\n\r　  "), temp_list)

        return "《" + self.bookname + '->' + title + "》\n\n" + article_content, _res.text

    # 将文件显示在Table中（列表显示）
    @EventLoop
    def bindTable(self):
        res = [[self.book_number, self.list[index][0], self.list[index][1]]
               for index in range(len(self.list))]
        self.tableWidget.appendItems(res)
        self.tableWidget.scrollToTop()

    # 将文件显示在List列表中（图表显示）
    @EventLoop
    def bindList(self):
        self.listWidget.addItems(
            [self.list[index][0] for index in range(len(self.list))])
        # self.listWidget.scrollToBottom()
        self.listWidget.scrollToTop()

    # 表格单击方法，用来打开选中的项
    @EventLoop
    def tableClick_event(self, item):
        self.QTextEdit.clear()
        QModelIndex = self.tableWidget.model.index(item.row(), 2)
        _, _text = self.getcontent(QModelIndex.data())
        self.QTextEdit.setHtml(_text)

    # 列表单击方法，用来打开选中的项
    @EventLoop
    def currentRowChanged_event(self, row):
        self.row = row
        self.QTextEdit.clear()
        _text, _ = self.getcontent(self.list[row][1])
        _temp = '<font size="4">' + _text.replace("\n", "<br>") + '</font>'
        self.QTextEdit.setText(_temp)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    text = '''
    根据北京银保监局近期工作部署要求,以及本次监管谈话，盛唐融信高度重视，迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。
    公司由专项小组牵头，按监管要求全面深入进行排查整治。主要包括两方面，一是全面排查现有营销人员，重点是是否存在曾涉及金赛银事件、销售其他未经批准金融保险产品等其他违法违规行为；二是盛唐融信股权激励计划情况说明及风险预案。具体汇报如下：
    一、高度重视
    盛唐融信对此次谈话高度重视，悉心接受，积极改正，按监管要求抓好整改落实，有关情况及时向监管汇报。盛唐融信将以本次整治为契机，进一步提高政治站位，增强行动自觉，做好全面排查整改，加强营销人员及合规管理，促进公司健康发展，维护市场公平秩序。
    '''

    ui.QTextEdit.setText(text)
    sys.exit(app.exec_())  # 程序关闭时退出进程
