# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 16:57:09
#FilePath     : /xjLib/xt_Alispeech/config.py
#LastEditTime : 2020-06-09 11:23:57
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


class Constant:
    '''全局常量'''
    appKey = 'Ofm34215thIUdSIX'
    accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
    accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
    token = ''
    expire_time = 0


def GetToken():
    '''获取token,更新Constant'''
    access_key_id = Constant.accessKeyId
    access_key_secret = Constant.accessKeySecret
    now = get_10_timestamp()

    if Constant.expire_time > now:
        return Constant.token, Constant.expire_time
    else:
        Constant.token, Constant.expire_time = AccessToken.create_token(access_key_id, access_key_secret)

    return Constant.token, Constant.expire_time


class SpeechReqMeta:
    '''默认参数'''
    appkey = Constant.appKey
    # #导入此库就立即加载token
    token = Constant.token or GetToken()[0]
    format = 'wav'
    sample_rate = 16000
    voice = 'Aida'
    volume = 100
    speech_rate = 0
    pitch_rate = 0


class SynResult:
    '''合成结果'''
    response = ''
    filename = ''
    callback = ''

    def __repr__(self):
        return f'filename:<{self.filename}>,response:{self.response},callback:<{self.callback}>'


class TransResult:
    '''识别结果'''
    text = ''
    name = ''
    task_id = ''
    response = ''

    def __repr__(self):
        return f'text:<{self.text}>,task_id:<{self.task_id}>'
