#  !/usr/bin/env python
#  -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-07-14 18:50:01
#FilePath     : /xjLib/test/利用abc模块实现抽象类.py
#LastEditTime : 2020-07-14 18:55:25
# Github       : https://github.com/sandorn/home
# ==============================================================
'''
from abc import ABCMeta, abstractmethod


class All_file(metaclass=ABCMeta):

    all_type = 'file'

    @abstractmethod  #  定义抽象方法，无需实现功能
    def read(self):
        '子类必须定义读功能'
        pass

    @abstractmethod  # 定义抽象方法，无需实现功能
    def write(self):
        '子类必须定义写功能'
        pass


class Txt(All_file):  # 子类继承抽象类，但是必须定义read和write方法
    def read(self):
        print('文本数据的读取方法')

    def write(self):
        print('文本数据的读取方法')


class Sata(All_file):  # 子类继承抽象类，但是必须定义read和write方法
    def read(self):
        print('硬盘数据的读取方法')

    def write(self):
        print('硬盘数据的读取方法')


class Process(All_file):  # 子类继承抽象类，但是必须定义read和write方法
    def read(self):
        print('进程数据的读取方法')

    def write(self):
        print('进程数据的读取方法')


wenbenwenjian = Txt()
yingpanwenjian = Sata()
jinchengwenjian = Process()

#  这样大家都是被归一化了,也就是一切皆文件的思想

wenbenwenjian.read()
yingpanwenjian.write()
jinchengwenjian.read()

print(wenbenwenjian.all_type)
print(yingpanwenjian.all_type)
print(jinchengwenjian.all_type)
