# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-06-11 12:27:03
#FilePath     : /xjLib/test/alispeech-test.py
#LastEditTime : 2020-06-23 12:11:03
# Github       : https://github.com/sandorn/home
# ==============================================================
'''
from xt_Alispeech import synthesizeClass, ReqLongSynthesizer, APITransUrl, PostTransFile, TranscriberProcess, ReqSynthesizer
from xt_String import string_split_limited_list
from xt_Alispeech.xt_Pygame import pygame_play, ReqSynthesizer_Thread_read, Synt_Thread_read

longtext = '''
        根据保险专业中介机构公司治理专项视频会议要求，我司按照会议安排，对公司相关业务及经营独立性展开全面自查自纠，现将有关工作情况汇报如下：
        一、股东业务自查情况：
        股东公司业务约占我司全部业务的70%，主要为年金险和健康险。股东业务开展基于盛唐融信与股东公司之间签订的代理合同，盛唐融信完全在代理合同框架内开展股东产品代理活动。
        股东公司与盛唐签订的代理协议约定：10年期年金险手续费93%，20年期健康险手续费率133%。手续费符合市场水平，在同业市场中属于中等。
        自2019年1月1日至2020年4月30日，公司与股东间业务共计规模保费1亿9247.8万元，标准保费1亿2766.68万元，股东业务真实、合规；手续费结算共计1亿2196万元，综合实际结算手续费率约95.5%。
        手续费结算符合双方签署的保险专业代理产品协议，手续费结算规范、合理。公司与股东公司之间无虚挂业务、套取费用行为。
    '''

ssml_text = '''
        <speak>
            相传北宋年间，
            <say-as interpret-as="date"> 1121-10-10 </say-as>
            <say-as interpret-as="address">，开封城</say-as>
            郊外的早晨笼罩在一片
            <sub alias="双十一">11.11</sub>
            前买买买的欢乐海洋中。一支运货的骡队刚进入城门
            <soundEvent src="https://gw.alipayobjects.com/os/bmw-prod/9a4c57cc-caec-46aa-b4fa-d1e2dd0187d0.wav"/>
            一个肤白貌美
            <phoneme alphabet="py" ph="de5">地</phoneme>
            姑娘便拦下第一排的小哥<say-as interpret-as="name">阿发。</say-as>
        </speak>
        <speak voice="xiaomei">
            “亲，本店今日特惠，鞋履全场
            <say-as interpret-as="digits">199</say-as>
            减
            <say-as interpret-as="cardinal">100</say-as>，
            走过路过不要错过”。
        </speak>
        <speak voice="sicheng" rate="150">
            “不啦不啦，赶着上货，已经
            <say-as interpret-as="time">09:59:59</say-as>
            了，再晚就供应链断裂了”。
            </speak>
            <speak>
            <say-as interpret-as="name">阿发</say-as>
            擦了擦汗，带着运货队伍，径直穿过闹巷，耳边充斥着各种叫卖声：
        </speak>
        <speak voice="ninger" rate="200">
            最新花色现染布匹，买两尺送一尺；
        </speak>
        <speak voice="xiaobei">
            爆款纱帽头盔，7天无理由退货；
        </speak>
        <speak voice="sijia">
            专治大小方脉，调理男人妇人疑难杂症。
        </speak>
        <speak>
            突然，一匹马不知怎么受了惊，在路上嘶鸣狂奔
            <soundEvent src="https://gw.alipayobjects.com/os/bmw-prod/520dcd7c-19b8-43fb-bdd9-1c1a8ea6434d.wav"/>
            一个孩子也吓坏了，跌跌撞撞地扑向大人怀里
            <break time="50ms"/>大喊道：
        </speak>
        <speak voice="sitong" rate="150">
            “妈妈，妈妈！”
        </speak>
        <speak>
            这时，
            <say-as interpret-as="name">阿发</say-as>
            心想
        </speak>
        <speak effect="robot" pitch="-100">
            “吓死宝宝了！”
        </speak>
        <speak>
            于是他赶紧捂住了
            <phoneme alphabet="py" ph="he2 bao1">钱包</phoneme>，
            继续赶路送货。一路上，
            <say-as interpret-as="address">开封城</say-as>
            的繁荣景象给
            <say-as interpret-as="name">阿发</say-as>
            留下了深刻的印象。
        </speak>
        <speak bgm="https://gw.alipayobjects.com/os/bmw-prod/46e7e489-6007-4d6b-b079-8cba944c2b9c.wav" backgroundMusicVolume="30" rate="-200">
            物换星移，繁华落尽，于是他在购物狂欢之余握起画笔，勾勒出一幅长卷，并命名为《清明上河图》。
        </speak>
    '''

audiofilepath = "D:/Personal/Downloads/nls-sample-16k.wav"

urlLink = "https://aliyun-nls.oss-cn-hangzhou.aliyuncs.com/asr/fileASR/examples/nls-sample-16k.wav"


def 合成语音():
    # #短文字合成语音，限定300字符
    SYC = synthesizeClass(longtext)
    res = SYC.run()
    print(res)
    SYC.setparams(
        'text',
        '根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。'
    )
    SYC.setparams('callback', pygame_play)  # 设置回调
    res = SYC.run()
    print(3333, SYC.result.filename)
    #  处理结果
    # pygame_play(SYC.result.response.content)


def 合成语音2():
    # #短文字合成语音，限定300字符
    res = ReqSynthesizer(longtext, savefile=False, callback=pygame_play)
    print(res)


def 合成长语音():
    # #长文字合成语音
    long_text_list = string_split_limited_list(longtext)
    # Synt_Thread_read(long_text_list)
    ReqLongSynthesizer(longtext, callback=pygame_play)


def 网络音频识别():
    # #网络音频文件识别
    res = APITransUrl(urlLink)
    print('网络音频文件识别', res, res.response)


def 本地音频识别():
    # # 本地音频文件识别
    res = PostTransFile(audiofilepath)  # 一句话识别，1分钟以内
    print('本地音频文件识别', res, res.response)
    res = TranscriberProcess(audiofilepath)
    print('本地音频文件识别', res, res.response)


def 使用SSML别():
    # #短文字合成语音，使用SSML
    ssml_text_list = [
        '<speak' + item for item in ssml_text.split('<speak') if item.strip()
    ]
    ReqSynthesizer_Thread_read(ssml_text_list)


# 合成语音()
# 合成语音2()
合成长语音()
# 网络音频识别()
# 本地音频识别()
# 使用SSML别()
