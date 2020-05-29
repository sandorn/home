# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-25 11:34:01
#LastEditTime : 2020-05-29 15:14:43
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================

智能语音交互
https://nls-portal.console.aliyun.com/overview

Python SDK_语音合成_智能语音交互-阿里云
https://help.aliyun.com/document_detail/120699.html?spm=a2c4g.11174283.3.5.66d27275YUUT3w

python如何实现语音合成 - 知乎
https://zhuanlan.zhihu.com/p/88800344

RAM访问控制
https://ram.console.aliyun.com/users/sandorn_ram
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
import json
import time
import uuid

from aliyunsdkcore.acs_exception.exceptions import (ClientException,
                                                    ServerException)
from aliyunsdkcore.client import AcsClient  # 阿里云核心代码库
from aliyunsdkcore.request import CommonRequest  # 阿里云官方核心代码库

import ali_speech
from ali_speech.callbacks import (SpeechSynthesizerCallback,
                                  SpeechTranscriberCallback)
from ali_speech.constant import (ASRFormat, ASRSampleRate)
from xjLib.xt_Thread import CustomThread
from xjLib.req import SessRequests, parse_get, parse_post

accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
Appkey = 'Ofm34215thIUdSIX'


def get_token(access_key_id=None, access_key_secret=None):
    if access_key_id is None:
        access_key_id = accessKeyId
    if access_key_secret is None:
        access_key_secret = accessKeySecret

    # 创建AcsClient实例
    client = AcsClient(access_key_id, access_key_secret, "cn-shanghai")

    # 创建request，并设置参数
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')
    response = client.do_action_with_exception(request)
    res = json.loads(response)
    return (res['Token']['Id'], res['Token']['ExpireTime'])


def get_ali_token(access_key_id=None, access_key_secret=None):
    if access_key_id is None:
        access_key_id = accessKeyId
    if access_key_secret is None:
        access_key_secret = accessKeySecret

    print(access_key_id, access_key_secret)
    token, expire_time = ali_speech.NlsClient.create_token(
        access_key_id, access_key_secret)

    return (token, expire_time)


def postLong(appKey,
             token,
             text,
             audioSaveFile=uuid.uuid4().hex,  #.hex 将生成的uuid字符串中的'－'删除
             format='pcm',
             sampleRate=16000,
             voice='Siyue',
             volume=100,
             speech_rate=0,
             pitch_rate=0):

    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async'
    # 设置HTTPS Headers
    httpHeaders = {'Content-Type': 'application/json'}
    # 设置HTTPS Body
    params = {
        "header": {
            "appkey": appKey,
            "token": token
        },
        "context": {
            "device_id": "my_device_id"
        },
        "payload": {
            "enable_notify": False,
            "tts_request": {
                "format": format,
                "sample_rate": sampleRate,
                "voice": voice,
                "volume": volume,
                "speech_rate": speech_rate,
                "pitch_rate": pitch_rate,
                "text": text,
            },
        },
    }

    session = SessRequests()
    session.setheader(httpHeaders)
    res = session.post(url, json=params)  # "https://httpbin.org/post"
    # json=params,  # data=json.dumps(params)
    print(8888, res.text)
    #!失败  400000005
    return

    contentType = res.headers['Content-Type']

    if res.status == 200 and 'audio/mpeg' == contentType:
        with open(
                f'{audioSaveFile}_{voice}_{round(sampleRate/1000)}K.{format}',
                mode='wb') as f:
            f.write(res.content)
        print(
            f'{audioSaveFile}_{voice}_{round(sampleRate/1000)}K.{format}, POST request succeed!'
        )
    else:
        print('The POST request failed: ' + str(params))


def postRESTful(appKey,
                token,
                text,
                audioSaveFile=None,  #.hex 将生成的uuid字符串中的'－'删除
                format='wav',
                sampleRate=16000,
                voice='Aixia',
                volume=100,
                speech_rate=0,
                pitch_rate=0):
    '''短文本语音合成'''
    '''
    RESTful API_语音合成_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/94737.html?spm=a2c4g.11186623.2.17.2579259en8Zice
    #!超过300字符串自动截断
    '''
    # host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
    # 设置HTTPS Headers
    httpHeaders = {'Content-Type': 'application/json'}
    # 设置HTTPS Body
    body_dict = {
        'appkey': appKey,
        'token': token,
        'text': text,
        'format': format,
        'sample_rate': sampleRate,
        'voice': voice,
        'volume': volume,
        'speech_rate': speech_rate,
        'pitch_rate': pitch_rate,
        # voice 发音人，可选，默认是xiaoyun
        # volume 音量，范围是0~100，可选，默认50
        # speech_rate 语速，范围是-500~500，可选，默认是0
        # pitch_rate 语调，范围是-500~500，可选，默认是0
    }

    session = SessRequests()
    session.setheader(httpHeaders)
    res = session.post(url, json=body_dict)  # "https://httpbin.org/post"

    contentType = res.headers['Content-Type']
    if res.status == 200 and 'audio/mpeg' == contentType:
        if audioSaveFile is None:
            return res.content

        filename = f'{audioSaveFile}_{uuid.uuid4().hex}_{voice}_{round(sampleRate/1000)}K.{format}'
        with open(filename, mode='wb') as f:
            f.write(res.content)
        print(filename, ' GET request succeed!')
        return filename
    else:
        print('The GET request failed: ' + res.text + '\n By ' + str(body_dict))


def getRESTful(appKey,
               token,
               text,
               audioSaveFile=None,
               format='wav',
               sampleRate=16000,
               voice='Aixia',
               volume=100,
               speech_rate=0,
               pitch_rate=0):
    '''短文本语音合成'''
    # host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
    # 设置HTTPS Headers
    httpHeaders = {'Content-Type': 'application/json'}
    # 设置HTTPS Body
    body_dict = {
        'appkey': appKey,
        'token': token,
        'text': text,
        'format': format,
        'sample_rate': sampleRate,
        'voice': voice,
        'volume': volume,
        'speech_rate': speech_rate,
        'pitch_rate': pitch_rate,
        # voice 发音人，可选，默认是xiaoyun
        # volume 音量，范围是0~100，可选，默认50
        # speech_rate 语速，范围是-500~500，可选，默认是0
        # pitch_rate 语调，范围是-500~500，可选，默认是0
    }

    session = SessRequests()
    session.setheader(httpHeaders)
    res = session.get(url, params=body_dict)  # "https://httpbin.org/post"
    # print(res, res.headers)

    contentType = res.headers['Content-Type']

    if res.status == 200 and 'audio/mpeg' == contentType:
        if audioSaveFile is None:
            return res.content

        filename = f'{audioSaveFile}_{uuid.uuid4().hex}_{voice}_{round(sampleRate/1000)}K.{format}'
        with open(filename, mode='wb') as f:
            f.write(res.content)
        print(filename, ' GET request succeed!')
        return filename
    else:
        print('The GET request failed: ' + res.text + '\n By ' + str(body_dict))


class SynthesizerMyCallback(SpeechSynthesizerCallback):
    # #文字转音频，使用回调方式
    # #参数name用于指定保存音频的文件
    def __init__(self, name):
        self._name = name
        self._fout = open(name, 'wb')

    def on_binary_data_received(self, raw):
        print('MyCallback.on_binary_data_received: %s' % len(raw))
        self._fout.write(raw)

    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: %s' % message)
        self._fout.close()

    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' %
              (message['header']['task_id'], message['header']['status_text']))
        self._fout.close()

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def Synthesizerprocess(appkey,
                       token,
                       text,
                       audioSaveFile=uuid.uuid4().hex,
                       format='wav',
                       sampleRate=16000,
                       voice='Aixia',
                       volume=100,
                       speech_rate=0,
                       pitch_rate=0):
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    filename = f'{audioSaveFile}_{voice}_{round(sampleRate/1000)}K.{format}'
    callback = SynthesizerMyCallback(filename)
    synthesizer = client.create_synthesizer(callback)
    synthesizer.set_appkey(appkey)
    synthesizer.set_token(token)
    synthesizer.set_voice(voice)
    synthesizer.set_text(text)
    synthesizer.set_format(format)
    synthesizer.set_sample_rate(sampleRate)
    synthesizer.set_volume(volume)
    synthesizer.set_speech_rate(speech_rate)
    synthesizer.set_pitch_rate(pitch_rate)

    try:
        ret = synthesizer.start()
        if ret < 0:
            return ret

        synthesizer.wait_completed()
    except Exception as e:
        print(e)
    finally:
        synthesizer.close()
        return callback._name


import pygame


class LongCallback(SpeechSynthesizerCallback):
    # #文字转音频，使用回调方式
    # #参数name用于指定保存音频的文件
    def __init__(self, name):
        self._name = name
        self._fout = open(name, 'wb')
        self.py_mixer = pygame.mixer
        self.py_mixer.init(frequency=8000)  #!使用16000和默认,声音不行
        self.datas = []

    def on_binary_data_received(self, raw):
        print('MyCallback.on_binary_data_received: %s' % len(raw))
        self.datas.append(raw)
        self._fout.write(raw)

    def read(self):
        raw = self.datas.pop(0)
        self.py_mixer.Sound(raw).play()
        while self.py_mixer.get_busy():
            print('self.py_mixer.playing......')
            time.sleep(0.200)

    def on_completed(self, message):
        print('MyCallback.OnRecognitionCompleted: %s' % message)
        self._fout.close()
        # return self._name

    def on_task_failed(self, message):
        print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' %
              (message['header']['task_id'], message['header']['status_text']))
        self._fout.close()

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def Longprocess(appkey,
                token,
                text,
                audioSaveFile=uuid.uuid4().hex,
                format='wav',
                sampleRate=16000,
                voice='Aixia',
                volume=100,
                speech_rate=0,
                pitch_rate=0):
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    filename = f'{audioSaveFile}_{voice}_{round(sampleRate/1000)}K.{format}'
    callback = LongCallback(filename)
    synthesizer = client.create_synthesizer(callback)
    synthesizer.set_appkey(appkey)
    synthesizer.set_token(token)
    synthesizer.set_voice(voice)
    synthesizer.set_format(format)
    synthesizer.set_sample_rate(sampleRate)
    synthesizer.set_volume(volume)
    synthesizer.set_speech_rate(speech_rate)
    synthesizer.set_pitch_rate(pitch_rate)

    for index, data in enumerate(text):
        if not data.strip():
            continue
        synthesizer.set_text(text)
        ret = synthesizer.start()
        if ret < 0:
            continue
        synthesizer.wait_completed()

    synthesizer.close()
    return callback._name


class TranscriberCallback(SpeechTranscriberCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """

    def __init__(self, name='default'):
        self._name = name

    def on_started(self, message):
        print('TranscriberCallback.OnRecognitionStarted: %s' % message)

    def on_result_changed(self, message):
        print(
            'TranscriberCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s'
            % (self._name, message['header']['task_id'],
               message['payload']['result']))

    def on_sentence_begin(self, message):
        print(
            'TranscriberCallback.on_sentence_begin: file: %s, task_id: %s, sentence_id: %s, time: %s'
            % (self._name, message['header']['task_id'],
               message['payload']['index'], message['payload']['time']))

    def on_sentence_end(self, message):
        print(
            'TranscriberCallback.on_sentence_end: file: %s, task_id: %s, sentence_id: %s, time: %s, result: %s'
            % (self._name, message['header']['task_id'],
               message['payload']['index'], message['payload']['time'],
               message['payload']['result']))

        self.result = message['payload']['result']

    def on_completed(self, message):
        print('TranscriberCallback.OnRecognitionCompleted: %s' % message)

    def on_task_failed(self, message):
        print(
            'TranscriberCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s'
            % (message['header']['task_id'], message['header']['status_text']))

    def on_channel_closed(self):
        print('TranscriberCallback.OnRecognitionChannelClosed')


def TranscriberProcess(_, appkey, token, filepath):
    '''本地音频文件识别
    Python SDK_实时语音识别_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/120698.html?spm=a2c4g.11186623.6.577.2579259eScpzA7
    支持音频编码格式：pcm(无压缩的pcm文件或wav文件)，16bit采样位数的单声道(mono)
    '''
    client = ali_speech.NlsClient()
    # 设置输出日志信息的级别：DEBUG、INFO、WARNING、ERROR
    client.set_log_level('INFO')
    callback = TranscriberCallback(filepath)
    transcriber = client.create_transcriber(callback)
    transcriber.set_appkey(appkey)
    transcriber.set_token(token)
    transcriber.set_format(ASRFormat.PCM)
    transcriber.set_sample_rate(ASRSampleRate.SAMPLE_RATE_16K)
    transcriber.set_enable_intermediate_result(False)
    transcriber.set_enable_punctuation_prediction(True)
    transcriber.set_enable_inverse_text_normalization(True)

    try:
        ret = transcriber.start()
        if ret < 0:
            return ret

        print('sending audio...')
        with open(filepath, 'rb') as f:
            audio = f.read(3200)
            while True:
                audio = f.read(3200)
                if not audio:
                    break

                ret = transcriber.send(audio)

                if ret < 0:
                    break
                time.sleep(0.1)

        transcriber.stop()
    except Exception as e:
        print(e)
    finally:
        transcriber.close()
        return {
            callback._name: callback.result,
            'name': callback._name,
            'result': callback.result
        }


def Transcriber_process_multithread(appkey, token, filepath_list):
    _ = [
        CustomThread(TranscriberProcess, [appkey, token, filepath_list[i]])
        for i in range(len(filepath_list))
    ]
    result_list = CustomThread.wait_completed()
    return result_list


def urllinkTrans(akId,
                 akSecret,
                 appKey,
                 urlLink,
                 enable_words=False,
                 auto_split=False):
    '''
    网络音频文件识别
    识别的文件需要提交基于HTTP可访问的URL地址，不支持提交本地文件
    接口说明_录音文件识别_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/90727.html?spm=a2c4g.11186623.6.581.2579259eScpzA7
    '''
    # 网址音频文件转文字
    PRODUCT = "nls-filetrans"
    DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
    API_VERSION = "2018-08-17"

    # 创建AcsClient实例
    client = AcsClient(akId, akSecret, "cn-shanghai")
    # 提交录音文件识别请求
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name("SubmitTask")
    postRequest.set_method('POST')

    task = {
        'appkey': appKey,
        'file_link': urlLink,
        'version': "4.0",
        'enable_words': enable_words,
        'auto_split': auto_split  # 开启智能分轨
    }
    postRequest.add_body_params("Task", json.dumps(task))

    taskId = ""

    try:
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        print(1111, postResponse)
        statusText = postResponse['StatusText']
        if statusText == 'SUCCESS':
            print("网络音频文件识别请求成功响应！")
            taskId = postResponse['TaskId']
        else:
            print("网络音频文件识别请求失败！")
            return
    except (ServerException, ClientException) as e:
        print(e)

    # 创建CommonRequest，设置任务ID
    getRequest = CommonRequest()
    getRequest.set_domain(DOMAIN)
    getRequest.set_version(API_VERSION)
    getRequest.set_product(PRODUCT)
    getRequest.set_action_name('GetTaskResult')
    getRequest.set_method('GET')
    getRequest.add_query_param('TaskId', taskId)

    # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，或者为错误描述，则结束轮询。
    statusText = ""
    Result_text = ""
    Result = ""
    while True:
        try:
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            statusText = getResponse['StatusText']
            if statusText == 'RUNNING' or statusText == 'QUEUEING':
                # 继续轮询
                time.sleep(10)
            else:
                Result = getResponse
                Result_text = getResponse['Result']['Sentences'][0]['Text']
                # print(2222, Result)
                # 退出轮询
                break

        except ServerException as e:
            print(e)
        except ClientException as e:
            print(e)
    if statusText == 'SUCCESS':
        print("录音文件识别成功！")
    else:
        print("录音文件识别失败！")
    return Result_text, Result


def postTrans(appKey,
              token,
              audio_File,
              format='wav',
              sampleRate=16000,
              enablePunctuationPrediction=False,
              enableInverseTextNormalization=True,
              enableVoiceDetection=True):
    '''
    一句话识别RESTful API支持以POST方式整段上传不超过一分钟的语音文件
    RESTful API_一句话识别_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/92131.html?spm=5176.10695662.1996646101.searchclickresult.249745f65JYpsf
    '''
    url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
    # 设置RESTful请求参数
    request = url + '?appkey=' + appKey
    request = request + '&format=' + format
    request = request + '&sample_rate=' + str(sampleRate)
    if enablePunctuationPrediction:
        request = request + '&enable_punctuation_prediction=' + 'true'
    if enableInverseTextNormalization:
        request = request + '&enable_inverse_text_normalization=' + 'true'
    if enableVoiceDetection:
        request = request + '&enable_voice_detection=' + 'true'
    print('Request: ' + request)

    with open(audio_File, mode='rb') as f:
        audioContent = f.read()

    # 设置HTTPS Headers
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': str(len(audioContent)),
    }

    session = SessRequests()
    session.setheader(httpHeaders)
    body_json = session.post(
        request, data=audioContent).json  # "https://httpbin.org/post"

    status = body_json['status']
    if status == 20000000:
        result = body_json['result']
    # print(1111, result, type(body_json))
    return result, body_json


if __name__ == "__main__":
    token = get_token()[0]
    longtext = '''
        郑阳市，下午四点，原本正该艳阳高照，天空却笼罩了厚厚的乌云，黑得有若夜晚降临。        伴随着乌云的，是一阵又一阵的狂风，以及远处的电闪雷鸣，仿佛世界末日一般。
        冯君坐在员工宿舍里，茫然地看着窗外，将手里的啤酒瓶往桌上一顿，重重地叹口气，“这尼玛……是哪位道友在渡劫？”
        冯君不是修炼者，他只是网络小说爱好者，而他此刻的吐槽，只是因为他的心情极其不爽。
        他要辞职了。
        冯君今年二十四岁，毕业于江夏大学，拿的是中文和工商管理双学位。
        虽然大学扩招之后，城市里的本科生已经多过狗了，但是能在四年里，在985院校拿到双学位，很显然，他勉强可以归到天之骄子那一类人里。
        然而，大学毕业就是失业，他先是去女朋友所在的南方城市打拼了两年，然后带着丰富的经历，独自来到郑阳市。
        目前他就职的单位——不能说是单位，而是该说公司，是鸿捷文化娱乐有限公司。
        鬼才知道，为什么健身会所要冠以“文化”之名，也许是传说中的文体不分家？
        没错，冯君现在是就职于鸿捷健身会所。
        不是传说中艳、遇无数的健身教练，而是负责接待、跑腿和打扫卫生的小弟。
        健身教练是要证件的，鸿捷健身会所不是路边的野店，会所在郑阳的名气极大。
        冯君之所以能应聘成功，一来是目前市场上青壮劳力比较短缺，二来是他的形象不错，相貌硬朗，身材也比较壮硕，小鲜肉什么的谈不上，但是勉强搭得上“精壮”的边儿。
        然而，应聘成功之后，他才知道，想要做健身教练，得有本儿！
        这真是一个悲伤的消息。
        所以堂堂的双学位获得者，竟然成了健身会所的小弟。
        当然，小弟也难免有春天，在他就职的三个月时间里，也有几个中老年妇女对他表示出了兴趣，希望接受他的“单独训练”，不过冯君摇头了——她们的目的不那么单纯。
        关键是，她们长得太下不为例了，个别人还有令人难以接受的体味和咄咄逼人的气势。
        有健身教练因为他的迂腐而耻笑他——研究生真是穷得有志气。
        尼玛，双学位和研究生不是一回事好不好？
        不管怎么说，冯君在鸿捷健身会所，算是一个小小的另类，学历高职位低不说，还有点年轻人不服输的傲气，在服务行业里，这种气质是不被鼓励的。
        客人不会喜欢这种傲气，同僚们也会心里鄙视。
        冯君今天的业务单子，就是被自己的同僚撬走了。
        上午的时候，四个青春靓丽的女孩儿走进了会所，她们不是会员，就是用临时兴起前来健身，其中一个高挑的女孩儿，长得相当令人惊艳。
        负责接待她们的是冯君，在她们健身的过程中，如果能说服她们办卡，他可以赚到提成。
        凭良心说，冯君对此不报太大的信心，原因很简单，这几个女孩一看就是大学生，附近可是没有什么大专院校。
        而且学生嘛，正是青春年少，有长期健身需求的不多，腰包的厚度也不够，愿意在这上面花钱的极少。
        但是就这么一个小小的接待业务，还被别人撬走了，负责健美的教练刘树明走上前，表示自己可以提供相关的咨询和服务。
        刘教练走上前的时候，对着冯君做了一个赶苍蝇的动作，“去去去……我来！”
        冯君对此是相当的不忿，不但是因为提成，也是因为对方的态度——你丫跟我说话的时候，看我一眼很难吗？
        但是他也不能说什么，在健身会所，健身教练的优先级，当然高于小弟。
        然后……就出事了，刘教练被人打了。
        打他的就是那四个女生。
        刘树明身为健身教练，拥有健美的身材和夸张的肌肉，战斗力不会太差，但是那四个女生里，有两个很能打，所以，双拳难敌四手。
        大堂经理被惊动了，过来一问才知道，四个女生一开始就表示，我们是随便练一练，不需要教练，但是刘树明死乞白咧地要讲解，还毛手毛脚地摸来摸去，女生们终于火了。
        可是刘教练表示：我就是想提供一些辅导，通过热情的服务，争取让她们办理会员。
        大堂经理郭跃玲知道刘树明的小算盘——这家伙的食谱很杂。
        刘教练为了赚钱，能为老丑的富婆提供各种服务，合法的和不怎么合法的，也愿意勾搭年轻漂亮的小妹妹，打个友谊赛什么的。
        郭大堂先对客户表示了歉意，免了她们的单，好言好语将人送走之后，开始追究责任。
        然而奇怪的是，她把板子瞄准了一个匪夷所思的方向。
        “冯君，既然是你负责接待的，你为什么没有跟进？客户已经说了，人家不需要教练！”
        刘教练也咬牙切齿地看着冯君，眼中满是怒火，“你如果能负责接下来的服务，我何至于此？”
        冯君的傲气并不是限于传说，闻言他将手里的抹布往地上一摔，冷冷地看郭大堂一眼，“我也没求着刘教练上来接手，丫撵我的时候，都不看我一眼……抢我业务还有道理了？”
        “你这是什么态度？”郭大堂的声音变得尖厉了起来，“就这么跟领导说话？”
        冯君转身向外走去，“我身体不舒服，要回去休息！”
        这个时候，他已经打定了主意，这鸟毛地方，劳资不待了。
        然后，他就买了一提啤酒，来到宿舍里慢慢地喝，心里一直在琢磨：辞职了该去哪儿？
        郑阳虽然是准副省级城市，但是这里的工作并不好找，服务员、小弟、搬运工之类的，倒是容易一些，可是合适他双学位学历的工作，真的是很难找。
        当初他在郑阳转悠了大半个月，也没找到合适的工作，要不也不会选择来健身会所了。
        当然，回老家也是一个选择，他的老家是个小县城，父母做了些小买卖，在地方上有一点小小的人脉，为他找个工作不算很难，实在不行，接了自家的摊子干也可以。
        然而，身为985的双学位，冯君怎么肯回去？他舍不得大城市的繁华，更丢不起那人。
        一边看着有若地球末日的窗外，他一边思索，是现在辞职呢，还是等发了工资再辞职？
        这两年多下来，他没有攒到什么钱，就算加上父母给他打来的求职的钱，卡上也不过才一万多块，甚至他的手机，都是充话费送的，虽然号称智能机，但基本上是老年机。
        不知道什么时候，窗外豆大的雨点落了下来，打在窗玻璃上，“砰砰”地作响。
        闪电也一道比一道亮，轰隆隆的雷声不绝于耳。
        冯君喝完了宿舍里剩下的半瓶白酒，又喝了七八瓶啤酒，酒意上头，就想打个电话给朋友，拿起老年机，却发现手机只剩下了百分之三的电量。
        他将手机充上电，自己却一头栽在床上，呼呼大睡了起来。
        临睡之前，他还不忘将手机攥在手里，没办法，这种低级的员工宿舍里，丢东西是常态——他丢过不止一次钱了，流动人口多的地方，短期行为就必然多。
        底层劳动人民的日常，实在是艰难，说多了都是泪……
        不知道睡了多久，窗外猛地一道闪电亮起，闪耀得人睁不开眼，与此同时，一道电弧顺着充电器的电线，蹿向那只老旧的智能机。
        冯君是被炸雷惊醒的，这雷就有若在耳边一般，声音也极大，有若天崩地裂一般，哪怕是睡得半死，他也蹭地坐了起来，毛发直立。
        他惊魂未定地四下看一看，才发现窗玻璃的中央，都震得裂开一道缝，“不会吧，这雷的距离……三百米都不到？”
        然后，他才觉得手上一阵剧痛，低头一看，老年机倒是被他攥在手里，但是这充电线……怎么就变得黑了呢？
        抽动一下鼻子，他闻到空中有烧橡胶的味道……
        他还没有来得及做出任何的反应，旁边的屋子里就响起了叫声。
        “握草，电视都冒烟了，这尼玛雷也太大了一点吧？”
        “我入他先人，这楼没有避雷针吗？”
        冯君所在的宿舍，位于一栋四层的筒子楼里，虽然老旧，也有避雷针。
        但是雷太大了，太近了，避雷针不是万能的，这一记惊雷，劈坏了筒子楼周边最少五十台电视，近百部有线电话、路由器和WIFI。
        冯君对外界的损失，没多大兴趣，他关心的是：手机劈坏了没有？
        破手机虽然老旧且缓慢，打电话还是很方便的，蹭上隔壁的WIFI，上网也不是问题，当然，最关键的是，里面存着他的通讯录。
        他按了一下手机下沿中央的home键，发现手机不但亮了，反应也正常——缓慢而坚定。
        或许我该打个电话，试一试通话效果？冯君一边想，一边扫一眼手机界面。
        然后他就愣住了：现在是晚上八点？
        好吧，八点不算奇怪，毕竟他睡的时候也近六点了。
        但是为什么……手机的电量，已经是百分之百了？

        冯君的手机，真的是充话费送的，不但配置奇低运行缓慢，而且……充电时间也很长。
        由于缺乏快充技术，手机要四个小时才能勉强充满电，然后能使用一天半到两天。
        若是一直抱着手机在划，一天都撑不下来。
        冯君好奇的是，这手机怎么能在两个小时左右，将电量充满？
        他是如此地好奇，甚至忘了自己即将离职的烦恼。
        冯君是个喜欢看网络小说的家伙，这个选择其实有点不得已，泡吧之类的消遣，他也喜欢，但是那些爱好太费钱了，看书比较便宜，就算看正版，一天都花不了一盒烟钱。
        ——莫非我遇到了传说的机缘？
        冯君实在没办法控制自己不这么想，毕竟他似乎……是被雷劈了，居然安然无恙？
        他尝试着打了一个电话给同事王海峰，事实证明，通话效果很不错，他甚至听得出来，对方的情绪不是很好。
        王海峰是他在鸿捷会所比较亲近的人，丫虽然也是二十多岁，但却拥有教练资格证，在健体方面有很强的专业能力，两人年纪相近，地位相差极大，却有很好的私交。
        冯君为今天的事抱怨了一番，并且表示，自己不想在这里干下去了。
        王教练则是心不在焉回一句，“哦，刘树明欺负你？回头我收拾他。”
        刘树明只是普通的塑形教练，而且已经三十多了，虽然肌肉比较夸张，但是真要动手的话，根本不是王海峰的对手。
        冯君放下电话，轻声嘀咕一句，“这家伙心里有事。”
        好吧，别人的事，跟他没多大关系，他现在要考虑的是，明天是不是还去上班？
        鸿捷会所虽然是服务行业，但还是比较正规的，针对流动性大的服务员，公司里有日工资的说法，冯君明天辞职的话，这二十多天的工钱，也是要结的。
        不过……财务上任大姐毛病太多，难免要被念叨很久。
        更重要的是，如果他辞职的话，明天晚上就要自己找住处了，那是要花钱的。
        “唉，鸿捷里就没几个好人，”冯君一边念叨着，一边扫视着手机——电量充得很快，不要掉得也很快吧？
        看着看着，他就看到了手机QQ，猛地想起:QQ农场的菜还没收呢。
        QQ农场，不是冯君自己要装的，他装这个玩意儿，是为了巴结领导，严格来说，是为了巴结鸿捷公司的老总——红姐喜欢偷菜。
        身在职场，不需要像在官场一般的谨慎，但是领导有爱好，下面的小职员也最好配合一下，这是王海峰提醒他的。
        果不其然，他装了QQ农场两天后，红姐来视察，发现了他“不小心”露出的农场界面，就将他的QQ号要了去，双学位这也算是有了直达天听的路径。
        不过离领导近了，也不完全是好事，红姐在加了他一个多月后，有一天就无意中说起，“你这级别上去了，也不能不种牧草啊。”
        冯君顿时幡然醒悟：领导那里还开了牧场！
        冯君其实也开了牧场，但是他自家种的草，一般就够用了，快没草的时候，才会想着种两茬，哪里想得到，领导的牧场也需要牧草？
        红姐从来不种牧草，她级别高，种的都是高附加值的作物。
        不种牧草怎么办？只能靠偷了，反正鸿捷会所这么多员工，她有的是盗窃目标。
        冯君勉强算是个天之骄子，得了领导的提示，种牧草就是常事了，而且他还提醒自己，不能种了就收，得等领导偷完，自己再收——虽然他很不喜欢被偷的感觉。
        然而，红姐也不是卡着点收，身为鸿捷的老总，她一天多少事儿呢，农场主经常等半天，都盼不来小偷，到后来，他就只能等牧草被偷得不能再偷的时候，再出手收获。
        这也算对得起领导了吧？
        现在，冯君就打算对不起领导了，“反正都要辞职了，我记得这次种的全是牧草来的……”
        然后他就点开了QQ农场，看着地里已经成熟的牧草，操纵着屏幕上的大手，轻轻一点。
        握草……真的是握草了！
        下一刻，他眼前一黑，就置身于一个奇怪的空间里，周边都是QQ农场的样子，面前是10块田地，都种满了牧草，还有田地在旁边抛荒。
        甚至不远处，还有一个狗舍，狗舍前有一个碗，空的——狗粮要花钱买的。
        再说了，买了狗粮，领导还能愉快地偷菜吗？
        冯君愣了足足有十分钟，狠狠抽了自己一记耳光，发现很痛之后，才一蹦老高，“握草……这尼玛，这尼玛，这尼玛……”
        他已经激动得语无伦次了，奇遇，绝对是传说中的奇遇啊。
        事实证明，确实是奇遇，他居然有幸亲自去收割牧草，不需要镰刀什么的，他的手一伸，一拽就是一把，真正的“握草”。
        但是……握草是很累的，严格来说，手工收取田地里的牧草，真的很辛苦。
        冯君用了差不多半个小时，才拽完了一块牧草，这一块地，足有半分大小——你说你把地搞这么大做啥呢？吃饱了撑的？
        然后，他站起身子来，“这……怎么出去啊？系统，系统你在吗？”
        哥们儿希望，系统的形象，能是一个白衣飘飘的仙子，实在不行，机器人也行，就是不要萝莉，萝莉神马的最讨厌了，我还不知道想对谁卖萌呢。
        非常遗憾，啥都没有，别说最讨厌的萝莉，就连系统提示音都没有。
        冯君看着剩余九块地里成熟的牧草，轻声嘀咕一句，“或许……得都收完，才能出去？”
        六个小时之后，冯君坐在田埂上，气喘吁吁地看着面前的十块空地，恨不得就地躺倒，美美地睡一觉，“这尼玛，真不是人干的活啊，系统……系统你还不出来？”
        依旧是没有任何的反应。
        “好吧，萝莉也行，”冯君打算认输了，“萝莉……萝莉你还不出来？”
        依旧是没有任何的反应。
        冯君有点慌了，这不是进来出不去吧？哥们儿的生活虽然有点小小的不如意，但是……我真的还没做好当农民的心理准备，更别说还是一个在游戏里的农民。
        想到悲惨处，他忍不住要心中忐忑：不会进得来出不去，整个人就化为一股“0”和“1”组成的数据流了吧？
        经过多次尝试，半个小时之后，冯君终于回到了现实中。
        他先是打量一眼四周，又伸手掐了一下自己的大腿——没办法，刚才那个耳光抽得太狠，现在都有点耳鸣，他觉得还是掐一下自己比较合适。
        大腿上传来的痛觉告诉他：没错，真的回到了现实。
        紧接着，他如释重负地长出一口气，“我去，还说实在不得已，得去农场外探险呢。”
        事实证明，农场那个奇怪的空间里，并没有什么系统之类的逆天存在，他刚才之所以出不来，是因为一块地里，残留了一根细小的牧草。
        仅仅是因为没有收取干净牧草，他差点饿死在游戏里，这是多么痛的领悟。
        “看来，这个农场，还是严格地执行了程序设定，”冯君对自己说，脸上有哭笑不得的表情。
        接下来，身为奇遇的受益者，他当然首先要分析一下，这个奇遇是从何而来。
        不过下一刻，冯君的肚子就传来“咕噜噜”一阵鸣叫——他已经有七八个小时没有进食了，尤其是在这段时间内，他还在干体力活。
        然而，当他的眼光扫向手机右上角的时间时，他再次惊呆了，“我去，还是晚上八点？”
        翻看一下日期，冯君可以确定，自己还是活在当天，活在喝了很多酒然后被雷劈的这一天。
        也就是说，自己进入农场之后，虽然在里面待了七个小时，外面的时间，竟然是静止的！
        “好牛掰的玩意儿，”他情不自禁地感叹一句，然后忍不住浮想联翩，拥有这种逆天的宝物或者说机缘，当哥们儿走上人生巅峰时，该使用哪种风骚的步伐？
        搂着白富美的时候，又应该使用什么样的姿势？
        或者，一只白富美不够的话，还可以考虑多来几只……
        好吧，这些都是一闪而过的念头，当务之急是，他现在必须出去吃点东西了。
        当他从床上站起身时，猛然间只觉得双腿发软，眼前一黑，若不是一伸手扶住了墙，肯定会摔倒在地上。
        有点……饿过劲儿了？冯君双目紧闭，深呼吸几口，才缓缓睁开眼睛，“不行，今天一定要好好地大吃一顿，犒劳一下自己。”
        就在他走到房间门口的时候，一个小胖子匆匆地从外面走了进来，见到他精疲力竭的模样，顿时就是一愣，“握草，你这是干什么去了？”
        这是冯君的室友赵红旗，也是鸿捷的小弟，平常主要负责代客泊车，经常能拿到小费，收入比双学位小弟要高一点，花钱手脚也大。
        冯君很不喜欢此人，倒不是他嫉妒对方收入高，而是他两次丢钱，赵红旗都有作案的嫌疑。
        所以，面对对方的提问，他只是有气无力地回答，“我去种了半天地。”
        “握草，”赵红旗不满意了，郑阳这堂堂的省会城市，还是准副省级，市区里哪里会有地给你种？“我就是关心一下你，你不呛人会死吗？”
        冯君看了他好一阵，才微微颔首，很真诚地发话，“不骗你，我真的是握草去了……”
    '''
    Longprocess(Appkey, token, longtext)
    '''
    # #长文字合成语音
    postLong(Appkey, token, longtext)
    # #短文字合成语音，限定300字符
    text = '根据北京银保监局近期工作部署要求，盛唐融信高度重视，迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。'
    postRESTful(Appkey, token, text, speech_rate=-40)
    filename = Synthesizerprocess(Appkey, token, text, speech_rate=-40)
    print(filename)
    # #网络音频文件识别
    urlLink = "https://aliyun-nls.oss-cn-hangzhou.aliyuncs.com/asr/fileASR/examples/nls-sample-16k.wav"
    text, res = urllinkTrans(accessKeyId, accessKeySecret, Appkey, urlLink)
    print('网络音频文件识别', text, res)

    # # 本地音频文件识别
    filepath = "D:/alibabacloud-nls-python-sdk/nls-sample-16k.wav"
    text, res  = postTrans(Appkey, token, filepath)  ##一句话识别，1分钟以内

    res = TranscriberProcess(None, Appkey, token, filepath)
    print('本地音频文件识别', res, res['result'], '|||', res['name'])

    bbb = Transcriber_process_multithread(Appkey, token, [filepath, filepath])
    print('本地音频文件批量识别', bbb)
    '''
'''
{
    {
        "NlsRequestId": "aed8c1af075347819118ff6bf8111168",
        "RequestId": "0989F63E-5069-4AB0-822B-5BD2D95356DF",
        "Token": {
            "ExpireTime": 1527592757,
            "Id": "124fc7526f434b8c8198d6196b0a1c8e",
            "UserId": "123456789012"
        }
    }
    Token->Id 为本次分配的访问令牌Access token
    Token->ExpireTime 为此令牌的有效期时间戳（单位：秒，例如1527592757换算为北京时间为：2018/5/29 19:19:17，即token在该时间之前有效。）


    声音说明：
    字级别音素边界接口：语音实时合成服务在输出音频的同时，可输出每个字在音频中的时间位置，即时间戳。该时间信息可用于驱动虚拟人口型、做视频配音字幕等。
    注意：只有支持字级别音素边界接口的发音人才有此功能。
    名称	voice参数值	类型	适用场景	支持语言	支持采样率(Hz)	支持字级别音素边界接口	备注
    小云	Xiaoyun	标准女声	通用场景	支持中文及中英文混合场景	8K/16K	否
    小刚	Xiaogang	标准男声	通用场景	支持中文及中英文混合场景	8K/16K	否
    若兮	Ruoxi	温柔女声	通用场景	支持中文及中英文混合场景	8K/16K/24K	否
    思琪	Siqi	温柔女声	通用场景	支持中文及中英文混合场景	8K/16K/24K	是
    思佳	Sijia	标准女声	通用场景	支持中文及中英文混合场景	8K/16K/24K	否
    思诚	Sicheng	标准男声	通用场景	支持中文及中英文混合场景	8K/16K/24K	是
    艾琪	Aiqi	温柔女声	通用场景	支持中文及中英文混合场景	8K/16K	是
    艾佳	Aijia	标准女声	通用场景	支持中文及中英文混合场景	8K/16K	是
    艾诚	Aicheng	标准男声	通用场景	支持中文及中英文混合场景	8K/16K	是
    艾达	Aida	标准男声	通用场景	支持中文及中英文混合场景	8K/16K	是
    宁儿	Ninger	标准女声	通用场景	仅支持纯中文场景	8K/16K/24K	否
    瑞琳	Ruilin	标准女声	通用场景	仅支持纯中文场景	8K/16K/24K	否
    思悦	Siyue	温柔女声	客服场景	支持中文及中英文混合场景	8K/16K/24K	否
    艾雅	Aiya	严厉女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    艾夏	Aixia	亲和女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    艾美	Aimei	甜美女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    艾雨	Aiyu	自然女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    艾悦	Aiyue	温柔女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    艾婧	Aijing	严厉女声	客服场景	支持中文及中英文混合场景	8K/16K	是
    小美	Xiaomei	甜美女声	客服场景	支持中文及中英文混合场景	8K/16K/24K	否
    艾娜	Aina	浙普女声	客服场景	仅支持纯中文场景	8K/16K	是
    伊娜	Yina	浙普女声	客服场景	仅支持纯中文场景	8K/16K/24K	否
    思婧	Sijing	严厉女声	客服场景	仅支持纯中文场景	8K/16K/24K	是
    思彤	Sitong	儿童音	童声场景	仅支持纯中文场景	8K/16K/24K	否
    小北	Xiaobei	萝莉女声	童声场景	仅支持纯中文场景	8K/16K/24K	是
    艾彤	Aitong	儿童音	童声场景	仅支持纯中文场景	8K/16K	是
    艾薇	Aiwei	萝莉女声	童声场景	仅支持纯中文场景	8K/16K	是
    艾宝	Aibao	萝莉女声	童声场景	仅支持纯中文场景	8K/16K	是
    Harry	Harry	英音男声	英文场景	仅支持英文场景	8K/16K	否
    Abby	Abby	美音女声	英文场景	仅支持英文场景	8K/16K	否
    Andy	Andy	美音男声	英文场景	仅支持英文场景	8K/16K	否
    Eric	Eric	英音男声	英文场景	仅支持英文场景	8K/16K	否
    Emily	Emily	英音女声	英文场景	仅支持英文场景	8K/16K	否
    Luna	Luna	英音女声	英文场景	仅支持英文场景	8K/16K	否
    Luca	Luca	英音男声	英文场景	仅支持英文场景	8K/16K	否
    Wendy	Wendy	英音女声	英文场景	仅支持英文场景	8K/16K/24K	否
    William	William	英音男声	英文场景	仅支持英文场景	8K/16K/24K	否
    Olivia	Olivia	英音女声	英文场景	仅支持英文场景	8K/16K/24K	否
    姗姗	Shanshan	粤语女声	方言场景	支持标准粤文（简体）及粤英文混合场景	8K/16K/24K	否
    小玥	Xiaoyue	四川话女声	方言场景	支持中文及中英文混合场景	8K/16K	否	公测版
    Lydia	Lydia	英中双语女声	英文场景	仅支持英文场景	8K/16K	否	公测版
    艾硕	Aishuo	自然男声	客服场景	仅支持英文场景	8K/16K	是	公测版
    青青	Qingqing	台湾话女声	方言场景	仅支持纯中文场景	8K/16K	否	公测版
    翠姐	Cuijie	东北话女声	方言场景	仅支持纯中文场景	8K/16K	否	公测版
    小泽	Xiaoze	湖南重口音男声	方言场景	仅支持纯中文场景	8K/16K	是	公测版
    调用限制
    传入文本必须采用UTF-8编码；
    传入文本不能超过300个字符。超过300字符的内容会被截断，只合成300字符以内的内容。
    服务地址
    访问类型	说明	URL
    外网访问	所有服务器均可使用外网访问URL（SDK中默认设置了外网访问URL，不需您设置）	wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1
    阿里云上海ECS内网访问	您使用阿里云上海ECS（即ECS地域为华东2(上海)），可使用内网访问URL。
    说明：使用内网访问方式，将不产生ECS实例的公网流量费用。
    ECS的经典网络不能访问AnyTunnel，即不能在内网访问语音服务；如果希望使用AnyTunnel，需要创建专有网络后在其内部访问。	ws://nls-gateway.cn-shanghai-internal.aliyuncs.com:80/ws/v1
    交互流程
    说明：交互流程图为Java SDK、C++ SDK、iOS SDK、Android SDK的交互流程，不包含RESTful API的交互流程，RESTful API的交互流程图请直接阅读RESTful API 2.0一节。

    tts

    说明：服务端的响应除了音频流之外，都会在返回信息的header包含task_id参数，用于表示本次识别任务的ID，请记录下这个值，如果发生错误，请将task_id和错误信息提交到工单。

    1. 鉴权
    客户端在与服务端建立WebSocket链接的时候，需要使用Token进行鉴权。Token获取请阅读 获取 Token一节。

    2. synthesis start
    客户端发送语音合成请求，其中在请求消息中需要进行参数设置，各参数由SDK中SpeechSynthesizer对象的相关set方法设置，各参数含义如下：

    参数	类型	是否必需	说明
    appkey	String	是	管控台创建的项目Appkey
    text	String	是	待合成文本，文本内容必须采用UTF-8编码，长度不超过300个字符（英文字母之间需要添加空格）
    voice	String	否	发音人，默认是xiaoyun
    format	String	否	音频编码格式，默认是pcm。支持的格式：pcm、wav、mp3
    sample_rate	Integer	否	音频采样率，默认是16000
    volume	Integer	否	音量，范围是0~100，默认50
    speech_rate	Integer	否	语速，范围是-500~500，默认是0
    pitch_rate	Integer	否	语调，范围是-500~500，默认是0
    3. synthesize audio data
    服务端开始返回合成的语音二进制数据，SDK接收并处理二进制数

    4. synthesis complete
    语音合成完毕，服务端发送合成完毕事件通知，示例如下：

    {
        "header": {
            "message_id": "05450bf69c53413f8d88aed1ee600e93",
            "task_id": "640bc797bb684bd69601856513079df5",
            "namespace": "SpeechSynthesizer",
            "name": "SynthesisCompleted",
            "status": 20000000,
            "status_message": "GATEWAY|SUCCESS|Success."
        }
    }
    温馨提示：文档提供的示例Demo中将合成的音频保存在了文件中，如果您需要播放音频且对实时性要求较高，建议使用流式播放，即边接收语音数据边播放，减少延时。

    服务状态码
    在服务的每一次响应中，都包含status字段，即服务状态码，状态码各种取值含义如下：

    通用错误：

    错误码	原因	解决办法
    40000001	身份认证失败	检查使用的令牌是否正确，是否过期
    40000002	无效的消息	检查发送的消息是否符合要求
    403	令牌过期或无效的参数	首先检查使用的令牌是否过期，然后检查参数值设置是否合理
    40000004	空闲超时	确认是否长时间（10秒）没有发送数据掉服务端
    40000005	请求数量过多	检查是否超过了并发连接数或者每秒钟请求数
    40000000	默认的客户端错误码	查看错误消息或提交工单
    50000000	默认的服务端错误	如果偶现可以忽略，重复出现请提交工单
    50000001	内部调用错误	如果偶现可以忽略，重复出现请提交工单
    网关错误：

    错误码	原因	解决办法
    40010001	不支持的接口	使用了不支持的接口，如果使用SDK请提交工单
    40010002	不支持的指令	使用了不支持的指令，如果使用SDK请提交工单
    40010003	无效的指令	指令格式错误，如果使用SDK请提交工单
    40010004	客户端提前断开连接	检查是否在请求正常完成之前关闭了连接
    40010005	任务状态错误	发送了当前任务状态不能处理的指令
    Meta错误：

    错误码	原因	解决办法
    40020105	应用不存在	检查应用appKey是否正确，是否与令牌归属同一个账号
    TTS错误：

    错误码	原因	解决办法
    41020001	参数错误	检查是否传递了正确的参数
    51020001	TTS服务端错误	如果偶现可以忽略，重复出现请提交工单
}
'''
