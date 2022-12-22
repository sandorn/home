# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-22 19:33:44
FilePath     : /xjLib/xt_DAO/xt_Xlwings.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import xlwings as xw


class XlwingsObj():

    def __init__(self):
        self.App = xw.App(visible=False, add_book=False)
        self.Books = {}
        self.Sheets = {}
        self.Ranges = {}

    def openbook(self, book_name, index=None):
        if index is None: index = len(self.Books) + 1
        self.Books[index] = app.books.open(book_name)

    def addbook(self, book_name, index=None):
        if index is None: index = len(self.Books) + 1
        self.Books[index] = self.App.books.add()
        self.Books[index].save(book_name)

    def savebook(self, index=None):
        if index is not None: self.Books[index].save()
        else:
            for index in range(len(self.Books)):
                self.Books[index].save()

    def closebook(self, index=None):
        if index is not None: self.Books[index].close()
        else:
            for index in range(len(self.Books)):
                self.Books[index].close()

    def addsheet(self, sheet_name, index=None):
        if index is None: index = len(self.Sheets) + 1
        self.Sheets[index] = self.Books[0].sheets.add(sheet_name)

    def quit(self):
        for index in range(len(self.Books)):
            self.Books[index].close()
        self.App.quit()


if __name__ == "__main__":
    app = xw.App(visible=True, add_book=False)
    pid = app.pid
    print(pid)
    wb = app.books.add()  # 创建一个临时表格
    wb.sheets.add(name='hello_friend')
    sht = wb.sheets['hello_friend']  # 选中hello_friend的sheet,也可以用sheets[0]去选中
    sht.range("A1").value = 1  # 给指定单元格赋值

    import sys
    print(sys.version)
    print(sys.executable)
    print(sys.path)
# app.quit()
# app.kill(pid)
