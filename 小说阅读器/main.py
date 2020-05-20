# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-07 12:43:12
#LastEditTime : 2020-05-13 19:00:57
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import sys

from read_ui import Ui_MainWindow
# from READ_UI import Ui_MainWindow
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())  # 程序关闭时退出进程
'''
————————————————
版权声明：本文为CSDN博主「king0964」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/king0964/article/details/104276137
'''
