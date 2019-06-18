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
@LastEditors: Even.Sand
@LastEditTime: 2019-06-17 17:20:52
'''
from xjLib.req import parse_get
from xjLib.log import log
from pyquery import PyQuery
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed  # 线程池模块
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from xjLib.UI import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    _signal = pyqtSignal(list)
    _step = pyqtSignal()

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        # #自用变量
        self.keys = []  # 关键字
        self.urls = []  # url_list
        self._name = ''  # 文件名
        self.texts = []  # 用于存放结果
        self.step = 0
        self._step.connect(self.step_valueChanged)
        self._signal.connect(self.update)

    def step_valueChanged(self):
        self.pbar.setValue(int(self.step))
        pass

    def update(self, _res):
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        QApplication.setOverrideCursor(Qt.WaitCursor)  # 显示等待中的鼠标样式
        for item in _res:
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
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')

        if filename:
            [self.keysTable.removeRow(0) for _ in range(self.keysTable.rowCount())]
            self.status_bar.showMessage('导入关键字......')
            self._name = filename.split('.')[0:-1][0]  # 文件名，含完整路径，去掉后缀

            _k = []
            with open(filename) as myFile:
                '''
                #for row in myFile.readlines():
                for row in myFile:
                    row = row.strip()  # 默认删除空白符
                    if len(row) == 0:
                        continue  # len为0的行,跳出本次循环
                    _k.append(row)
                # !下面一句语句代替
                '''
                _k = [row.strip() for row in myFile if len(row.strip()) != 0]
            self.keys = sorted(set(_k), key=_k.index)

            self.step = 0
            _max = len(self.keys)
            self.pbar.setMaximum(_max)
            self._step.emit()  # 传递更新进度条信号
            # 写入QTableWidget
            for item in self.keys:
                RowCont = self.keysTable.rowCount()
                self.keysTable.insertRow(RowCont)
                self.keysTable.setItem(RowCont, 0, QTableWidgetItem(item))
                self.keysTable.scrollToBottom()  # 滚动到最下面
                self.step += 1
                self.label.setText("进度：{}/{} ".format(self.step, _max))
                self._step.emit()  # 传递更新进度条信号
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
        self.urls = [(key, page, "https://www.baidu.com/s?wd={}&pn={}".format(
            key, page * 10)) for key in self.keys for page in range(pages)]
        _max = len(self.urls)
        self.step = 0
        self.pbar.setMaximum(0)
        self._step.emit()  # 传递更新进度条信号
        self.label.setText("进度：{}/{}".format(self.step, _max))
        self.status_bar.showMessage('准备抓取任务......')
        # 启动多线程
        future_tasks = []
        with ThreadPoolExecutor(20) as p:
            for url in self.urls:
                _res = p.submit(self.getkeys, url)
                future_tasks.append(_res)
                self.step += 1
                self._step.emit()  # 传递更新进度条信号
                self.label.setText("进度：{}/{}".format(self.step, _max))
                QApplication.processEvents(
                    QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
                time.sleep(0.05)

        self.step = 0
        self._step.emit()  # 传递更新进度条信号
        self.pbar.setMaximum(_max)
        self.status_bar.showMessage('抓取百度检索信息......')
        QApplication.processEvents(
            QEventLoop.ExcludeUserInputEvents)  # 忽略用户的输入（鼠标和键盘事件）
        self.texts = []  # #清空结果库
        # 等待到所有线程结束
        for obj in as_completed(future_tasks):
            _res = obj.result()
            self.step += 1
            self._step.emit()  # 传递更新进度条信号
            self.label.setText("进度：{}/{}".format(self.step, _max))
            if len(_res) == 0:
                continue
            self.texts.append(_res)
            self._signal.emit(_res)  # 传递更新进度条信号
        self.texts.sort()
        self.status_bar.showMessage('抓取百度检索信息完毕')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)
        QApplication.restoreOverrideCursor()  # 恢复鼠标样式

    # ! 多线程运行，as_completed 等待各子线程结束，将各子线程运行结果返回给主线程
    # ! 子线程全部启动后，在逐一退出时会有卡顿

    def getkeys(self, target):
        (key, page, url) = target
        _texts = []
        response = parse_get(url=url)
        result = PyQuery(response.text)  # content.decode('uft-8')
        index = 0
        for each in result("h3 a").items():
            # #获取显示字符和网页链接
            index += 1
            href = each.attr('href')
            title = each.text()

            # # 剔除百度自营内容
            if '百度' in title:
                continue
            if not href.startswith('http'):
                continue

            # #获取真实网址
            baidu_url = parse_get(url=href, allow_redirects=False)
            real_url = baidu_url.headers['Location']  # 得到网页原始地址
            if '.baidu.com' in real_url:
                continue
            if real_url.startswith('http'):
                _texts.append([key, page, index, title, real_url])
        #self.status_bar.showMessage('{}\tdone\tat\t{}'.format(key, get_litetime()))
        QApplication.processEvents()
        time.sleep(0.02)
        return _texts

    @pyqtSlot()
    def on_saveObject_triggered(self):
        if len(self.texts) == 0:
            self.status_bar.showMessage('没有发现需要保存的内容！！！')
            return
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)

        _filename = self._name + '_百度词频.txt'
        lists = self.texts
        # 函数说明:将爬取的文章lists写入文件
        self.status_bar.showMessage('[' + _filename + ']开始保存......')

        with open(_filename, 'w', encoding='utf-8') as f:
            f.write('   key   \tpage\tindex\ttitle\turl\t\n')
            for key in lists:  # 区分关键字
                for index in key:  # 区分记录index
                    [f.write(str(v) + '\t') for v in index]
                    f.write('\n')
            '''
            # # 下面有换行问题
            # #[f.write(str(v) + '\t') for key in lists for index in key for v in index]
            # #多层次的list 或 tuple写入文件
            def each(data):
                for index, value in enumerate(data):
                    if isinstance(value, list) or isinstance(value, tuple):
                        each(value)
                    else:
                        f.write(str(value) + '\t')
                        if index == len(data) - 1:
                            f.write('\n')

            each(lists)
            '''
        self.texts = []
        self.status_bar.showMessage('[' + _filename + ']保存完成。')
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)


if __name__ == "__main__":
    log = log()
    app = QApplication(sys.argv)
    w = MyWindow()
    sys.exit(app.exec_())
