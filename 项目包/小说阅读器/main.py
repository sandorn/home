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
LastEditTime : 2022-11-22 15:44:56
Github       : https://github.com/sandorn/home
==============================================================
'''
import sys

from read_ui import Ui_MainWindow
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())  # 程序关闭时退出进程
'''
————————————————
版权声明：本文为CSDN博主「king0964」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/king0964/article/details/104276137
'''
