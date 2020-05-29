# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-25 11:14:04
#LastEditTime : 2020-05-25 12:31:52
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
Python语音合成_weixin_33748818的博客-CSDN博客
https://blog.csdn.net/weixin_33748818/article/details/94197901

Python3 语音合成——pyttsx3 从文本到语音_python_geeknuo的博客-CSDN博客
https://blog.csdn.net/u014663232/article/details/103834543

'''

import win32com.client
import time
spk = win32com.client.Dispatch("SAPI.SpVoice")
for i in range(100):
    pass
    # spk.Speak(u"%d你好" % i)
    # time.sleep(1)

import pyttsx3

say = pyttsx3.init()  # 创建pyttsx对象，并初始化对象
rate = say.getProperty('rate')  # 获取当前语速属性的值
say.setProperty('rate', rate - 20)  # 设置语速属性为当前语速减20
msg = '''今天的天气真好，出去打球吧'''  # 需要合成的文字

say.say(msg)  # 合成并播放语音
say.runAndWait()  # 等待语音播放完
