# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 09:23:27
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 09:26:15
'''
from PyQt5.QtWidgets import QApplication
import sys
from TMainWindow import TMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    dlg = TMainWindow()
    dlg.show()

    app.exec_()
