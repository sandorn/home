# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 16:57:09
#LastEditTime : 2020-06-03 18:40:58
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
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
from xt_String import get_10_timestamp


# #全局常量
class Constant:
    appKey = 'Ofm34215thIUdSIX'
    accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
    accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
    token = ''
    expire_time = 0


def GetToken():
    access_key_id = Constant.accessKeyId
    access_key_secret = Constant.accessKeySecret
    now = get_10_timestamp()

    if Constant.expire_time > now:
        return Constant.token, Constant.expire_time
    else:
        Constant.token, Constant.expire_time = AccessToken.create_token(access_key_id, access_key_secret)

    return Constant.token, Constant.expire_time


# #默认参数
class SpeechReqMeta:

    appkey = Constant.appKey
    token = Constant.token or GetToken()[0]
    format = 'wav'
    sample_rate = 16000
    voice = 'Aida'
    volume = 100
    speech_rate = 0
    pitch_rate = 0
