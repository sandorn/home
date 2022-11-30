# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
FilePath     : /项目包/小说阅读器/main.py
LastEditTime : 2022-11-29 16:52:06
Github       : https://github.com/sandorn/home
==============================================================
'''
import sys

from PyQt5 import QtWidgets
from read_ui import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())  # 程序关闭时退出进程
