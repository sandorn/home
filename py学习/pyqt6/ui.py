# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-16 13:34:02
LastEditTime : 2024-06-16 13:34:08
FilePath     : /CODE/py学习/pyqt6/ui.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication([])
window = QMainWindow()
button = QPushButton('Click me!')
window.setCentralWidget(button)
window.show()
sys.exit(app.exec())
