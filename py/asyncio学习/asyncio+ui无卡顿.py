# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-08 10:55:08
@LastEditors: Even.Sand
@LastEditTime: 2020-04-21 16:04:14
https://blog.csdn.net/qq_27825451/article/details/86483493
'''

import asyncio
import threading
import time
import tkinter as tk  # 导入 Tkinter 库


class Form:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('500x300')
        self.root.title('窗体程序')  # 设置窗口标题

        self.button = tk.Button(
            self.root, text="开始计算", command=self.change_form_state)
        self.label = tk.Label(master=self.root, text="等待计算结果")
        self.text1 = tk.Entry(self.root, width=10)
        self.text2 = tk.Entry(self.root, width=10)
        # autoseparators, height, maxundo,spacing1, spacing2, spacing3,state, tabs, undo, width, wrap,

        self.text1.pack()
        self.text2.pack()
        self.button.pack()
        self.label.pack()  # Label内容content区域放置位置，自动调节尺寸
        # 放置lable的方法有：1）l.pack(); 2)l.place();

        self.root.mainloop()

    async def calculate(self):
        await asyncio.sleep(0.3)
        self.label["text"] = str(int(self.text1.get()) * int(self.text2.get()))

    def get_loop(self, loop):
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def change_form_state(self):
        coroutine1 = self.calculate()
        new_loop = asyncio.new_event_loop()
        # !在当前线程下创建时间循环，（未启用），在start_loop里面启动它
        t = threading.Thread(target=self.get_loop, args=(new_loop,))
        # !通过当前线程开启新的线程去启动事件循环
        t.start()

        asyncio.run_coroutine_threadsafe(coroutine1,
                                         new_loop)  # 这几个是关键，代表在新线程中事件循环不断“游走”执行

    def __del__(self):
        self.root.quit()


if __name__ == '__main__':
    form = Form()
