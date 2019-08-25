# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-26 09:50:18
@LastEditors: Even.Sand
@LastEditTime: 2019-06-26 09:55:41
'''
import sys
import os
import codecs
import random
from Ui_main import Ui_Form
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo, QTimer, Qt


class PiChart(QWidget, Ui_Form):
    """
    饼图演示
    """

    def __init__(self, parent=None):
        """
        数据可视化
        """
        super(PiChart, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """
        一些界面配置
        """
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.splitter.setOpaqueResize(False)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 9)

        self.view = QWebEngineView(self.widget)
        vv = QVBoxLayout()
        vv.addWidget(self.view)
        self.widget.setLayout(vv)
        # url = QUrl(QFileInfo("./pie-simple.html").absoluteFilePath())
        # self.view.load(url)
        # url = QUrl(os.path.abspath("./pie-simple.html"))
        # self.view.load(url)
        with codecs.open(os.path.dirname(__file__) + "/pie-simple.html", "r", "utf-8") as f:
            html = f.read()
        self.view.setHtml(html)
        self.time = QTimer()

    def showPi(self):
        """
        显示饼形图
        """
        food = self.spinBox_food.value()
        rent = self.spinBox_rent.value()
        electricity = self.spinBox_electricity.value()
        traffic = self.spinBox_traffic.value()
        relationship = self.spinBox_relationship.value()
        taobao = self.spinBox_taobao.value()
        jscode = "showPiChart({}, {}, {}, {}, {}, {});".format(food, traffic, relationship, rent, electricity, taobao)
        self.view.page().runJavaScript(jscode)

    def autoShow(self):
        """
        自动演示
        """
        self.spinBox_food.setValue(random.randint(100, 10000))
        self.spinBox_rent.setValue(random.randint(100, 10000))
        self.spinBox_electricity.setValue(random.randint(100, 1000))
        self.spinBox_traffic.setValue(random.randint(100, 2000))
        self.spinBox_relationship.setValue(random.randint(100, 3000))
        self.spinBox_taobao.setValue(random.randint(100, 10000))

    @pyqtSlot(bool)
    def on_checkBox_toggled(self, flag):
        """
        复选框选中时触发
        """
        if flag:
            self.time.start(1000)
            self.time.timeout.connect(self.autoShow)
        else:
            self.time.stop()

    @pyqtSlot(int)
    def on_spinBox_food_valueChanged(self, n):
        """
        伙食消费微调框数值改变时触发
        """
        self.showPi()

    @pyqtSlot(int)
    def on_spinBox_rent_valueChanged(self):
        """
        房租微调框数值改变时触发
        """
        self.showPi()

    @pyqtSlot(int)
    def on_spinBox_electricity_valueChanged(self):
        """
        水电气微调框数值改变时触发
        """
        self.showPi()

    @pyqtSlot(int)
    def on_spinBox_traffic_valueChanged(self):
        """
        交通微调框数值改变时触发
        """
        self.showPi()

    @pyqtSlot(int)
    def on_spinBox_relationship_valueChanged(self):
        """
        人情往来微调框数值改变时触发
        """
        self.showPi()

    @pyqtSlot(int)
    def on_spinBox_taobao_valueChanged(self):
        """
        淘宝网购微调框数值改变时触发
        """
        self.showPi()

    def __del__(self):
        self.view.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    piChart = PiChart()
    piChart.show()
    sys.exit(app.exec_())
