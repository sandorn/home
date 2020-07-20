# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-25 11:34:01
#FilePath     : /xjLib/xt_Alispeech/__init__.py
#LastEditTime : 2020-07-20 15:09:07
# Github       : https://github.com/sandorn/home
# ==============================================================
'''
import json
import time

from aliyunsdkcore.acs_exception.exceptions import (ClientException, ServerException)
from aliyunsdkcore.client import AcsClient  # 阿里云核心代码库
from aliyunsdkcore.request import CommonRequest  # 阿里云官方核心代码库

from ali_speech import NlsClient
from ali_speech.callbacks import (SpeechSynthesizerCallback, SpeechTranscriberCallback)
from .conf import Constant  # 常量参数
from .conf import SpeechArgs  # 默认参数
from .conf import SynResult, TransResult
from xt_Requests import SessionClient
from xt_String import md5, string_split_limited_list


def ReqLongSynthesizer(longtext, savefile=True, method='post', callback=None):
    '''长文本语音合成目前没有免费试用版'''
    res_list = []
    long_text_list = string_split_limited_list(longtext)
    for text in long_text_list:
        res = ReqSynthesizer(text, savefile=savefile, method=method, callback=callback)
        res_list.append(res)
    return res_list


def ReqSynthesizer(text, format='wav', savefile=True, method='post', callback=None):
    result = SynResult()
    url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
    args_dict = SpeechArgs().get_dict()  # class_add_dict(SpeechArgs())
    args_dict['format'] = format  # #更新
    args_dict['text'] = text  # 添加

    session = SessionClient()
    result.response = session[method](url, params=args_dict, json=args_dict, headers={'Content-Type': 'application/json'}).raw

    if 'audio/mpeg' == result.response.headers['Content-Type']:

        if savefile:
            result.filename = f'''{md5(text)}_{ args_dict['voice'] }_{args_dict['sample_rate']//1000}K.{args_dict['format']}'''
            with open(result.filename, mode='wb') as f:
                f.write(result.response.content)
            print(result.filename, 'Request succeed!')

        if callback:
            result.callback = callback(result.response.content)

    return result


class synthesizeClass:
    def __init__(self, text=None, savefile=True, callback=None, method='post'):
        self.session = SessionClient()
        self.method = method
        self.callback = callback
        self.url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts'
        self.savefile = savefile
        self.result = SynResult()
        self.args_dict = SpeechArgs().get_dict()
        self.args_dict['text'] = text  # 添加

    def setparams(self, attr, value):
        if attr in self.args_dict.keys():
            self.args_dict[attr] = value
        elif hasattr(self, attr):
            setattr(self, attr, value)

    def run(self):
        res = self.session[self.method](self.url, params=self.args_dict, json=self.args_dict, headers={'Content-Type': 'application/json'}).raw
        self.result.response = res
        return self._handle_result()

    def _handle_result(self):
        if 'audio/mpeg' == self.result.response.headers['Content-Type']:

            if self.savefile:
                self.result.filename = f'''{md5(self.args_dict['text'] )}_{self.args_dict['voice'] }_{self.args_dict['sample_rate'] //1000}K.{self.args_dict['format']}'''
                with open(self.result.filename, mode='wb') as f:
                    f.write(self.result.response.content)
                print(self.result.filename, 'Request succeed!')

            if self.callback:
                self.result.callback = self.callback(self.result.response.content)

        return self.result


class Synthesizer_MyCallback(SpeechSynthesizerCallback):
    # #文字转音频，使用回调方式
    # #参数name用于指定保存音频的文件
    def __init__(self, name):
        self._name = name
        self._fout = open(name, 'wb')
        self.result = SynResult()
        self.result.filename = self._name
        self.result.callback = 'Synthesizer_MyCallback'

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


def Synthesizerprocess(text, callback=Synthesizer_MyCallback):
    client = NlsClient()
    client.set_log_level('INFO')
    args_dict = SpeechArgs().get_dict()
    args_dict['format'] = format  # #更新
    args_dict['text'] = text  # 添加
    audioFile = md5(text)
    filename = f'''{audioFile}_{args_dict['voice']}_{args_dict['sample_rate']//1000}K.{args_dict['format']}'''
    callbackfunc = callback(filename)
    synthesizer = client.create_synthesizer(callbackfunc)
    synthesizer.set_appkey(args_dict['appkey'])
    synthesizer.set_token(args_dict['token'])
    synthesizer.set_voice(args_dict['voice'])
    synthesizer.set_text(text)
    synthesizer.set_format(args_dict['format'])
    synthesizer.set_sample_rate(args_dict['sample_rate'])
    synthesizer.set_volume(args_dict['volume'])
    synthesizer.set_speech_rate(args_dict['speech_rate'])
    synthesizer.set_pitch_rate(args_dict['pitch_rate'])

    try:
        ret = synthesizer.start()
        if ret < 0:
            return ret

        synthesizer.wait_completed()
    except Exception as e:
        print(e)
    finally:
        synthesizer.close()
        return callbackfunc.result


class TranscriberCallback(SpeechTranscriberCallback):
    """
    构造函数的参数没有要求，可根据需要设置添加
    示例中的name参数可作为待识别的音频文件名，用于在多线程中进行区分
    """
    def __init__(self, name='default'):
        self._name = name
        self.result = TransResult()
        self.result.name = self._name

    def on_started(self, message):
        print('TranscriberCallback.OnRecognitionStarted: %s' % message)

    def on_result_changed(self, message):
        print('TranscriberCallback.OnRecognitionResultChanged: file: %s, task_id: %s, result: %s' % (self._name, message['header']['task_id'], message['payload']['result']))

    def on_sentence_begin(self, message):
        print('TranscriberCallback.on_sentence_begin: file: %s, task_id: %s, sentence_id: %s, time: %s' % (self._name, message['header']['task_id'], message['payload']['index'], message['payload']['time']))
        self.result.task_id = message['header']['task_id']

    def on_sentence_end(self, message):
        print('TranscriberCallback.on_sentence_end: file: %s, task_id: %s, sentence_id: %s, time: %s, result: %s' % (self._name, message['header']['task_id'], message['payload']['index'], message['payload']['time'], message['payload']['result']))
        self.result.text = message['payload']['result']

    def on_completed(self, message):
        print('TranscriberCallback.OnRecognitionCompleted: %s' % message)

    def on_task_failed(self, message):
        print('TranscriberCallback.OnRecognitionTaskFailed-task_id:%s, status_text:%s' % (message['header']['task_id'], message['header']['status_text']))

    def on_channel_closed(self):
        print('TranscriberCallback.OnRecognitionChannelClosed')


def TranscriberProcess(filepath):
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
    transcriber.set_appkey(Constant().appKey)
    transcriber.set_token(Constant().token)
    transcriber.set_format('pcm')
    transcriber.set_sample_rate(16000)
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
        return callback.result


def PostTransFile(audioFile, format='wav', sampleRate=16000, enablePunctuationPrediction=False, enableInverseTextNormalization=True, enableVoiceDetection=True):
    '''
    一句话识别RESTful API支持以POST方式整段上传不超过一分钟的语音文件
    RESTful API_一句话识别_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/92131.html?spm=5176.10695662.1996646101.searchclickresult.249745f65JYpsf
    '''
    result = TransResult()
    result.name = audioFile
    url = 'http://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/asr'
    # 设置RESTful请求参数
    request = url + '?appkey=' + Constant().appKey
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
        'X-NLS-Token': Constant().token,
        'Content-type': 'application/octet-stream',
        'Content-Length': str(len(audioContent)),
    }

    session = SessionClient()
    session.update_headers(httpHeaders)
    response = session.post(request, data=audioContent)  # "https://httpbin.org/post"
    result.response = response.json
    result.task_id = response.json['task_id']
    status = result.response['status']
    if status == 20000000:
        result.text = result.response['result']
    # print(1111, result, type(body_json))
    return result


def APITransUrl(urlLink, enable_words=False, auto_split=False):
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
    result = TransResult()
    result.name = urlLink
    # 创建AcsClient实例
    client = AcsClient(Constant().accessKeyId, Constant().accessKeySecret, "cn-shanghai")
    # 提交录音文件识别请求
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name("SubmitTask")
    postRequest.set_method('POST')

    task = {
        'appkey': Constant().appKey,
        'file_link': urlLink,
        'version': "4.0",
        'enable_words': enable_words,
        'auto_split': auto_split,  # 开启智能分轨
    }
    postRequest.add_body_params("Task", json.dumps(task))

    try:
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        statusText = postResponse['StatusText']
        if statusText == 'SUCCESS':
            print("网络音频文件识别请求成功响应！")
            result.task_id = postResponse['TaskId']
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
    getRequest.add_query_param('TaskId', result.task_id)

    # 以轮询的方式进行识别结果的查询，直到服务端返回的状态描述符为"SUCCESS"、"SUCCESS_WITH_NO_VALID_FRAGMENT"，或者为错误描述，则结束轮询。
    statusText = ""

    while True:
        try:
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            statusText = getResponse['StatusText']
            if statusText == 'RUNNING' or statusText == 'QUEUEING':
                # 继续轮询
                time.sleep(10)
            else:
                result.response = getResponse
                result.text = getResponse['Result']['Sentences'][0]['Text']
                # print(2222, Result)
                # 退出轮询
                break

        except (ServerException, ClientException) as err:
            print(err)

    if statusText == 'SUCCESS':
        print("录音文件识别成功！")
    else:
        print("录音文件识别失败！")

    return result


'''
    阿里云语音合成对接接口 - 简书
    https://www.jianshu.com/p/3a462046b574

    RAM访问控制
    https://ram.console.aliyun.com/users/sandorn_ram

    由SSML控制合成效果_由SSML控制合成效果_长文本语音合成_智能语音交互-阿里云
    https://help.aliyun.com/knowledge_detail/146123.html?spm=a2c4g.11186631.2.5.4f6b485aLTLTLv

    RESTful API_RESTful API_长文本语音合成_智能语音交互-阿里云
    https://help.aliyun.com/knowledge_detail/130555.html?spm=a2c4g.11186631.2.4.4f6b485aLTLTLv

    由SSML控制合成效果_语音合成_智能语音交互-阿里云
    https://help.aliyun.com/document_detail/101645.html?spm=a2c4g.11174283.3.9.29807275qNaSDa

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
'''
