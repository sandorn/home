# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-07 17:18:41
LastEditTime : 2022-12-15 14:45:41
FilePath     : /xjLib/xt_Excel.py
Github       : https://github.com/sandorn/home
==============================================================
https://blog.csdn.net/qq_44614026/article/details/113275741
https://www.cnblogs.com/xcc-/p/xcc_08.html
https://blog.csdn.net/weixin_45417815/article/details/122015992
'''

import os

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


class ExcelHandler():
    ''' openpyxl操作Excel xlsx文件的类 '''

    def __init__(self, file, sheet_name=None):
        '''初始化函数'''
        self.file = file
        if not os.path.exists(file):
            #新建一个新工作表
            _wb = openpyxl.Workbook()
            _wb.save(file)
            _wb.close()

        self.wb = openpyxl.load_workbook(self.file)
        self.sh_name_list = self.wb.sheetnames

        if sheet_name is None: _sh = self.wb.active
        elif sheet_name not in self.sh_name_list:
            _sh = self.wb.create_sheet(sheet_name)
        else:
            _sh = self.wb[sheet_name]
        assert isinstance(_sh, Worksheet)
        self.sh = _sh

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wb.close()
        return False if exc_type else True

    def CreateSheet(self, sheet_name):
        _sh = self.wb.create_sheet(sheet_name)
        assert isinstance(_sh, Worksheet)
        self.sh = _sh

    #创建新表单
    def createNewSheet(self, location, newSheetName):
        self.wb.create_sheet(index=location, title=newSheetName)

    #删除表单
    def removeSheet(self, sheetName):
        self.wb.remove(sheetName)

    def read_header(self, sheet_name=None):
        '''获取表头'''
        # 表头信息为当前表单的标题,限制最大行为1,values_only= True返回单元格的值
        # 如果不加tuple,返回的只是一个对象
        if sheet_name is not None:
            _sh = self.wb[sheet_name]
            assert isinstance(_sh, Worksheet)
            self.sh = _sh

        self.headers = tuple(self.sh.iter_rows(max_row=1, values_only=True))[0]
        return self.headers

    def read_all(self, sheet_name=None):
        '''
        读取xlsx格式文件中的数据
        返回:
            data:表格中的数据
        '''
        if sheet_name is not None:
            _sh = self.wb[sheet_name]
            assert isinstance(_sh, Worksheet)
            self.sh = _sh

        data = [[cell.value for cell in row] for row in self.sh.rows]
        return data

    def read_rows(self, sheet_name=None):
        '''
        读取除表头外所有数据（除第一行外的所有数据）
        返回的内容是一个二维列表,若想获取每一行的数据,可使用for循环或*解包
        '''
        data = self.read_all(sheet_name)
        return data[1:]

    def read_row(self, row, sheet_name=None):
        '''读取某一行数据'''
        if sheet_name is not None:
            _sh = self.wb[sheet_name]
            assert isinstance(_sh, Worksheet)
            self.sh = _sh

        return [cell.value for cell in self.sh[row]]

    def read_row_dict(self, row, sheet_name=None):
        '''
        获取某一行数据,且将表头中的内容与数据结合展示（以字典的形式）
        如：{'序号':1,'会员卡号': '680021685898','机场名称':'上海机场'}
        '''
        row_data = self.read_row(row)
        titles = self.read_header()
        data_dict = dict(zip(titles, row_data))
        return data_dict

    def read_col(self, col, sheet_name=None):
        '''读取某一列数据'''
        if sheet_name is not None:
            _sh = self.wb[sheet_name]
            assert isinstance(_sh, Worksheet)
            self.sh = _sh

        return [*tuple(self.sh.iter_cols(min_col=col, max_col=col, values_only=True))[0]]

    def read_all_dict(self, sheet_name=None):
        '''
        获取所有数据,且将表头中的内容与数据结合展示（以字典的形式）
        如：[
        {'序号':1,'会员卡号': '680021685898','机场名称':'上海机场'},
        {'序号':2,'会员卡号': '680021685899','机场名称':'广州机场'}
        ]
        '''
        if sheet_name is not None:
            _sh = self.wb[sheet_name]
            assert isinstance(_sh, Worksheet)
            self.sh = _sh

        data = []
        rows = list(self.sh.rows)
        titles = self.read_header()
        for row in rows[1:]:
            rwo_data = [cell.value for cell in row]
            data_dict = dict(zip(titles, rwo_data))
            data.append(data_dict)
        return data

    def read_cell(self, row, column):
        '''读取单元格数据'''
        return self.sh.cell(row, column).value

    #修改单元格方法
    def write_cell(self, row, column, value):
        self.sh.cell(row, column).value = value
        self.wb.save(self.file)

    def write_add(self, data_list):
        '''
        追加写入xlsx格式文件
        参数:data_list:将要写入表格的数据(二维列表)
        '''
        for tdd in data_list:
            self.sh.append(tdd)
        self.wb.save(self.file)

    #保存文件方法
    def save_wb(self, excel_path=None):
        if excel_path is not None: self.wb.save(excel_path)
        self.wb.save(self.file)

    @staticmethod
    def write_change(file, sheet_name, row, column, data):
        '''写入Excel数据'''
        wb = openpyxl.load_workbook(file)
        sh = wb[sheet_name]
        assert isinstance(sh, Worksheet)
        sh.cell(row, column).value = data
        wb.save(file)
        wb.close()


if __name__ == "__main__":
    with ExcelHandler("d:/1.xlsx", "Sheet1") as he:
        he.write_cell(1, 2, '2019年')
        rows = he.read_all()
        # he.write_add(rows)
        # print(he.read_all_dict())
        print(he.read_row(1))
        # print(he.read_cell(1, 3))
        print(he.sh_name_list)
        # he2 = ExcelHandler("d:/2.xlsx")
        # he2.write_add(rows)
        print(he.read_col(1))
####################################################
# he = ExcelHandler("d:/1.xlsx", "Sheet1")
# he.write_cell(1, 2, '2019年')
# rows = he.read_all()
# # he.write_add(rows)
# # print(he.read_dict())
# print(he.read_header())
# # print(he.read_cell(1, 3))
# print(he.sh_name_list)
# he2 = ExcelHandler("d:/2.xlsx", "Sheet99")
# he2.write_add(rows)
