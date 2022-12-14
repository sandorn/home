# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-21 19:30:27
#LastEditTime : 2020-05-21 20:17:22
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
PyQt5-QComboBox控件使用 - ygzhaof_100 - 博客园
https://www.cnblogs.com/ygzhaof/p/10062433.html
'''

#QComboBox下拉列表控件使用,省市级联
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
from xjLib.xt_ui import xt_QComboBox, xt_QDoubleSpinBox, xt_QSpinBox
import sys


class WindowClass(QWidget):

    def __init__(self, parent=None):
        self.citys = {"北京": ["北京"], "上海": ["上海"], "河北省": ["石家庄", "邯郸"]}
        super(WindowClass, self).__init__(parent)
        layout = QVBoxLayout()
        self.comboBox_1 = xt_QComboBox()
        self.comboBox_1.addItem("--请选择--")
        self.comboBox_1.addItem("北京")
        self.comboBox_1.addItem("上海")
        self.comboBox_1.addItem("河北省")
        self.comboBox_1.addItems(["湖南省", "湖北省", "天津"])

        self.comboBox_2 = xt_QComboBox()
        self.comboBox_2.addItem("--请选择--")
        self.QSpinBox = xt_QDoubleSpinBox()

        layout.addWidget(self.comboBox_1)
        layout.addWidget(self.comboBox_2)
        layout.addWidget(self.QSpinBox)
        # self.comboBox_1.currentIndexChanged.connect(self.btnState)

        self.setLayout(layout)

    def btnState(self):
        print("状态：", self.comboBox_1.currentText())
        # for count in range(self.comboBox_1.count()):
        #     print("列表选项:" ,self.comboBox_1.itemText(count),count)

        province = self.comboBox_1.currentText()
        print(province in self.citys.keys())
        if province != "--请选择--":
            self.comboBox_2.clear()
            self.comboBox_2.addItems(self.citys[province] if province in
                                     self.citys.keys() else ["--请选择--"])
        else:
            self.comboBox_2.clear()
            self.comboBox_2.addItem("--请选择--")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowClass()
    win.show()
    sys.exit(app.exec_())
