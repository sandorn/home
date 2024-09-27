# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-23 17:17:17
LastEditTime : 2024-09-27 17:06:19
FilePath     : /CODE/test/excel构建图表.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import xlsxwriter

# 创建一个新的 Excel 文件和工作表
workbook = xlsxwriter.Workbook("chart.xlsx")
worksheet = workbook.get_worksheet_by_name("总指标")


# 一些数据
data = [10, 40, 50, 20, 10, 50]

# 将数据写入工作表
worksheet.write_column("A1", data)

# 创建一个图表对象
chart = workbook.add_chart({"type": "line"})

# 配置图表数据系列
chart.add_series({"values": "=总指标!$A$1:$D$7"})
chart.set_title({"name": "Chart with Python"})
chart.set_x_axis({"name": "X Axis"})
chart.set_y_axis({"name": "Y Axis"})
chart.set_style(10)

# 将图表插入工作表
worksheet.insert_chart("L1", chart)

# 关闭 Excel 文件
workbook.close()
