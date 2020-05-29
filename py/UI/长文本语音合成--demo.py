# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-27 19:00:56
#LastEditTime : 2020-05-27 21:11:53
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

# -*- coding: UTF-8 -*-
# Python 2.x
import http.client
import urllib3
import json
import time


class TtsHeader:

    def __init__(self, app_key, token):
        self.appkey = app_key
        self.token = token

    def tojson(self, e):
        return {'appkey': e.appkey, 'token': e.token}


class TtsContext:

    def __init__(self, device_id):
        self.device_id = device_id

    #将序列化函数定义到类中
    def tojson(self, e):
        return {'device_id': e.device_id}


class TtsRequest:

    def __init__(self, voice, sample_rate, format, enable_subtitle, text):
        self.voice = voice
        self.sample_rate = sample_rate
        self.format = format
        self.enable_subtitle = enable_subtitle
        self.text = text

    def tojson(self, e):
        return {
            'voice': e.voice,
            'sample_rate': e.sample_rate,
            'format': e.format,
            'enable_subtitle': e.enable_subtitle,
            'text': e.text
        }


class TtsPayload:

    def __init__(self, enable_notify, notify_url, tts_request):
        self.enable_notify = enable_notify
        self.notify_url = notify_url
        self.tts_request = tts_request

    def tojson(self, e):
        return {
            'enable_notify': e.enable_notify,
            'notify_url': e.notify_url,
            'tts_request': e.tts_request.tojson(e.tts_request)
        }


class TtsBody:

    def __init__(self, tts_header, tts_context, tts_payload):
        self.tts_header = tts_header
        self.tts_context = tts_context
        self.tts_payload = tts_payload

    def tojson(self, e):
        return {
            'header': e.tts_header.tojson(e.tts_header),
            'context': e.tts_context.tojson(e.tts_context),
            'payload': e.tts_payload.tojson(e.tts_payload)
        }


# 根据特定信息轮询检查某个请求在服务端的合成状态，轮询操作非必须，如果设置了回调url，则服务端会在合成完成后主动回调
def waitLoop4Complete(url, appkey, token, task_id, request_id):
    fullUrl = url + "?appkey=" + appkey + "&task_id=" + task_id + "&token=" + token + "&request_id=" + request_id
    print("fullUrl=", fullUrl)
    host = {
        "Host": "nls-gateway.cn-shanghai.aliyuncs.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        'Content-Type': 'application/json'
    }
    while True:
        req = urllib3.Request(url=fullUrl)
        result = urllib3.urlopen(req).read()
        print("query result = ", result)
        jsonData = json.loads(result)
        if jsonData.has_key("error_code") and jsonData[
                "error_code"] == 20000000 and jsonData.has_key("data") and (
                    jsonData["data"]["audio_address"] != ""):
            print("Tts Finished! task_id = " + jsonData["data"]["task_id"])
            print("Tts Finished! audio_address = " +
                  jsonData["data"]["audio_address"])
            break
        else:
            print("Tts Running...")
            time.sleep(3)


# 长文本语音合成restful接口，支持post调用，不支持get请求，发出请求后，可以轮询状态或者等待服务端合成后自动回调(如果设置了回调参数)
def requestLongTts4Post(tts_body, appkey, token):
    host = 'nls-gateway.cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/rest/v1/tts/async'
    # 设置HTTP Headers
    http_headers = {'Content-Type': 'application/json'}
    print('The POST request body content: ' + tts_body, type(tts_body))
    conn = http.client.HTTPSConnection(host)
    #conn = http.client.HTTPConnection(host)
    conn.request(method='POST', url=url, body=tts_body, headers=http_headers)
    response = conn.getresponse()
    print('Response status and response reason:', response.status,
          response.reason, response.headers, response.getheader('Content-Type'))
    body = response.read()
    if response.status == 200:
        jsonData = json.loads(body)
        print('The request succeed : ', jsonData)
        print('error_code = ', jsonData['error_code'])
        task_id = jsonData['data']['task_id']
        request_id = jsonData['request_id']
        print('task_id = ', task_id)
        print('request_id = ', request_id)
        # 说明：轮询检查服务端的合成状态，轮询操作非必须，如果设置了回调url，则服务端会在合成完成后主动回调
        waitLoop4Complete(url, appkey, token, task_id, request_id)
    else:
        print('The request failed: ' + str(body))


from xjLib.xt_ui.alispeak import get_ali_token
appkey = 'Ofm34215thIUdSIX'
token = get_ali_token()[0]

text = '原本正该艳阳高照，天空却笼罩了厚厚的乌云，黑得有若夜晚降临'
# 拼接Http Post请求的消息体内容
th = TtsHeader(appkey, token)
tc = TtsContext("mydevice")
# 发音人， 采样率， 语音格式， 待合成文本内容
tr = TtsRequest("xiaoyun", 16000, "wav", False, text)
# 是否设置回调url， 回调url地址，TtsRequest对象
tp = TtsPayload(True, "http://134.com", tr)
tb = TtsBody(th, tc, tp)
body = json.dumps(tb, default=tb.tojson)
requestLongTts4Post(str(body), appkey, token)
