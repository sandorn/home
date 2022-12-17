# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-16 12:19:18
LastEditTime : 2022-12-17 17:17:06
FilePath     : /xjLib/xt_DAO/xt_Xlwings.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-16 12:19:18
LastEditTime : 2022-12-17 16:47:04
FilePath     : /xjLib/xt_DAO/xt_Xlwings.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import xlwings as xw


class XwType:

    def __init__(self):
        self.app = xw.App(add_book=False)
        self.Book = {}
        self.Sheet = {}
        self.Range = {}


class ExcelHandler():
    ''' xlwings操作Excel xlsx文件的类 '''

    def __init__(self, book='工作簿1', sheet_name=None, range='A1'):
        self.app = xw.App(add_book=False)
        self.Book = book
        self.Sheet = sheet_name or self.Book.active
        self.Range = range

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False if exc_type else True

    def xl_insert(self, m_col, m_text):
        k = 0  # 记录插入行
        for i in range(1, self.Sheet.used_range.last_cell.row):
            # 检测到已插入的行进行跳过处理
            if (i == k): continue
            if (self.Sheet.range(m_col + str(i)).value == m_text):
                print("对第 " + str(i) + " 行进行了插入行操作！")
                self.Sheet.api.Rows(i).Insert()
                k = i + 1

    def xl_delete(self, m_col, m_text):

        _tmp_rows = 0  # 记录行
        for i in range(self.Sheet.used_range.last_cell.row, 1, -1):
            if (self.Sheet.range(m_col + str(i)).value == m_text):
                print("对第 " + str(i) + " 行进行了删除行操作！")
                self.Sheet.range(m_col + str(i)).api.EntireRow.Delete()
                _tmp_rows = i + 1
        return _tmp_rows

    def getbook(self):
        self.Book = input('请输入工作簿名称：')

    def getsheet(self):
        self.Sheet = input('请输入工作表名称：')

    def getrange(self):
        self.Range = input('请输入区域表达式：')

    def gets(self):
        self.getbook()
        self.getsheet()
        self.getrange()

    #读取特定Book、Sheet、Range的方法，导出一个list：
    def readL(self):
        readList = xw.books[self.Book].sheets[self.Sheet].range(self.Range).value
        print(readList)
        return readList

    #在特定Book、Sheet、Range的方法写入一个list：
    def writeL(self, List):
        xw.books[self.Book].sheets[self.Sheet].range(self.Range).value = List
        return


if __name__ == "__main__":
    app = xw.App(visible=True, add_book=False)  # 当然也可以通过app.visible = True设置可见性
    pid = app.pid
    print(pid)
    # app.quit()
