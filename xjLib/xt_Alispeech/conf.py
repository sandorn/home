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

from ali_speech._create_token import AccessToken
from nls.token import getToken
from xt_Class import dict_mothed_Mixin, readonly
from xt_Singleon import Singleton_Mixin
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
        # #token生命周期缩短10分钟
        if (self.__expire_time - 60 * 10) <= now:
            print(self.__expire_time)
            self.__token, self.__expire_time = getToken(self.__accessKeyId, self.__accessKeySecret)
        return self.__expire_time


@dataclass
class SpeechArgs(dict_mothed_Mixin):
    '''TTS参数'''

    long_tts: bool = False
    aformat: str = 'wav'
    sample_rate: int = 16000
    voice: str = 'Aida'  # aida   # ailun  # kenny
    volume: int = 50
    speech_rate: int = 0
    pitch_rate: int = 0
    text: str = ''

    wait_complete: bool = True
    start_timeout: int = 10
    completed_timeout: int = 60
    ex: dict = None
    # {'enable_subtitle': True}


@dataclass
class SynResult:
    '''合成结果'''
    task_id: str = ''
    voicedata: Any = ''
    filename: str = ''
    text: str = ''


@dataclass
class TransResult:
    '''识别结果'''
    task_id: str = ''
    voicedata: Any = ''
    filename: str = ''
    text: str = ''


def handle_ex_nsx_result(res):
    '''处理 ex_NSR ex_NST 结果'''
    dictMerged = {}
    res_list = []
    for key, values in res.items():
        _dict = eval(values)

        dictMerged[key] = dict(_dict['header'], **_dict['payload'])
        res_list.append((key, dictMerged[key]['result']))
    # print(dictMerged)
    # print(res_list)
    return res_list, dictMerged


'''
字级别音素边界接口：语音合成服务在输出音频的同时，可输出每个汉字/英文单词在音频中的时间位置，即时间戳。该时间信息可用于驱动虚拟人口型、做视频配音字幕等。详情请参见语音合成时间戳功能介绍。
文学场景相关发音人信息，请参见接口说明。
如需使用Android或iOS SDK，请参见移动端接口说明。

名称	voice参数值	类型	适用场景	支持语言	支持采样率（Hz）	支持时间戳（字级别音素边界）接口	支持儿化音	声音品质
知米_多情感	zhimi_emo	多种情感女声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
知燕_多情感	zhiyan_emo	多种情感女声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
知贝_多情感	zhibei_emo	多种情感童声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
知甜_多情感	zhitian_emo	多种情感女声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
小云	xiaoyun	标准女声	通用场景	中文及中英文混合场景	8K/16K	否	否	lite版
小刚	xiaogang	标准男声	通用场景	中文及中英文混合场景	8K/16K	否	否	lite版
若兮	ruoxi	温柔女声	通用场景	中文及中英文混合场景	8K/16K/24K	否	否	标准版
思琪	siqi	温柔女声	通用场景	中文及中英文混合场景	8K/16K/24K	是	否	标准版
思佳	sijia	标准女声	通用场景	中文及中英文混合场景	8K/16K/24K	否	否	标准版
思诚	sicheng	标准男声	通用场景	中文及中英文混合场景	8K/16K/24K	是	否	标准版
艾琪	aiqi	温柔女声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾佳	aijia	标准女声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾诚	aicheng	标准男声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾达	aida	标准男声	通用场景	中文及中英文混合场景	8K/16K	是	否	标准版
宁儿	ninger	标准女声	通用场景	纯中文场景	8K/16K/24K	否	否	标准版
瑞琳	ruilin	标准女声	通用场景	纯中文场景	8K/16K/24K	否	否	标准版
思悦	siyue	温柔女声	客服场景	中文及中英文混合场景	8K/16K/24K	否	否	标准版
艾雅	aiya	严厉女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾夏	aixia	亲和女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾美	aimei	甜美女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾雨	aiyu	自然女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾悦	aiyue	温柔女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
艾婧	aijing	严厉女声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
小美	xiaomei	甜美女声	客服场景	中文及中英文混合场景	8K/16K/24K	否	否	标准版
艾娜	aina	浙普女声	客服场景	纯中文场景	8K/16K	是	否	标准版
伊娜	yina	浙普女声	客服场景	纯中文场景	8K/16K/24K	否	否	标准版
思婧	sijing	严厉女声	客服场景	纯中文场景	8K/16K/24K	是	否	标准版
思彤	sitong	儿童音	童声场景	纯中文场景	8K/16K/24K	否	否	标准版
小北	xiaobei	萝莉女声	童声场景	纯中文场景	8K/16K/24K	是	否	标准版
艾彤	aitong	儿童音	童声场景	纯中文场景	8K/16K	是	否	标准版
艾薇	aiwei	萝莉女声	童声场景	纯中文场景	8K/16K	是	否	标准版
艾宝	aibao	萝莉女声	童声场景	纯中文场景	8K/16K	是	否	标准版
Harry	harry	英音男声	英文场景	英文场景	8K/16K	否	否	标准版
Abby	abby	美音女声	英文场景	英文场景	8K/16K	是	否	标准版
Andy	andy	美音男声	英文场景	英文场景	8K/16K	否	否	标准版
Eric	eric	英音男声	英文场景	英文场景	8K/16K	否	否	标准版
Emily	emily	英音女声	英文场景	英文场景	8K/16K	否	否	标准版
Luna	luna	英音女声	英文场景	英文场景	8K/16K	是	否	标准版
Luca	luca	英音男声	英文场景	英文场景	8K/16K	否	否	标准版
Wendy	wendy	英音女声	英文场景	英文场景	8K/16K/24K	否	否	标准版
William	william	英音男声	英文场景	英文场景	8K/16K/24K	否	否	标准版
Olivia	olivia	英音女声	英文场景	英文场景	8K/16K/24K	否	否	标准版
姗姗	shanshan	粤语女声	方言场景	标准粤文及粤英文混合场景	8K/16K/24K	否	否	标准版
小玥	chuangirl	四川话女声	方言场景	中文及中英文混合场景	8K/16K	否	否	标准版
Lydia	lydia	英中双语女声	英文场景	英文及英中文混合场景	8K/16K	是	否	标准版
艾硕	aishuo	自然男声	客服场景	中文及中英文混合场景	8K/16K	是	否	标准版
青青	qingqing	中国台湾话女声	方言场景	中文场景	8K/16K	否	否	标准版
翠姐	cuijie	东北话女声	方言场景	中文场景	8K/16K	否	是	标准版
小泽	xiaoze	湖南重口音男声	方言场景	中文场景	8K/16K	否	否	标准版
智香	tomoka	日语女声	多语种场景	日文场景	8K/16K	是	否	标准版
智也	tomoya	日语男声	多语种场景	日文场景	8K/16K	是	否	标准版
Annie	annie	美语女声	英文场景	英文场景	8K/16K	是	否	标准版
佳佳	jiajia	粤语女声	方言场景	标准粤文（简体）及粤英文混合场景	8K/16K	是	否	标准版
Indah	indah	印尼语女声	多语种场景	纯印尼语场景	8K/16K	否	否	标准版
桃子	taozi	粤语女声	方言场景	支持标准粤文（简体）及粤英文混合场景	8K/16K	是	否	标准版
柜姐	guijie	亲切女声	通用场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
Stella	stella	知性女声	通用场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
Stanley	stanley	沉稳男声	通用场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
Kenny	kenny	沉稳男声	通用场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
Rosa	rosa	自然女声	通用场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
Farah	farah	马来语女声	多语种场景	仅支持纯马来语场景	8K/16K	否	否	标准版
马树	mashu	儿童剧男声	通用场景	支持中文及中英文混合场景	8K/16K	是	否	标准版
小仙	xiaoxian	亲切女声	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
悦儿	yuer	儿童剧女声	通用场景	仅支持纯中文场景	8K/16K	是	否	标准版
猫小美	maoxiaomei	活力女声	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
知飞	zhifei	激昂解说	超高清场景	支持中文及中英文混合场景	8K/16K	是	否	精品版
知伦	zhilun	悬疑解说	超高清场景	支持中文及中英文混合场景	8K/16K	是	否	精品版
艾飞	aifei	激昂解说	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
亚群	yaqun	卖场广播	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
巧薇	qiaowei	卖场广播	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
大虎	dahu	东北话男声	方言场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
ava	ava	美语女声	英文场景	仅支持纯英文场景	8K/16K	是	否	标准版
艾伦	ailun	悬疑解说	直播场景	支持中文及中英文混合场景	8K/16K	是	是	标准版
杰力豆	jielidou	治愈童声	童声场景	仅支持纯中文场景	8K/16K	是	是	标准版
老铁	laotie	东北老铁	直播场景	仅支持纯中文场景	8K/16K	是	是	标准版
老妹	laomei	吆喝女声	直播场景	仅支持纯中文场景	8K/16K	是	是	标准版
艾侃	aikan	天津话男声	方言场景	仅支持纯中文场景	8K/16K	是	是	标准版
Tala	tala	菲律宾语女声	多语种场景	仅支持菲律宾语场景	8K/16K	否	否	标准版
Tien	tien	越南语女声	多语种场景	仅支持越南语场景	8K/16K	否	否	标准版
Becca	becca	美语客服女声	美式英语	支持纯英语场景	8K/16K	否	否	标准版
Kyong	Kyong	韩语女声	韩语场景	韩语	8K/16K	否	否	标准版
masha	masha	俄语女声	俄语场景	俄语	8K/16K	否	否	标准版


多情感声音支持说明
只有多情感发音人模型才可以支持多情感选择。多情感声音支持的情感如下表所示，每个音色支持的情感分类不完全相同，主要包括以下几种：neutral（中性）、happy（开心）、angry（生气）、sad（悲伤）、fear（害怕）、hate（憎恨）、surprise（惊讶）、arousal（激动）等。
音色名	voice参数值	情感分类（emotion category）
知米_多情感	zhimi_emo	angry, fear, happy, hate, neutral, sad, surprise
知燕_多情感	zhiyan_emo	neutral，happy，angry，sad，fear，hate，surprise，arousal
知贝_多情感	zhibei_emo	neutral，happy，angry，sad，fear，hate，surprise
知甜_多情感	zhitian_emo	neutral，happy，angry，sad，fear，hate，surprise
'''
