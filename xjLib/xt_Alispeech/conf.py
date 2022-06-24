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
#LastEditTime : 2020-07-22 13:27:36
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
from xt_Class import readonly, dict_mothed_Mixin
from typing import Any
from dataclasses import dataclass  #, field
from xt_Singleon import Singleton_Mixin


class Constant(Singleton_Mixin):
    __appKey = 'Ofm34215thIUdSIX'
    __accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
    __accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
    __token = ''
    __expire_time = 0

    appKey = property(lambda cls: cls.__appKey)
    accessKeyId = property(lambda cls: cls.__accessKeyId)
    accessKeySecret = property(lambda cls: cls.__accessKeySecret)
    expire_time = property(lambda cls: cls.__expire_time)

    # token = property(lambda cls: cls.__token)
    def __init__(self):
        self.__renew_token__()

    # 第二种方法
    @property
    def token(self):
        self.__renew_token__()
        return self.__token

    def __renew_token__(self):
        now = get_10_timestamp()
        # #token生命周期缩短30分钟
        if (self.__expire_time - 60 * 30) <= now:
            self.__token, self.__expire_time = AccessToken.create_token(self.__accessKeyId, self.__accessKeySecret)
        return self.__expire_time


# (init=False) 不做初始化，避免生成.__dict__
@dataclass
class SpeechArgs(dict_mothed_Mixin):
    '''默认参数'''
    appkey = readonly('_appkey')
    token = readonly('_token')

    _appkey: str = Constant().appKey
    _token: str = Constant().token
    format: str = 'wav'
    sample_rate: int = 16000
    voice: str = 'Aida'
    volume: int = 100
    speech_rate: int = 0
    pitch_rate: int = 0


@dataclass
class SynResult:
    '''合成结果'''
    response: Any = ''
    filename: str = ''
    callback: str = ''


@dataclass
class TransResult:
    '''识别结果'''
    text: str = ''
    name: str = ''
    task_id: str = ''
    response: Any = ''


if __name__ == "__main__":
    print(Constant(), 22222, id(Constant()))
    print(SpeechArgs())
    print(SynResult())
    print(TransResult())
    print(22222, id(Constant()), Constant().__dict__)
    a = Constant()
    print(22222, id(a))
    print(SynResult().__dict__)
    print(TransResult().__dict__)
