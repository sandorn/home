# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-21 22:57:48
#LastEditTime : 2020-05-21 22:57:51
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-12 11:31:03
#LastEditTime : 2020-05-21 22:57:19
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================


'''
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout)

from xjLib.mystr import Ex_Re_Sub, Ex_Replace
from xjLib.xt_ahttp import ahttpGet
from xjLib.xt_ui import xt_QMainWindow, xt_QTableWidget, xt_QListWidget, xt_QTabWidget, xt_QPushButton, xt_QLineEdit, xt_QLabel, xt_QTextEdit, xt_QTextBrowser


class Ui_MainWindow(xt_QMainWindow):

    def __init__(self):
        super().__init__('小说阅读器')
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.centralwidget = QtWidgets.QWidget()
        self.label = xt_QLabel("小说书号：")
        self.label_2 = xt_QLabel("保存路径：")
        self.lineEdit = xt_QLineEdit('38_38836')
        self.book_number = self.lineEdit.text()
        self.lineEdit_2 = xt_QLineEdit(os.path.dirname(__file__) + '\\')
        self.pushButton = xt_QPushButton("选择")
        self.pushButton_2 = xt_QPushButton("确定")

        self.tabWidget = xt_QTabWidget(["列表显示", "图表显示"])
        self.tableWidget = xt_QTableWidget(['书号', '名称'], 0, 2)
        self.tableWidget.setColumnWidth(0, 130)  # 设置第一列宽度
        self.tabWidget.lay[0].addWidget(self.tableWidget)
        self.listWidget = xt_QListWidget()
        self.tabWidget.lay[1].addWidget(self.listWidget)

    def retranslateUi(self):
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(self.pushButton_2)
        hlayout0 = QHBoxLayout()
        hlayout0.addWidget(self.label_2)
        hlayout0.addWidget(self.lineEdit_2)
        hlayout0.addWidget(self.pushButton)

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self.tabWidget)

        vlayout1 = QVBoxLayout()
        vlayout1.addLayout(hlayout)
        vlayout1.addLayout(hlayout0)
        vlayout1.addLayout(hlayout1)

        hlayout2 = QHBoxLayout()
        hlayout2.addLayout(vlayout1)
        self.QTextEdit = xt_QTextBrowser()
        hlayout2.addWidget(self.QTextEdit)

        vlayout3 = QVBoxLayout()
        vlayout3.addLayout(hlayout2)
        self.centralwidget.setLayout(vlayout3)
        self.setCentralWidget(self.centralwidget)

        self.pushButton.clicked.connect(self.setpath)  # 为选择按钮绑定事件
        self.pushButton_2.clicked.connect(self.getDatas)  # 点击确定获取数据

    def msg(self):
        try:
            # dir_path即为选择的文件夹的绝对路径，第二形参为对话框标题，第三个为对话框打开后默认的路径
            self.dir_path = QFileDialog.getExistingDirectory(
                None, "选择路径",
                os.path.dirname(__file__) + '/')
            self.lineEdit_2.setText(self.dir_path)  # 显示选择的保存路径
        except Exception as e:
            print(e)

    def setpath(self):
        try:
            # dir_path即为选择的文件夹的绝对路径，第二形参为对话框标题，第三个为对话框打开后默认的路径
            self.dir_path = QFileDialog.getExistingDirectory(
                None, "选择路径",
                os.path.dirname(__file__) + '/')
            self.lineEdit_2.setText(self.dir_path)  # 显示选择的保存路径
        except Exception as e:
            print(e)

    # 抓取所有数据
    def getDatas(self):
        self.baseurl = 'https://www.biqukan.com'
        self.path = self.lineEdit_2.text()
        try:

            self.book_number = self.lineEdit.text()  # 记录用户设置的书号
            _url = self.baseurl + '/' + self.book_number + '/'  # 设置书本初始地址
            self.getData(_url)  # 执行主方法

            self.getFiles()  # 获取所有文件
            self.bindList()  # 对列表进行绑定
            self.bindTable()  # 对表格进行绑定
            self.listWidget.itemClicked.connect(
                self.itemClicked_event)  # @绑定列表单击方法
            self.tableWidget.itemClicked.connect(self.tableClick)  # @绑定表格单击方法
        except Exception as err:
            QMessageBox.warning(None, "警告", f"没有数据，请重新设置书号……:{err}",
                                QMessageBox.Ok)
            return

    # 抓取数据
    def getData(self, url):
        response = ahttpGet(url).element
        self.bookname = response.xpath(
            '//meta[@property="og:title"]//@content')[0]
        全部章节节点 = response.xpath(
            '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

        self.path = self.path + "\\" + self.bookname + "\\"  # 设置文章存储路径
        if not os.path.isdir(self.path):  # 判断路径是否存在
            os.mkdir(self.path)  # 创建路径
        # self.list = []  #章节列表
        for item in 全部章节节点:  # 遍历文章列表
            # self.list.append(self.baseurl + item)  # 获取遍历到的具体文章地址
            articleUrl = self.baseurl + item  # 获取遍历到的具体文章地址
            self.savecontent(articleUrl)

        # QMessageBox.Information(None, "提示", self.book_number + "的小说保存完成", QMessageBox.Ok)

    # 从网页提取数据
    def savecontent(self, url):
        response = ahttpGet(url).element

        _title = "".join(response.xpath('//h1/text()'))
        _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

        title = Ex_Re_Sub(_title, {' ': '', ' ': ''})
        article_content = Ex_Replace(
            _showtext.strip("\n\r　  "),
            {
                '　　': '\n',
                ' ': ' ',
                '\', \'': '',
                # '\xa0': '',  # 表示空格  &nbsp;
                '\u3000': '',  # 全角空格
                '/&nbsp;': '',  # 全角空格
                'www.biqukan.com。': '',
                'm.biqukan.com': '',
                'wap.biqukan.com': '',
                'www.biqukan.com': '',
                '笔趣看;': '',
                '百度搜索“笔趣看小说网”手机阅读:': '',
                '请记住本书首发域名:': '',
                '请记住本书首发域名：': '',
                '笔趣阁手机版阅读网址:': '',
                '笔趣阁手机版阅读网址：': '',
                '[]': '',
                '<br />': '',
                '\r\r': '\n',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
                '    ': '\n    ',
            },
        )
        fileName = self.path + title + '.txt'  # 设置文章保存路径（包括文章名）
        with open(fileName, "w") as newFile:  # 打开或者创建文件
            newFile.write("<<" + title + ">>\n\n")  # 向文件中写入标题并换行
            newFile.write(article_content)  # 向文件中写入内容

    # 获取所有文件
    def getFiles(self):
        self.list = os.listdir(self.path)  # 列出文件夹下所有的目录与文件
        self.list = sorted(self.list)  # 排序
        # print(self.list)

    # 将文件显示在Table中（列表显示）
    def bindTable(self):
        for i in range(0, len(self.list)):  # 遍历文件列表
            self.tableWidget.insertRow(i)  # 添加新行
            # 设置第一列的值为书号
            self.tableWidget.setItem(
                i, 0, QtWidgets.QTableWidgetItem(self.lineEdit.text()))
            # 设置第二列的值为文件名
            self.tableWidget.setItem(i, 1,
                                     QtWidgets.QTableWidgetItem(self.list[i]))

    # 表格单击方法，用来打开选中的项
    def tableClick(self, item):
        #!显示内容
        if 'txt' in item.text():  # 点击文件名才弹出
            self.QTextEdit.clear()
            with open(self.path + '\\' + item.text(), "r") as file:
                data = file.read()
                self.QTextEdit.setPlainText(data)

    # 将文件显示在List列表中（图表显示）
    def bindList(self):
        for i in range(0, len(self.list)):  # 遍历文件列表
            self.item = QtWidgets.QListWidgetItem(self.listWidget)  # 创建列表项
            self.item.setIcon(QtGui.QIcon('book.png'))  # 设置列表项图标
            self.item.setText(self.list[i])
            self.item.setToolTip(self.list[i])  # 设置提示文字
            self.item.setFlags(QtCore.Qt.ItemIsSelectable
                               | QtCore.Qt.ItemIsEnabled)  # 设置选中与否

    # 列表单击方法，用来打开选中的项
    def itemClicked_event(self, item):
        self.QTextEdit.clear()
        with open(self.path + '\\' + item.text(), "r") as file:
            data = file.read()
            self.QTextEdit.setPlainText(data)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())  # 程序关闭时退出进程
