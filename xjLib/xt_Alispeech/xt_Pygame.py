# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 20:11:54
#LastEditTime : 2020-06-09 11:44:39
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import io
import time
from io import BytesIO
from threading import Lock, Thread

import pygame
from PyQt5.QtCore import QThread, pyqtSignal

from xt_Alispeech import ReqSynthesizer


def play_callback(data, format='wav'):
    # !使用16000和默认,声音不行
    pygame.mixer.init(frequency=8000)

    if format == 'mp3':
        print('pygame.mixer.music.loading.....')
        pygame.mixer.music.load(io.BytesIO(data))
        pygame.mixer.music.play(1, 0.07)
        print()
        while pygame.mixer.music.get_busy():
            print('pygame.mixer.music.playing.....')
            time.sleep(0.500)

    if format == 'wav':
        pygame.mixer.Sound(data).play()
        print('pygame.mixer.Sound.loading.....')
        while pygame.mixer.get_busy():
            print('pygame.mixer.playing.....')
            time.sleep(0.500)

    pygame.mixer.stop()
    print('pygame.mixer.stop!!！')
    return


class ReqSynthesizer_QThread_read(QThread):
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()
    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, textlist=[], format='wav'):
        super().__init__()
        self._target = ReqSynthesizer
        self.textlist = textlist
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # !使用16000和默认,声音不行
        self.format = format
        if self.format == 'wav':
            self.pym = pygame.mixer
        else:
            self.pym = pygame.mixer.music
        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):
        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, savefile=False).response.content
                self.datas_list.append(data)
                if not self._running:
                    break

            print('MainMonitor stoping!!!!!!')

        ##daemon=True,跟随主线程关闭 ,不能用双QThread嵌套
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):
        while self._running:
            if self.pym.get_busy():
                # 正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        self.stop()
                        print('all recod play finished!!!!!!')
                        self._signal.emit()

        # 停止标记
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False


class ReqSynthesizer_Thread_read(Thread):
    '''传入字符list,连续朗读'''

    _signal = pyqtSignal()
    __instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, textlist=[], format='wav'):
        super().__init__()
        self._target = ReqSynthesizer
        self.textlist = textlist
        self.datas_list = []
        self._running = True
        pygame.mixer.init(frequency=8000)  # !使用16000和默认,声音不行
        self.format = format
        if self.format == 'wav':
            self.pym = pygame.mixer
        else:
            self.pym = pygame.mixer.music
        self.main_monitor()  # 启动语音生成
        self.start()

    def main_monitor(self):
        def _func():
            while len(self.textlist) > 0:
                text = self.textlist.pop(0)
                data = self._target(text, format=self.format, savefile=False).response.content
                self.datas_list.append(data)
                if not self._running:
                    break

            print('MainMonitor stoping!!!!!!')

        ##daemon=True,跟随主线程关闭 ,下面为Thread
        self._MainMonitor = Thread(target=_func, daemon=True, name="MainMonitor")
        self._MainMonitor.start()

    def run(self):

        while self._running:
            if self.pym.get_busy():
                # 正在播放，等待
                QThread.msleep(500)
                print('self.py_mixer.playing......')
                continue
            else:
                if len(self.datas_list) > 0:
                    # 朗读完毕，有未加载数据
                    _data = self.datas_list.pop(0)
                    if self.format == 'wav':
                        pygame.mixer.Sound(_data).play()
                    else:
                        pygame.mixer.music.load(BytesIO(_data))
                        pygame.mixer.music.play(1, 0.07)
                    print('self.py_mixer new loading......')
                    continue

                if not self._MainMonitor.is_alive():
                    # #合成语音线程结束，朗读完毕，且无未加载数据
                    if len(self.textlist) == 0 and len(self.datas_list) == 0:
                        self.stop()
                        print('all recod play finished!!!!!!')
                        self._signal.emit()

        # 停止
        self.pym.stop()
        print('self.py_mixer.stoping!!!!!!')

    def stop(self):
        self._running = False


if __name__ == "__main__":
    from xt_Alispeech import synthesizeClass, ReqLongSynthesizer, APITransUrl, PostTransFile, TranscriberProcess
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
            <say-as interpret-as="date">1121-10-10</say-as>
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

    from xt_String import string_split_limited_list

    def 合成语音():
        # #短文字合成语音，限定300字符
        SYC = synthesizeClass(longtext)
        res = SYC.run()
        print(res)
        SYC.setparams('text', '根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。')
        from xt_Pygame import play_callback
        SYC.setparams('callback', play_callback)  # 设置回调
        res = SYC.run()
        print(3333, SYC.result.filename)
        #  处理结果
        # play_callback(SYC.result.response.content)

    def 合成语音2():
        # #短文字合成语音，限定300字符
        res = ReqSynthesizer(longtext, savefile=False, callback=play_callback)
        print(res)

    def 合成长语音():
        # #长文字合成语音
        long_text_list = string_split_limited_list(longtext)
        # ReqSynthesizer_Thread_read(long_text_list)
        reses = ReqLongSynthesizer(longtext)
        print(reses)

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
        ssml_text_list = ['<speak' + item for item in ssml_text.split('<speak') if item.strip()]
        ReqSynthesizer_Thread_read(ssml_text_list)

    # 合成语音()
    合成语音2()
    # 合成长语音()
    # 网络音频识别()
    # 本地音频识别()
    # 使用SSML别()
