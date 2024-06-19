# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-17 16:34:43
LastEditTime : 2024-06-19 13:04:09
FilePath     : /CODE/py学习/脚本/键鼠测试.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import pyautogui

pyautogui.PAUSE = 0.5

# print(pyautogui.size())
# print(pyautogui.position())
# pyautogui.moveTo(200, 150)
# pyautogui.click(300,500)
windows = pyautogui.getWindowsWithTitle('无标题 - Notepad')  # 如果找到了指定窗口
if len(windows) > 0:
    print(windows)
    windows[0].activate()
    # 获取窗口位置
    left, top, width, height = windows[0].left, windows[0].top, windows[0].width, windows[0].height
    print(left, top, width, height)
    # 移动鼠标到窗口中心
    pyautogui.moveTo(left + width / 2, top + height / 2)
    # 点击窗口
    pyautogui.click()
    pyautogui.typewrite('test', interval=0.01)  # 输入字符串,interval参数为每次键
    pyautogui.write('abcde', interval=0.01)
    pyautogui.press('A')
print(pyautogui.getAllWindows())
