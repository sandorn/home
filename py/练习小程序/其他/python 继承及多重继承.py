# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-03 14:56:24
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 15:02:46
'''


class Father(object):
    def __init__(self, money):
        self.money = money
        print('money:', money)

    def play(self):
        print('father play with me')


class Mother(object):
    def __init__(self, face):
        self.face = face
        print('face:', face)

    def play(self):
        print('mother go shopping with me')


class Child(Mother, Father):  # !按照继承顺序,Mother在前，play调用Mother
    def __init__(self, money, face):
        Father.__init__(self, money)
        Mother.__init__(self, face)


def main():
    c = Child(100, 300)
    c.play()  # !按照继承顺序


if __name__ == '__main__':
    main()
