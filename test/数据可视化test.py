# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-10-08 13:04:01
LastEditTime : 2024-10-08 13:04:01
FilePath     : /CODE/test/数据可视化test.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import pandas as pd
import pynimate as nim
from matplotlib import pyplot as plt

df = pd.DataFrame(
    {
        "time": ["1960-01-01", "1961-01-01", "1962-01-01"],
        "Afghanistan": [1, 2, 3],
        "Angola": [2, 3, 4],
        "Albania": [1, 2, 5],
        "USA": [5, 3, 4],
        "Argentina": [1, 4, 5],
    }
).set_index("time")

cnv = nim.Canvas()
bar = nim.Barplot(df, "%Y-%m-%d", "2d")
bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
cnv.add_plot(bar)
cnv.animate()
plt.show()
