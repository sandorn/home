# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-25 11:34:01
#LastEditTime : 2020-06-01 21:28:41
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================

阿里云语音合成对接接口 - 简书
https://www.jianshu.com/p/3a462046b574

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

由SSML控制合成效果_由SSML控制合成效果_长文本语音合成_智能语音交互-阿里云
https://help.aliyun.com/knowledge_detail/146123.html?spm=a2c4g.11186631.2.5.4f6b485aLTLTLv

RESTful API_RESTful API_长文本语音合成_智能语音交互-阿里云
https://help.aliyun.com/knowledge_detail/130555.html?spm=a2c4g.11186631.2.4.4f6b485aLTLTLv

由SSML控制合成效果_语音合成_智能语音交互-阿里云
https://help.aliyun.com/document_detail/101645.html?spm=a2c4g.11174283.3.9.29807275qNaSDa

'''
import json
import time
from xjLib.mystr import md5, get_10_timestamp

from aliyunsdkcore.acs_exception.exceptions import ClientException, ServerException
from aliyunsdkcore.client import AcsClient  # 阿里云核心代码库
from aliyunsdkcore.request import CommonRequest  # 阿里云官方核心代码库

from ali_speech import NlsClient
from ali_speech.callbacks import SpeechSynthesizerCallback, SpeechTranscriberCallback
from ali_speech.constant import ASRFormat, ASRSampleRate
from ali_speech._create_token import AccessToken
from xjLib.mystr import string_split_join_with_maxlen_list

from xjLib.Requests import SessionClient

accessKeyId = 'LTAI4G5TRjsGy8BNKPtctjXQ'
accessKeySecret = 'hS8Kl0b9orxNUW7IOeBIFUfzgcVn00'
Appkey = 'Ofm34215thIUdSIX'


# 将全局使用的变量定义在类中
class G:
    token = ''
    expire_time = 0


def get_token(access_key_id=None, access_key_secret=None):
    if access_key_id is None:
        access_key_id = accessKeyId
    if access_key_secret is None:
        access_key_secret = accessKeySecret
    now = get_10_timestamp()
    if G.expire_time > now:
        return (G.token, G.expire_time)
    else:
        G.token, G.expire_time = AccessToken.create_token(access_key_id, access_key_secret)
    return (G.token, G.expire_time)


def ReqLongSynthesizer(appKey, token, longtext, audioFile='', format='wav', sampleRate=16000, voice='Aida', volume=100, speech_rate=0, pitch_rate=0, method='post', callback=None):
    '''
    #!长文本语音合成目前没有免费试用版
    NlsClient.getInstance()
    接口说明_接口说明_长文本语音合成_智能语音交互-阿里云
    https://help.aliyun.com/knowledge_detail/130509.html?spm=a2c4g.11186631.2.1.4f6b485aLTLTLv

    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/rest/v1/tts/async'
    '''
    long_text_list = string_split_join_with_maxlen_list(longtext)

    for text in long_text_list:
        ReqSynthesizer(appKey, token, text, audioFile=audioFile, format=format, sample_rate=sampleRate, voice=voice, volume=volume, speech_rate=speech_rate, pitch_rate=pitch_rate, method=method, callback=callback)


def ReqSynthesizer(appKey, token, text, audioFile='', format='wav', sample_rate=16000, voice='Aida', volume=100, speech_rate=0, pitch_rate=0, method='post', callback=None):
    result = {}
    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
    httpHeaders = {'Content-Type': 'application/json'}
    body_dict = {
        'appkey': appKey,
        'token': token,
        'text': text,
        'format': format,
        'sample_rate': sample_rate,
        'voice': voice,
        'volume': volume,
        'speech_rate': speech_rate,
        'pitch_rate': pitch_rate,
    }

    session = SessionClient()
    session.update_headers(httpHeaders)
    if method == 'get':
        res = session.get(url, params=body_dict)  # "https://httpbin.org/post"
    else:
        res = session.post(url, json=body_dict)  # "https://httpbin.org/post"

    if 'audio/mpeg' == res.headers['Content-Type']:
        result['data'] = res.content
        if audioFile == '':
            audioFile = md5(text)

        if audioFile is not None:
            result['filename'] = f'{audioFile}_{voice}_{round(sample_rate/1000)}K.{format}'
            with open(result['filename'], mode='wb') as f:
                f.write(res.content)
            print(result['filename'], 'Request succeed!')

        if callback:
            result['callback'] = callback(res.content)

    return result


class synthesizeClass:
    def __init__(self, appkey, token, text=None, audioFile='', format='wav', sample_rate=16000, voice='Aida', volume=100, speech_rate=0, pitch_rate=0, callback=None, method='post'):
        self.session = SessionClient()
        self.session.update_headers({'Content-Type': 'application/json'})
        self.method = method
        self.callback = callback
        self.url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
        self.appkey = appkey
        self.token = token
        self.text = text
        self.audioFile = audioFile
        self.format = format
        self.sample_rate = sample_rate
        self.voice = voice
        self.volume = volume
        self.speech_rate = speech_rate
        self.pitch_rate = pitch_rate
        self.result = {}
        self.body_dict = {'appkey': self.appkey, 'token': self.token, 'text': self.text, 'format': self.format, 'sample_rate': self.sample_rate, 'voice': self.voice, 'volume': self.volume, 'speech_rate': self.speech_rate, 'pitch_rate': self.pitch_rate}

    # #设置参数，更新body_dict
    def setparams(self, attr, value):
        self.__setattr__(attr, value)
        if attr == 'text':
            self.audioFile = md5(text)
        if attr in self.body_dict.keys():
            self.body_dict[attr] = value

    def run(self, params=None, data=None, json=None, **kwargs):

        if self.method == 'post':
            if json is None and data is None:
                json = self.body_dict
            self.result['response'] = self.session.post(self.url, data=data, json=json, **kwargs)
        else:
            if params is None:
                params = self.body_dict
            response = self.session.get(self.url, params=params, **kwargs)
        return self.makeResult(response)

    def makeResult(self, res):
        if 'audio/mpeg' == self.result['response'].headers['Content-Type']:
            self.result['data'] = res.content
            if self.audioFile == '':
                self.audioFile = md5(text)
            if self.audioFile is not None:
                self.result['filename'] = f'{self.audioFile}_{self.voice}_{round(self.sample_rate/1000)}K.{self.format}'
                with open(self.result['filename'], mode='wb') as f:
                    f.write(res.content)
                print(self.result['filename'], 'Request succeed!')

            if self.callback:
                self.result['callback'] = self.callback(res.content)

        return self.result


class Synthesizer_MyCallback(SpeechSynthesizerCallback):
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
        print('MyCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (message['header']['task_id'], message['header']['status_text']))
        self._fout.close()

    def on_channel_closed(self):
        print('MyCallback.OnRecognitionChannelClosed')


def Synthesizerprocess(appkey, token, text, audioFile='', format='wav', sampleRate=16000, voice='Aida', volume=100, speech_rate=0, pitch_rate=0, callback=Synthesizer_MyCallback):
    client = NlsClient()
    client.set_log_level('INFO')
    if audioFile == '':
        audioFile = md5(text)
    filename = f'{audioFile}_{voice}_{round(sampleRate/1000)}K.{format}'
    # callback = SynthesizerMyCallback(filename)
    synthesizer = client.create_synthesizer(callback(filename))
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
        print('TranscriberCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (self._name, message['header']['task_id'], message['payload']['result']))

    def on_sentence_begin(self, message):
        print('TranscriberCallback.on_sentence_begin: file: %s, task_id: %s, sentence_id: %s, time: %s' % (self._name, message['header']['task_id'], message['payload']['index'], message['payload']['time']))

    def on_sentence_end(self, message):
        print('TranscriberCallback.on_sentence_end: file: %s, task_id: %s, sentence_id: %s, time: %s, result: %s' % (self._name, message['header']['task_id'], message['payload']['index'], message['payload']['time'], message['payload']['result']))

        self.result = message['payload']['result']

    def on_completed(self, message):
        print('TranscriberCallback.OnRecognitionCompleted: %s' % message)

    def on_task_failed(self, message):
        print('TranscriberCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (message['header']['task_id'], message['header']['status_text']))

    def on_channel_closed(self):
        print('TranscriberCallback.OnRecognitionChannelClosed')


def TranscriberProcess(appkey, token, filepath):
    '''本地音频文件识别
    Python SDK_实时语音识别_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/120698.html?spm=a2c4g.11186623.6.577.2579259eScpzA7
    支持音频编码格式：pcm(无压缩的pcm文件或wav文件)，16bit采样位数的单声道(mono)
    '''
    client = NlsClient()
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
        return {callback._name: callback.result, 'name': callback._name, 'result': callback.result}


def APITransUrl(akId, akSecret, appKey, urlLink, enable_words=False, auto_split=False):
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

    task = {'appkey': appKey, 'file_link': urlLink, 'version': "4.0", 'enable_words': enable_words, 'auto_split': auto_split}  # 开启智能分轨
    postRequest.add_body_params("Task", json.dumps(task))

    taskId = ""

    try:
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
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


def PostTransFile(appKey, token, audioFile, format='wav', sampleRate=16000, enablePunctuationPrediction=False, enableInverseTextNormalization=True, enableVoiceDetection=True):
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

    with open(audioFile, mode='rb') as f:
        audioContent = f.read()

    # 设置HTTPS Headers
    httpHeaders = {
        'X-NLS-Token': token,
        'Content-type': 'application/octet-stream',
        'Content-Length': str(len(audioContent)),
    }

    session = SessionClient()
    session.update_headers(httpHeaders)
    response = session.post(request, data=audioContent)  # "https://httpbin.org/post"
    body_json = response.json
    status = body_json['status']
    if status == 20000000:
        result = body_json['result']
    # print(1111, result, type(body_json))
    return result, body_json


if __name__ == "__main__":
    token = get_token()[0]
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

    '''
    filepath = "D:/alibabacloud-nls-python-sdk/nls-sample-16k.wav"
    urlLink = "https://aliyun-nls.oss-cn-hangzhou.aliyuncs.com/asr/fileASR/examples/nls-sample-16k.wav"
    text = '根据北京银保监局近期工作部署要求，盛唐融信迅速响应，立即成立专项整治小组，由公司总经理毕永辉任整治小组组长，成员包括公司副总经理刘新军、行政人事部总经理朱立志。'
    # #长文字合成语音
    long_text_list = string_split_join_with_maxlen_list(longtext)
    from xjLib.Pygame import ReqSynthesizer_Thread_read

    ReqSynthesizer_Thread_read(long_text_list)
    ReqLongSynthesizer(Appkey, token, longtext)

    # #短文字合成语音，限定300字符
    SYC = synthesizeClass(Appkey, token, text )
    res = SYC.run()
    SYC.setparams('text', text2)
    from xjLib.Pygame import play_callback
    SYC.setparams('callback', play_callback)  # 设置回调
    res = SYC.run()
    print(3333, SYC.result['filename'])
    #  处理结果
    #  play_callback(SYC.result['response'].content)

    ReqSynthesizer(Appkey, token, text, audioSaveFile='audioSaveFile' )

    filename = Synthesizerprocess(Appkey, token, text )
    print(filename)
    # #将文本分解为300字符以内一段，生成list
    from xjLib.mystr import string_split_join_with_maxlen_list
    # #短文字合成语音，使用SSML
    ssml_text_list = ['<speak' + item for item in ssml_text.split('<speak') if item.strip()]
    for index, item in enumerate(ssml_text_list):
        print(index, item)
    from xjLib.Pygame import ReqSynthesizer_Thread_read

    ReqSynthesizer_Thread_read(ssml_text_list)
    # #网络音频文件识别
    text, res = APITransUrl(accessKeyId, accessKeySecret, Appkey, urlLink)
    print('网络音频文件识别', text, res)

    # # 本地音频文件识别
    text, res  = PostTransFile(Appkey, token, filepath)  ##一句话识别，1分钟以内

    res = TranscriberProcess(None, Appkey, token, filepath)
    print('本地音频文件识别', res, res['result'], '|||', res['name'])

{
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
    各参数含义如下：

    参数	类型	是否必需	说明
    appkey	String	是	管控台创建的项目Appkey
    text	String	是	待合成文本，文本内容必须采用UTF-8编码，长度不超过300个字符（英文字母之间需要添加空格）
    voice	String	否	发音人，默认是xiaoyun
    format	String	否	音频编码格式，默认是pcm。支持的格式：pcm、wav、mp3
    sample_rate	Integer	否	音频采样率，默认是16000
    volume	Integer	否	音量，范围是0~100，默认50
    speech_rate	Integer	否	语速，范围是-500~500，默认是0
    pitch_rate	Integer	否	语调，范围是-500~500，默认是0

    服务状态码通用错误：

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
