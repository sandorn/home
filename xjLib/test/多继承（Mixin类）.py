# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-10 12:20:30
#FilePath     : /xjLib/test/多继承（Mixin类）.py
#LastEditTime : 2020-07-10 12:21:02
#Github       : https://github.com/sandorn/home
#==============================================================
'''


class Document:  # 第三方库，不允许修改
    def __init__(self, content):
        print('Dcoument __init__')
        self.content = content


class Word(Document):
    pass  # 第三方库，不允许修改


class Pdf(Document):
    pass  # 第三方库，不允许修改


class PrintableMixin:
    def print(self):
        print(self.content, 'Mixin')


class PrintableWord(PrintableMixin, Word):
    pass


print(PrintableWord.__dict__)  # {'__module__': '__main__', '__doc__': None}
print(PrintableWord.mro())
# [<class '__main__.PrintableWord'>, <class '__main__.PrintableMixin'>, <class '__main__.Word'>, <class '__main__.Document'>, <class 'object'>]

pw = PrintableWord('test string')
pw.print()  # test string Mixin


class SuperPrintableMixin(PrintableMixin):
    def print(self):
        print('-' * 20)  # 打印增强
        super().print()
        print('-' * 20)  # 打印增强


# PrintableMixin类的继承
class SuperprintablePdf(SuperPrintableMixin, Pdf):
    pass


print(SuperprintablePdf.__dict__)  # {'__module__': '__main__', '__doc__': None}
print(SuperprintablePdf.mro())
# [<class '__main__.SuperprintablePdf'>, <class '__main__.SuperPrintableMixin'>,\
# <class '__main__.PrintableMixin'>, <class '__main__.Pdf'>, \
# <class '__main__.Document'>, <class 'object'>]

spp = SuperprintablePdf('super print pdf')
spp.print()
# --------------------
# super print pdf Mixin
# --------------------
