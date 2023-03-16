# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-15 19:05:16
LastEditTime : 2023-03-15 19:05:39
FilePath     : /CODE/py学习/PY编程模式/Python数据可视化.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import pandas as pd


def a1():
    df = pd.DataFrame([["A", 1, 2019], ["B", 2, 2019], ["A", 2, 2020], ["B", 3, 2020]], columns=["name", "value", "year"])  # 构造测试数据
    fig, ax = plt.subplots()  # 准备画板

    def draw_one_year(year):  # 绘制单帧
        cur_df = df[df["year"] == year].sort_values(by="value")
        ax.barh(cur_df["name"], cur_df["value"], color=["r", "g"])

    animator = animation.FuncAnimation(fig, draw_one_year, frames=range(2019, 2021))  # 动态绘制
    animator.save("./test.gif")  # 保存数据


import pandas as pd
import pynimate as nim
from matplotlib import pyplot as plt


def a2():
    df = pd.DataFrame({
        "time": ["1960-01-01", "1961-01-01", "1962-01-01"],
        "Afghanistan": [1, 2, 3],
        "Angola": [2, 3, 4],
        "Albania": [1, 2, 5],
        "USA": [5, 3, 4],
        "Argentina": [1, 4, 5],
    }).set_index("time")

    cnv = nim.Canvas()
    bar = nim.Barplot(df, "%Y-%m-%d", "2d")
    bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
    cnv.add_plot(bar)
    cnv.animate()
    plt.show()


if __name__ == "__main__":
    a2()
