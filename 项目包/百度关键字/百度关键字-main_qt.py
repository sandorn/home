# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-21 14:40:30
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-30 15:50:19
'''
import sys
import time

from PyQt5.QtCore import QEventLoop, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QFileDialog, QTableWidgetItem, qApp)

from xt_Ahttp import ahttpGetAll
from xt_File import savefile

from xt_Requests import parse_get
from baidu_key_UI import Ui_MainWindow
from urllib.parse import unquote


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
