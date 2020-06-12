# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-09 17:25:36
#FilePath     : /UI学习/gtk-练习-1.py
#LastEditTime : 2020-06-11 14:23:44
#Github       : https://github.com/sandorn/home
#==============================================================
'''

TITLE = "Center Window"
DESCRIPTION = """
This window is located in the middle of screen,and set the window size
"""
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MyWindow(Gtk.Window):
    WIDTH, HEIGHT = 200, 100

    def __init__(self):
        Gtk.Window.__init__(self, title="Center Window")
        self.set_size_request(self.WIDTH, self.HEIGHT)
        self.move((Gdk.Screen.width() - self.WIDTH) / 2, (Gdk.Screen.height() - self.HEIGHT) / 2)
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()

    @staticmethod
    def on_button_clicked(widget):
        print("Hello World")


if __name__ == "__main__":
    win = MyWindow()
