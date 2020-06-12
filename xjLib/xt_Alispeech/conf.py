# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 16:57:09
#FilePath     : /xjLib/xt_Alispeech/conf.py
#LastEditTime : 2020-06-11 15:12:06
#Github       : https://github.com/sandorn/home
#==============================================================

用户登录名称 sandorn_ram@1915355838841755.onaliyun.com
登录密码 rH17b#9{$gDqRiJXB3flDaWqbMPAEz{n
user1 = {
    'AccessKey_ID': 'LTAI4G5TRjsGy8BNKPtctjXQ',
    'AccessKey_Secret': 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
}
user2 = {
    'AccessKey_ID': 'LTAI4GAdnViJdPBCpaTuaUXM',
    'AccessKey_Secret': 'NJP6DZR0pWtK3Ze3cpi9XqhLeEzNdg'
}
'''

from ali_speech._create_token import AccessToken
from xt_Time import get_10_timestamp
from xt_String import class_to_dict


class Constant:
    '''常量'''
    __appKey = 'Ofm34215thIUdSIX'
    __accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
    __accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
    __token = ''
    __expire_time = 0

    def __init__(self):
        '''更新Constant.获取token'''
        now = get_10_timestamp()
        # #token生命周期缩短3分钟
        if (Constant.__expire_time - 60 * 3) <= now:
            Constant.__token, Constant.__expire_time = AccessToken.create_token(Constant.__accessKeyId, Constant.__accessKeySecret)

    appKey = property(lambda cls: cls.__appKey)
    accessKeyId = property(lambda cls: cls.__accessKeyId)
    accessKeySecret = property(lambda cls: cls.__accessKeySecret)
    token = property(lambda cls: cls.__token)
    expire_time = property(lambda cls: cls.__expire_time)

    # 第二种方法
    # @property
    # def token(self):
    #     Constant.__gettoken__()
    #     return Constant.__token


class SpeechArgs:
    '''默认参数'''
    appkey = Constant().appKey
    # #导入此库就立即加载token
    token = Constant().token
    format = 'wav'
    sample_rate = 16000
    voice = 'Aida'
    volume = 100
    speech_rate = 0
    pitch_rate = 0


class SynResult:
    '''合成结果'''

    def __init__(self):
        self.response = ''
        self.filename = ''
        self.callback = ''

    def __repr__(self):
        return f'filename:<{self.filename}>,response:{self.response},callback:<{self.callback}>'


class TransResult:
    '''识别结果'''

    def __init__(self):
        self.text = ''
        self.name = ''
        self.task_id = ''
        self.response = ''

    def __repr__(self):
        return f'text:<{self.text}>,task_id:<{self.task_id}>'


if __name__ == "__main__":
    print(Constant().token)
    c1 = Constant()
    print(c1.token)
    c2 = Constant()
    print(c2.accessKeyId)
    print(Constant().appKey)
    # from xt_String import class_to_dict
    # body_dict = class_to_dict(SpeechArgs())
    # body_dict['format'] = 'format'  # #更新
    # body_dict['text'] = 'text'  # 添加
    # print(body_dict)

    pass
