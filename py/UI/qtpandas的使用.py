# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-21 17:21:48
#LastEditTime : 2020-05-21 17:21:50
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from qtpandas.views.DataTableView import DataTableWidget
from qtpandas.models.DataFrameModel import DataFrameModel


class MyMainWidget(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(MyMainWidget, self).__init__(parent)
        self.setupUi(self)

        self.setLayout(self.gridLayout)

        # 退出窗口
        self.quit_btn.clicked.connect(self.quit_act)

        # qtpandas
        model = DataFrameModel()
        # 空模型那个用于存储和处理数据
        # print(type(self.widget_2))
        self.widget_2.setViewModel(model)
        data = {'A': [10, 11, 12], 'B': [12, 11, 10], 'C': ['a', 'b', 'c']}
        self.df = pandas.DataFrame(data)
        self.df['A'] = self.df['A'].astype(np.int8)  # 委托，规定某一列的类型
        model.setDataFrame(self.df)

        # 保存数据
        self.quit_btn_7.clicked.connect(self.save_data)

    def save_data(self):
        self.df.to_csv('data.csv')

    def quit_act(self):
        # sender 是发送信号的对象
        sender = self.sender()
        print(sender.text() + '键被按下')
        qApp = QApplication.instance()
        qApp.quit()
