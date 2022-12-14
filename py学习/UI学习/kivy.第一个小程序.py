# !/usr/bin/env python
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-10 16:36:09
@LastEditors: Even.Sand
@LastEditTime: 2020-03-10 16:44:23
'''
# TestApp().run()
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput


class TestApp(App):
    def build(self):
        return Button(text='iPaoMi')


kivy.require('1.11.1')  # 用你当前的kivy版本替换


class MyApp(App):
    def build(self):
        return Label(text='Hello world')


kivy.require("1.11.1")

fonts = "./SourceHanSerifSC-Regular.otf"

# 页面一


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.add_widget(Label(text="号码:", font_name=fonts))
        self.ip = TextInput(multiline=False, font_name=fonts)
        self.add_widget(self.ip)
        self.add_widget(Label(text="说明:", font_name=fonts))

        self.add_widget(Label(text="号段：", font_name=fonts))
        self.port = TextInput(multiline=False, font_name=fonts)
        self.add_widget(self.port)
        self.add_widget(Label(text="说明:", font_name=fonts))

        self.add_widget(Label(text="Sheet个数：", font_name=fonts))
        self.name = TextInput(multiline=False, font_name=fonts)
        self.add_widget(self.name)
        self.add_widget(Label(text="说明:", font_name=fonts))

        self.join = Button(text="运行", font_name=fonts)
        self.join.bind(on_press=self.join_button)  # 点击它就会弹出另一个页面
        self.add_widget(Label())
        self.add_widget(Label())
        self.add_widget(self.join)

    def join_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        name = self.name.text
        info = f"{port} {ip} {name}"
        chat_app.info_page.update_info(info)  # 调用页面二的方法 赋值显示
        chat_app.screen_manager.current = "Info"  # 加载页面渲染信息


# 页面二
class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=30, font_name=fonts)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)

# 程序对象


class EpicApp(App):
    def build(self):
        self.screen_manager = ScreenManager()  # 渲染的页面==>屏幕==>屏幕管理器

        self.connect_page = ConnectPage()   # 页面一
        screen = Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.info_page = InfoPage()  # 页面二
        screen = Screen(name="Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    chat_app = EpicApp()
    chat_app.run()
