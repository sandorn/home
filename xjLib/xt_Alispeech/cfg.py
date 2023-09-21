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

用户登录名称:sandorn_ram@1915355838841755.onaliyun.com
登录密码:rH17b#9{$gDqRiJXB3flDaWqbMPAEz{n
appKey = 'Ofm34215thIUdSIX'
'AccessKey ID': 'LTAI4G5TRjsGy8BNKPtctjXQ',
'AccessKey Secret': 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
'''
from dataclasses import dataclass
from typing import Any

from nls.token import getToken
from xt_Class import dict_mothed_Mixin
from xt_Thread.Singleon import Singleton_Mixin
from xt_Time import get_10_timestamp

_ACCESS_APPKEY = 'Ofm34215thIUdSIX'
_ACCESS_KeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
_ACCESS_Secret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'


class Constant(Singleton_Mixin):
    '''Constant : 常量参数'''
    __appKey = _ACCESS_APPKEY
    __accessKeyId = _ACCESS_KeyId
    __accessKeySecret = _ACCESS_Secret
    __token = ''
    __ExpireTime = 0

    appKey = property(lambda cls: cls.__appKey)
    accessKeyId = property(lambda cls: cls.__accessKeyId)
    accessKeySecret = property(lambda cls: cls.__accessKeySecret)
    expire_time = property(lambda cls: cls.__ExpireTime)

    def __init__(self):
        self.__renew_token__()

    # token = property(lambda cls: cls.__token)
    # 第二种方法
    @property
    def token(self):
        self.__renew_token__()
        return self.__token

    def __renew_token__(self):
        now = get_10_timestamp()
        # #token生命周期缩短10分钟
        if (self.__ExpireTime - 60 * 10) <= now:
            self.__token = getToken(self.__accessKeyId, self.__accessKeySecret)
        return self.__token


# @dataclass
class SpeechArgs(dict_mothed_Mixin):
    '''TTS参数'''
    long_tts: bool = False
    aformat: str = 'mp3'
    sample_rate: int = 16000
    voice: str = 'ailun'  # aida   # ailun  # kenny  # aijing # aixia
    volume: int = 50
    speech_rate: int = -80
    pitch_rate: int = -80
    text: str = ''
    wait_complete: bool = True
    start_timeout: int = 10
    completed_timeout: int = 60
    ex: dict = {}
    # {'enable_subtitle': True}


@dataclass
class SynResult:
    '''合成结果,暂未使用'''
    id: str = ''
    filename: str = ''
    text: str = ''
    vdata: Any = ''


@dataclass
class TransResult:
    '''识别结果,暂未使用'''
    id: str = ''
    filename: str = ''
    text: str = ''
    vdata: Any = ''


VIOCE = [
    ('知米_多情感', 'zhimi_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知燕_多情感', 'zhiyan_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知贝_多情感', 'zhibei_emo', '多种情感童声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知甜_多情感', 'zhitian_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小云', 'xiaoyun', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
    ('小刚', 'xiaogang', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
    ('若兮', 'ruoxi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思琪', 'siqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
    ('思佳', 'sijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思诚', 'sicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
    ('艾琪', 'aiqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾佳', 'aijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾诚', 'aicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾达', 'aida', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('宁儿', 'ninger', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('瑞琳', 'ruilin', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思悦', 'siyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('艾雅', 'aiya', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾夏', 'aixia', '亲和女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾美', 'aimei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾雨', 'aiyu', '自然女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾悦', 'aiyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾婧', 'aijing', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小美', 'xiaomei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('艾娜', 'aina', '浙普女声', '客服场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('伊娜', 'yina', '浙普女声', '客服场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思婧', 'sijing', '严厉女声', '客服场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
    ('思彤', 'sitong', '儿童音', '童声场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('小北', 'xiaobei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
    ('艾彤', 'aitong', '儿童音', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('艾薇', 'aiwei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('艾宝', 'aibao', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('Harry', 'harry', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Abby', 'abby', '美音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('Andy', 'andy', '美音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Eric', 'eric', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Emily', 'emily', '英音女声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Luna', 'luna', '英音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('Luca', 'luca', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Wendy', 'wendy', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('William', 'william', '英音男声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('Olivia', 'olivia', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('姗姗', 'shanshan', '粤语女声', '方言场景', '标准粤文及粤英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('小玥', 'chuangirl', '四川话女声', '方言场景', '中文及中英文混合场景', '8K/16K', '否', '否', '标准版'),
    ('Lydia', 'lydia', '英中双语女声', '英文场景', '英文及英中文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾硕', 'aishuo', '自然男声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('青青', 'qingqing', '中国台湾话女声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
    ('翠姐', 'cuijie', '东北话女声', '方言场景', '中文场景', '8K/16K', '否', '是', '标准版'),
    ('小泽', 'xiaoze', '湖南重口音男声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
    ('智香', 'tomoka', '日语女声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
    ('智也', 'tomoya', '日语男声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
    ('Annie', 'annie', '美语女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('佳佳', 'jiajia', '粤语女声', '方言场景', '标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('Indah', 'indah', '印尼语女声', '多语种场景', '纯印尼语场景', '8K/16K', '否', '否', '标准版'),
    ('桃子', 'taozi', '粤语女声', '方言场景', '支持标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('柜姐', 'guijie', '亲切女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Stella', 'stella', '知性女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Stanley', 'stanley', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Kenny', 'kenny', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Rosa', 'rosa', '自然女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Farah', 'farah', '马来语女声', '多语种场景', '仅支持纯马来语场景', '8K/16K', '否', '否', '标准版'),
    ('马树', 'mashu', '儿童剧男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小仙', 'xiaoxian', '亲切女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('悦儿', 'yuer', '儿童剧女声', '通用场景', '仅支持纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('猫小美', 'maoxiaomei', '活力女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('知飞', 'zhifei', '激昂解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
    ('知伦', 'zhilun', '悬疑解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
    ('艾飞', 'aifei', '激昂解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('亚群', 'yaqun', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('巧薇', 'qiaowei', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('大虎', 'dahu', '东北话男声', '方言场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('ava', 'ava', '美语女声', '英文场景', '仅支持纯英文场景', '8K/16K', '是', '否', '标准版'),
    ('艾伦', 'ailun', '悬疑解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('杰力豆', 'jielidou', '治愈童声', '童声场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('老铁', 'laotie', '东北老铁', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('老妹', 'laomei', '吆喝女声', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('艾侃', 'aikan', '天津话男声', '方言场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('Tala', 'tala', '菲律宾语女声', '多语种场景', '仅支持菲律宾语场景', '8K/16K', '否', '否', '标准版'),
    ('Tien', 'tien', '越南语女声', '多语种场景', '仅支持越南语场景', '8K/16K', '否', '否', '标准版'),
    ('Becca', 'becca', '美语客服女声', '美式英语', '支持纯英语场景', '8K/16K', '否', '否', '标准版'),
    ('Kyong', 'Kyong', '韩语女声', '韩语场景', '韩语', '8K/16K', '否', '否', '标准版'),
    ('masha', 'masha', '俄语女声', '俄语场景', '俄语', '8K/16K', '否', '否', '标准版'),
]

# 参数说明
# 参数	类型	参数说明
# text	String	要合成的文字。
# aformat	String	合成出来音频的格式，默认为pcm。
# voice	String	发音人，默认为xiaoyun。
# sample_rate	Integer	识别音频采样率，默认值：16000 Hz。
# volume	Integer	音量大小，取值范围0~100，默认值：50。
# speech_rate	Integer	语速，取值范围-500~500，默认值：0。
# pitch_rate	Integer	语调，取值范围-500~500，默认值：0。
# wait_complete	Boolean	是否阻塞到合成完成。
# start_timeout	Integer	和云端连接建立超时，默认值：10秒。
# completed_timeout	Integer	从连接建立到合成完成超时，默认值：60秒
# ping_interval	Integer	Ping包发送间隔，默认值：8秒。无需间隔可设置为0或None。
# ping_timeout	Integer	是否检查Pong包超时，默认值：None。None为不检查Pong包是否超时。
# ex	Dict	用户提供的额外参数，该字典内容会以key:value形式合并进请求的payload段中，详情可参见接口说明章节中的请求数据。
# 返回值：Boolean类型，False为失败，True为成功。
