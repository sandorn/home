# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
一个例子走近 Python 的 Mixin 类：利用 Python 多继承的魔力_(ÒωÓױ)-CSDN博客_python mixin
https://blog.csdn.net/u012814856/article/details/81355935?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.nonecase
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-10 12:15:19
#FilePath     : /xjLib/test/Mixin 类的实例.py
#LastEditTime : 2020-07-10 12:15:32
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class Displayer():
    def display(self, message):
        print(message)


class LoggerMixin():
    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        super().display(message)
        self.log(message)


class MySubClass(LoggerMixin, Displayer):
    def log(self, message):
        super().log(message, filename='subclasslog.txt')


subclass = MySubClass()
subclass.display("This string will be shown and logged in subclasslog.txt")
