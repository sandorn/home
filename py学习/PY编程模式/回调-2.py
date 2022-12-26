# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-25 15:51:34
LastEditTime : 2022-12-25 15:53:26
FilePath     : /py学习/PY编程模式/回调-2.py
Github       : https://github.com/sandorn/home
==============================================================
'''


class CallbackBase:

    def __init__(self):
        self.__callbackMap = {}
        for k in (getattr(self, x) for x in dir(self)):
            if hasattr(k, "bind_to_event"):
                self.__callbackMap.setdefault(k.bind_to_event, []).append(k)
            elif hasattr(k, "bind_to_event_list"):
                for j in k.bind_to_event_list:
                    self.__callbackMap.setdefault(j, []).append(k)

    @staticmethod
    def callback(event):

        def f(g, ev=event):
            g.bind_to_event = ev
            return g

        return f

    @staticmethod
    def callbacklist(eventlist):

        def f(g, evl=eventlist):
            g.bind_to_event_list = evl
            return g

        return f

    def dispatch(self, event):
        l = self.__callbackMap[event]
        f = lambda *args, **kargs: \
            map(lambda x: x(*args, **kargs), l)
        return f


class MyClass(CallbackBase):
    EVENT1 = 1
    EVENT2 = 2

    @CallbackBase.callback(EVENT1)
    def handler1(self, param=None):
        print("handler1 with param: %s" % str(param))
        return None

    @CallbackBase.callbacklist([EVENT1, EVENT2])
    def handler2(self, param=None):
        print("handler2 with param: %s" % str(param))
        return None

    def run(self, event, param=None):
        self.dispatch(event)(param)


if __name__ == "__main__":
    a = MyClass()
    a.run(MyClass.EVENT1, 'mandarina')
    a.run(MyClass.EVENT2, 'naranja')
