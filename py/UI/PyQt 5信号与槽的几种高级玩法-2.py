# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
PyQt 5信号与槽的几种高级玩法 - 博文视点（北京）官方博客 - CSDN博客
https://blog.csdn.net/broadview2006/article/details/80132757
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-23 19:42:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-23 19:57:50

使用自定义参数
在PyQt编程过程中，经常会遇到给槽函数传递自定义参数的情况，比如有一个信号与槽函数的连接是

button1.clicked.connect(show_page)
1
我们知道对于clicked信号来说，它是没有参数的；对于show_page函数来说，希望它可以接收参数。希望show_page函数像如下这样：

def show_page(self, name):
print(name,"  点击啦")
1
2
于是就产生一个问题——信号发出的参数个数为0，槽函数接收的参数个数为1，由于0<1，这样运行起来一定会报错（原因是信号发出的参数个数一定要大于槽函数接收的参数个数）。解决这个问题就是本节的重点：自定义参数的传递。
---------------------
作者：博文视点
来源：CSDN
原文：https://blog.csdn.net/broadview2006/article/details/80132757
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QMessageBox, QApplication, QHBoxLayout
import sys


class WinForm(QMainWindow):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')

        button1.clicked.connect(lambda: self.onButtonClick(1))
        button2.clicked.connect(lambda: self.onButtonClick(2))
        '''
        button1.clicked.connect(partial(self.onButtonClick, 1))
        button2.clicked.connect(partial(self.onButtonClick, 2))
        '''

        layout = QHBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)

        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def onButtonClick(self, n):
        print('Button {0} 被按下了'.format(n))
        QMessageBox.information(self, "信息提示框", 'Button {0} clicked'.format(n))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    sys.exit(app.exec_())
