# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-23 21:02:47
FilePath     : /py学习/pyttx3测试.py
LastEditTime : 2022-11-23 21:07:13
Github       : https://github.com/sandorn/home
==============================================================
可用，速度快，效果一般
'''
import pyttsx3


def say(text):
    engine = pyttsx3.init()
    #调整声音
    voices = engine.getProperty('voices')
    for v in voices:
        print(v)
    voice = engine.getProperty('voice')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    print(voice, rate, volume)
    engine.setProperty('volume', 0.8)
    engine.setProperty('rate', 240)
    engine.say(text)
    engine.save_to_file(text, r'D:\\temp\\test.mp3')
    engine.runAndWait()


if __name__ == "__main__":

    text = '盛唐中融个险机构经营平稳，3家新筹机构，深圳分公司已进入经营阶段，河北分公司、天津分公司筹建工作正在稳步推进中。2022年1-10月公司保险业务共实现保费4.9亿元，同比增长50%。其中寿险新契约规模保费2.66亿元，较上年实现66%的增长，寿险续期保费1.38亿元，团财险保费0.89亿元。'

    say(text)
    pass
