import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.utils.dataframe import dataframe_to_rows

# 创建一个 DataFrame
data = {
    "日期": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
    "销售额": [100, 200, 150, 300],
}
df = pd.DataFrame(data)

# 将 DataFrame 写入 Excel 文件
excel_file = "sales_data.xlsx"
df.to_excel(excel_file, index=False)

# 打开 Excel 文件并添加图表
wb = Workbook()
ws = wb.active

# 将 DataFrame 数据写入工作表
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# 创建一个折线图
chart = LineChart()
data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=len(df) + 1)
chart.add_data(data, titles_from_data=True)
chart.title = "销售额趋势"
chart.x_axis.title = "日期"
chart.y_axis.title = "销售额"

# 将图表添加到工作表
ws.add_chart(chart, "E5")

# 保存 Excel 文件
wb.save(excel_file)
