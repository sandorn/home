# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Software :   VSCode
@File     :   语法糖.py
@Time     :   2019/05/07 17:45:26
@Author   :   Even Sand
@Version  :   1.0
@Contact  :   sandorn@163.com
@License  :   (C)Copyright 2009-2019, NewSea
python @property，@staticmethod及@classmethod内置装饰器小结 - 大魔王的博客 - CSDN博客
https://blog.csdn.net/weixin_43533825/article/details/87866909
'''


class user(object):

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value == "":
            raise ValueError(u"名字不能为空")
        self._username = value


if __name__ == '__main__':
    demo = user()
    demo.username = "sdf"
    print(demo.username)
    demo.username = ''
    print(demo.username)
