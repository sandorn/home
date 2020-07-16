# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-13 17:20:00
#FilePath     : /xjLib/test/mixin混入编程案例.py
#LastEditTime : 2020-07-14 09:12:46
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class cl:
    pass


# @此类要继承自非object
class Coder(cl):
    def __init__(self, coder_type):
        self.getIde()
        self.writecode()
        print("-----" * 10)

    def writecode(self):
        print("writing code happy with his ide!!!")


class CPluseCoder:
    def getIde(self):
        print("Use VS ide")


class PythonCoder:
    def getIde(self):
        print("Use PC ide")


class SuperCoder:
    def getIde(self):
        print("can Use TEXT and shit any other IDE")


class JavaCoder:
    def getIde(self):
        print("User Eclipse")


class BaseCoder:
    def getIde(self):
        print("asking which ide is the best! any where !!!")


coder_dict = {
    "SuperCoder": SuperCoder,
    "PythonCoder": PythonCoder,
    "CPluseCoder": CPluseCoder,
    "JavaCoder": JavaCoder,
    "BaseCoder": BaseCoder,
}


def get_coder(coder_name=None):
    Coder.__bases__ = (coder_dict.get(coder_name, BaseCoder), )
    if coder_name is None:
        coder_name = "Finder"
    return Coder(coder_name)


# print(11111, Coder.__mro__)
# print(22222, Coder.__base__)
# print(33333, Coder.__bases__)
# Coder.__bases__ += (SuperCoder, )
# print(44444, Coder.__bases__)
# print(55555, Coder.__mro__)
get_coder("SuperCoder")
get_coder("PythonCoder")
get_coder("CPluseCoder")
get_coder("JavaCoder")
get_coder()
