# !/usr/bin/env python
"""
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-21 14:40:30
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-30 15:50:19
"""

import sys
import time
from urllib.parse import unquote

from baidu_key_UI import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QFileDialog, QTableWidgetItem
from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Requests import get
from xt_Ui import EventLoop


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
        self.label.setText(f'进度：{self.step}/{self.pbar.maximum()}')

    @EventLoop
    def update(self, item):
        RowCont = self.resultTable.rowCount()
        self.resultTable.insertRow(RowCont)
        self.resultTable.setItem(RowCont, 0, QTableWidgetItem(item[0]))
        self.resultTable.setItem(RowCont, 1, QTableWidgetItem(str(item[1])))
        self.resultTable.setItem(RowCont, 2, QTableWidgetItem(str(item[2])))
        self.resultTable.setItem(RowCont, 3, QTableWidgetItem(item[3]))
        self.resultTable.setItem(RowCont, 4, QTableWidgetItem(item[4]))
        self.resultTable.scrollToBottom()  # 滚动到最下

    @pyqtSlot()
    def on_openObject_triggered(self):
        # 打开关键字文件并导入
        self.disable_actions()  # 禁用动作按钮
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file')

        if filename:
            self.clear_keys_table()  # 清空关键字表格
            self.status_bar.showMessage('导入关键字......')
            self._name = self.get_file_name_without_extension(filename)

            with open(filename) as myFile:
                self.keys = self.get_sorted_unique_nonempty_rows(myFile)  # 获取文件中的排序、去重、非空行

            self.write_to_table_widget()  # 将关键字写入表格

        self.status_bar.showMessage('导入关键字完毕!')
        self.enable_actions()  # 启用动作按钮

    def disable_actions(self):
        self.open_action.setEnabled(False)
        self.save_action.setEnabled(False)
        self.run_action.setEnabled(False)

    def clear_keys_table(self):
        self.keysTable.setRowCount(0)

    def get_file_name_without_extension(self, filename):
        return '.'.join(filename.split('.')[:-1])

    def get_sorted_unique_nonempty_rows(self, file):
        return sorted({row.strip() for row in file if row.strip()})

    def write_to_table_widget(self):
        for item in self.keys:
            row_count = self.keysTable.rowCount()
            self.keysTable.insertRow(row_count)
            self.keysTable.setItem(row_count, 0, QTableWidgetItem(item))
            self.keysTable.scrollToBottom()

    def enable_actions(self):
        self.open_action.setEnabled(True)
        self.save_action.setEnabled(True)
        self.run_action.setEnabled(True)

    @pyqtSlot()
    @EventLoop
    def on_runObject_triggered(self):
        if len(self.keys) == 0:
            self.status_bar.showMessage('请先导入关键字！！！')
            return
        self.disable_actions()  # 禁用动作按钮

        self.resultTable.clearContents()
        self.resultTable.setRowCount(0)

        # 构建urls
        pages = self.lineEdit.value()

        self.urls = [f'https://www.baidu.com/s?wd={key}&pn={page * 10}' for key in self.keys for page in range(pages)]

        self.status_bar.showMessage('抓取百度检索信息......')

        self.texts = []  # #清空结果库
        resp_list = ahttpGetAll(self.urls)

        print(len(resp_list), resp_list[1])

        self.getdatas(resp_list)
        self.texts.sort(key=lambda x: x[0])  # #排序

        self.status_bar.showMessage('抓取百度检索信息完毕')

        self.enable_actions()  # 启用动作按钮

    def getdatas(self, resp_list):
        _max = len(resp_list)
        self.step = 0
        self.pbar.setMaximum(_max)
        self._step.emit()  # 传递更新进度条信号

        for response in resp_list:
            url = str(response.url)
            key = unquote(url.split('?')[1].split('&')[0].split('=')[1]).replace('+', ' ')
            pages = url.split('?')[1].split('&')[1].split('=')[1]

            搜索结果 = response.element.xpath('//h3/a')
            for index, each in enumerate(搜索结果):
                # #获取显示字符和网页链接
                href = each.xpath('@href')[0]
                title = each.xpath('string(.)').strip()
                # # 剔除百度自营内容
                if '百度' in title or not href.startswith('http') or href.startswith('http://www.baidu.com/baidu.php?'):
                    continue

                # #获取真实网址
                real_url = get(href, allow_redirects=False).headers['Location']  # 网页原始地址
                if real_url.startswith('http') and '.baidu.com' not in real_url:
                    _item = [key, pages, index, title, real_url]
                    self._signal.emit(_item)  # 传递更新结果数据表信号
                    self.texts.append(_item)
            self.step += 1
            self._step.emit()  # 传递更新进度条信号

        # QApplication.processEvents()
        time.sleep(0.02)

    @pyqtSlot()
    def on_saveObject_triggered(self):
        if len(self.texts) == 0:
            self.status_bar.showMessage('没有发现需要保存的内容！！！')
            return

        self.disable_actions()  # 禁用动作按钮

        savefile(f'{self._name}_百度词频.txt', self.texts, br='\t')
        self.texts = []
        self.status_bar.showMessage(f'[{self._name}_百度词频.txt]保存完成。')

        self.enable_actions()  # 启用动作按钮


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    sys.exit(app.exec())
