# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-05-30 11:35:10
LastEditTime : 2025-06-06 10:22:25
FilePath     : /CODE/xjLib/xt_damo/像素颜色捕捉.py
Github       : https://github.com/sandorn/home
==============================================================
"""
from __future__ import annotations

from bdtime import tt, vk
from damo import DM

dm = DM()


def conv_to_rgb(color):
    RGB_str = [color[:2], color[2:-2], color[-2:]]
    return [int(i, 16) for i in RGB_str]


tt.__init__()
while tt.during(10):  # 10s内捕捉鼠标当前位置的颜色
    tt.sleep(0.1)

    if tt.get_key_state(vk.mouse_right) or tt.is_pressed('alt + x'):
        print('--- stopped!')
        break  # 按下鼠标右键, 或者`alt + x`, 则退出循环

    # tt.stop_alt('s')  # 按下`alt + s`则停止进程

    x, y = dm.position
    color = dm.GetColor(x, y)

    print(f"{tt.now(1)},\t {x}:{y},\t color:{color}, \t 鼠标位置颜色RGB值:{conv_to_rgb(color)}")
