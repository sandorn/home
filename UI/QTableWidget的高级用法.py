# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 13:41:37
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 13:42:12

PyQt5高级界面控件之QTableWidget（四） - jia666666的博客 - CSDN博客
https://blog.csdn.net/jia666666/article/details/81627589
'''

import sys
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem)


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置标题与初始大小
        self.setWindowTitle("QTableWidget 例子")
        self.resize(430, 230)

        # 水平布局，初始表格为（4*3），添加到布局中
        conLayout = QHBoxLayout()
        tableWidget = QTableWidget(5, 3)
        conLayout.addWidget(tableWidget)

        # 设置水平头标签
        tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重(kg)'])

        # 创建新条目，设置背景颜色，添加到表格指定行列中
        newItem = QTableWidgetItem("张三")
        #newItem.setForeground(QBrush(QColor(255, 0, 0)))
        tableWidget.setItem(0, 0, newItem)

        # 创建新条目，设置背景颜色，添加到表格指定行列中
        newItem = QTableWidgetItem("男")
        #newItem.setForeground(QBrush(QColor(255, 0, 0)))
        tableWidget.setItem(0, 1, newItem)

        # 创建新条目，设置背景颜色，添加到表格指定行列中
        newItem = QTableWidgetItem("160")
        #newItem.setForeground(QBrush(QColor(255, 0, 0)))
        tableWidget.setItem(0, 2, newItem)

        # newItem = QTableWidgetItem("李四")
        # #将字体加粗，黑色字体
        # newItem.setFont(QFont('Times',12,QFont.Black))
        # tableWidget.setItem(1, 0, newItem)
        #
        # # 创建新条目，设置背景颜色，添加到表格指定行列中
        # newItem = QTableWidgetItem("男")
        # newItem.setFont(QFont('Times', 12, QFont.Black))
        # tableWidget.setItem(1, 1, newItem)
        #
        # # 创建新条目，设置背景颜色，添加到表格指定行列中
        # newItem = QTableWidgetItem("150")
        # newItem.setFont(QFont('Times', 12, QFont.Black))
        # tableWidget.setItem(1, 2, newItem)
        #
        # newItem = QTableWidgetItem("王五")
        # #将字体加粗，黑色字体
        # newItem.setFont(QFont('Times',12,QFont.Black))
        # tableWidget.setItem(2, 0, newItem)
        #
        # # 创建新条目，设置背景颜色，添加到表格指定行列中
        # newItem = QTableWidgetItem("女")
        # newItem.setFont(QFont('Times', 12, QFont.Black))
        # tableWidget.setItem(2, 1, newItem)
        #
        # # 创建新条目，设置背景颜色，添加到表格指定行列中
        # newItem = QTableWidgetItem("175")
        # newItem.setFont(QFont('Times', 12, QFont.Black))

        # 设置单元格文本的对齐方式
        # newItem.setTextAlignment(Qt.AlignRight|Qt.AlignBottom)
        #tableWidget.setItem(2, 2, newItem)

        # 按照体重排序
        # Qt.DescendingOrder降序
        # Qt.AscEndingOrder升序
        # tableWidget.sortItems(2,Qt.DescendingOrder)

        # 合并单元格
        # tableWidget.setSpan(2,0,4,1)

        # 设置单元格的大小
        # 将第一列的单元宽度设置为150
        # tableWidget.setColumnWidth(0,150)
        # 将第一行的单元格高度的设置为120
        # tableWidget.setRowHeight(0,120)

        # 表格中不显示分割线
        # tableWidget.setShowGrid(False)

        # 隐藏垂直头标签
        # tableWidget.verticalHeader().setVisible(False)

        self.setLayout(conLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Table()
    example.show()
    sys.exit(app.exec_())
