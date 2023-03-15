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
from matplotlib import pyplot as plt
import pandas as pd
import pynimate as nim

df = pd.DataFrame({
    "time": ["1960-01-01", "1961-01-01", "1962-01-01"],
    "Afghanistan": [1, 2, 3],
    "Angola": [2, 3, 4],
    "Albania": [1, 2, 5],
    "USA": [5, 3, 4],
    "Argentina": [1, 4, 5],
}).set_index("time")



if __name__ == '__main__':
    cnv = nim.Canvas()
    bar = nim.Barplot(df, "%Y-%m-%d", "2d")
    bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
    cnv.add_plot(bar)
    cnv.animate()
    plt.show()
