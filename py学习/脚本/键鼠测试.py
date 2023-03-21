# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-17 16:34:43
LastEditTime : 2023-03-17 16:35:00
FilePath     : /CODE/py学习/脚本/键鼠测试.py
Github       : https://github.com/sandorn/home
==============================================================
https://blog.csdn.net/u010751000/article/details/106989322/?ops_request_misc=&request_id=&biz_id=102&utm_term=python%20%E6%A8%A1%E6%8B%9F%E9%94%AE%E9%BC%A0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-106989322.142^v73^pc_new_rank,201^v4^add_ask,239^v2^insert_chatgpt&spm=1018.2226.3001.4187
'''
import time

from pykeyboard import PyKeyboard
# Python实用宝典
from pymouse import PyMouse

# 初始化鼠标对象
m = PyMouse()

time.sleep(5)

# 移动鼠标到(x, y)绝对地址
m.move(200, 200)
time.sleep(1)

# 鼠标点击(500, 300), 第三个参数代表键位，1是左键，2是右键，3是中键
m.click(850, 570, 1)
time.sleep(1)
# 中键垂直滚动 10个单位
m.scroll(200, 0)
# 当前位置
print(m.position())
# 当前屏幕大小
print(m.screen_size())

# 初始化键盘对象
k = PyKeyboard()

# 按住alt键
k.press_key(k.alt_key)
# tab键
k.tap_key(k.tab_key)
# 释放alt键
k.release_key(k.alt_key)

# F5键
k.tap_key(k.function_keys[5])
# Home键
k.tap_key(k.numpad_keys['Home'])
# 按数字5三次
k.tap_key(k.numpad_keys[5], n=3)
