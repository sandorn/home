# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-16 21:34:18
LastEditTime : 2022-12-17 20:52:50
FilePath     : /py学习/数据/xlwings--test.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import xlwings as xw

app = xw.App(add_book=False)
wb = app.books.add()  # 创建一个临时表格
wb.sheets.add(name='hello_friend')
sht = wb.sheets['hello_friend']  # 选中hello_friend的sheet,也可以用sheets[0]去选中
sht.range("A1").value = 1  # 给指定单元格赋值
# !重点,在调用range后的api后面的方法或者属性首字母必须大写
sht.range("A1").api.Font.Size = 15  # 设置单元格字体大小
sht.range("A1").api.Font.Name = "微软雅黑"  # 设置字体
sht.range("A1").api.Font.Bold = True  # 设置单元格字体是否加粗
sht.range("A1").api.Font.Color = 0x0000FF  # 设置字体颜色
# 画框
sht.range("A1:c3").api.Borders(9).LineStyle = 1  # 划底部边框
sht.range("A1:C3").api.Borders(9).Weight = 3
sht.range("A1:C3").api.Borders(10).LineStyle = 1  # 划右部边框
sht.range("A1:C3").api.Borders(10).Weight = 3
sht.range("A1:C3").api.Borders(11).LineStyle = 1  # 划内部竖线
sht.range("A1:C3").api.Borders(11).Weight = 2
sht.range("A1:C3").api.Borders(12).LineStyle = 1  # 划内部横线
sht.range("A1:C3").api.Borders(12).Weight = 2
sht.range("A1:C3").api.HorizontalAlignment = -4108
# -4108 水平居中。 -4131 靠左，-4152 靠右
sht.range("A1:C3").api.VerticalAlignment = -4108
# -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。
sht.range("B1").api.WrapText = True  # 自动换行
sht.range("A1:A3").api.Interior.ColorIndex = 6  # 设置单元格背景颜色
# sht.range("B2:C3").api.Interior.Pattern = 5  # 设置单元格前置网格
sht.range("C1").formula = "=SUM(A1:B1)"  # 引用公式
sht.range("C2").formula = "=SUM(A2:B2)"  # 引用公式
sht.range("C3").api.NumberFormatLocal = "0.00%"  # 设置单元格格式
sht.range("A1:C3").columns.autofit()  # 自动根据单元格中内容调整单元格的宽度
sht.range("A1").color = [0, 0, 255]  # 设置单元格背景颜色
print(sht.range("A1").value)  # 返回单元格内容
print(sht.range("A1").color)  # 返回单元格颜色值
print(sht.range("C1").formula_array)  # 返回单元格中的引用公式
sht.range('A2').value = [['hello 1', 'hello 2', 'hello 3'], [1.0, 2.0, 3.0]]  # 批量填写数据
sht.range("A1:C3").columns.autofit()  # 自动根据单元格中内容调整单元格的宽度
sht.range("A1:B1").api.Merge()  # 合并
print(sht.range("A1").merge_area)  # 返回涉及range的那些合并的单元格

print(sht.range("A4:C4").merge_cells)  # 是merge的元素,返回True,不是返回false,超过merge的范围返回None
sht.range("A1:B1").api.UnMerge()  # 取消合并单元格
