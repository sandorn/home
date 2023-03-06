# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-03-02 17:18:03
FilePath     : /CODE/py学习/UI学习/wx库窗口.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import wx
#import wx.xrc
from system_hotkey import SystemHotkey


class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(1080, 720)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.m_button1 = wx.Button(self, wx.ID_ANY, u"MyButton", wx.Point(-1, -1), wx.DefaultSize, 0)
        bSizer1.Add(self.m_button1, 0, wx.ALL, 5)
        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer1.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1), wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        m_choice1Choices = []
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer1.Add(self.m_choice1, 0, wx.ALL, 5)

        self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_checkBox1, 0, wx.ALL, 5)

        self.m_slider1 = wx.Slider(self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL)
        bSizer1.Add(self.m_slider1, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.m_menubar1 = wx.MenuBar(0)
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem(self.m_menu1, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu1.Append(self.m_menuItem1)

        self.m_menubar1.Append(self.m_menu1, u"MyMenu")

        self.SetMenuBar(self.m_menubar1)

        self.m_statusBar1 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.showMessage)
        hk1, hk2 = SystemHotkey(), SystemHotkey()
        hk1.register(('control', '1'), callback=lambda x: self.iprint("1111111111111111111!"))
        hk2.register(('control', '2'), callback=lambda x: print("2222222222222222222!"))

    def iprint(self, *args):
        print(*args)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def showMessage(self, event):
        print('showMessage')
        event.Skip()


if __name__ == "__main__":
    app = wx.App()  # 实例化一个主循环
    frame = MainWindow(None)  # 实例化一个窗口
    frame.Show()  # 调用窗口展示功能
    app.MainLoop()  # 启动主循环
