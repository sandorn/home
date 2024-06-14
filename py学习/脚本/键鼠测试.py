# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-17 16:34:43
LastEditTime : 2023-03-17 16:35:00
FilePath     : /CODE/py学习/脚本/键鼠测试.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import pyautogui

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)
currentMouseX, currentMouseY = pyautogui.position()
print(currentMouseX, currentMouseY)
pyautogui.moveTo(100, 150)
pyautogui.click()
