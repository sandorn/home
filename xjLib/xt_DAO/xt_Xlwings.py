# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-16 12:19:18
LastEditTime : 2022-12-17 23:36:27
FilePath     : /xjLib/xt_DAO/xt_Xlwings.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import xlwings as xw


class XlwingsObj:

    def __init__(self):
        self.App = xw.App(visible=False, add_book=False)
        self.Book = {}
        self.Sheet = {}
        self.Range = {}

    def xl_open(self, m_book):
        self.Book = xw.books[m_book]


if __name__ == "__main__":
    app = xw.App(visible=True, add_book=False)
    pid = app.pid
    print(pid)
    # app.quit()
    # app.kill(pid)
