# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-03-17 16:34:43
LastEditTime : 2024-06-19 09:21:07
FilePath     : /CODE/py学习/脚本/键鼠测试.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import pyautogui

screenWidth, screenHeight = pyautogui.size()
print(screenWidth, screenHeight)
currentMouseX, currentMouseY = pyautogui.position()
print(currentMouseX, currentMouseY)
pyautogui.moveTo(200, 150)
pyautogui.click()


""" location1 = pyautogui.locateOnScreen('1.png', confidence=0.7)
pyperclip.copy(i)  # 复制到剪切板
pyautogui.hotkey('ctrl', 'v')  # 粘贴到输入框，回车
pyautogui.press('enter') """
