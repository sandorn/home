# ！/usr/bin/env python
# -*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   wxHtml.py
@Time    :   2019/04/23 14:38:37
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

import wx

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.
app.MainLoop()
