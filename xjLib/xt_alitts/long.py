# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-08-30 09:13:46
LastEditTime : 2024-08-30 09:13:46
FilePath     : /CODE/xjLib/xt_alitts/long.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import http.client
import json
import time
import urllib.request

from xt_alitts.cfg import Constant


class TtsHeader:
    def __init__(self, appkey, token):
        self.appkey = appKey
        self.token = token

    def tojson(self, e):
        return {"appkey": e.appkey, "token": e.token}


class TtsContext:
    def __init__(self, device_id):
        self.device_id = device_id

    # 将序列化函数定义到类中。

    def tojson(self, e):
        return {"device_id": e.device_id}


class TtsRequest:
    def __init__(self, voice, sample_rate, format, enable_subtitle, text):
        self.voice = voice
        self.sample_rate = sample_rate
        self.format = format
        self.enable_subtitle = enable_subtitle
        self.text = text

    def tojson(self, e):
        return {
            "voice": e.voice,
            "sample_rate": e.sample_rate,
            "format": e.format,
            "enable_subtitle": e.enable_subtitle,
            "text": e.text,
        }


class TtsPayload:
    def __init__(self, enable_notify, notify_url, tts_request):
        self.enable_notify = enable_notify
        self.notify_url = notify_url
        self.tts_request = tts_request

    def tojson(self, e):
        return {
            "enable_notify": e.enable_notify,
            "notify_url": e.notify_url,
            "tts_request": e.tts_request.tojson(e.tts_request),
        }


class TtsBody:
    def __init__(self, tts_header, tts_context, tts_payload):
        self.tts_header = tts_header
        self.tts_context = tts_context
        self.tts_payload = tts_payload

    def tojson(self, e):
        return {
            "header": e.tts_header.tojson(e.tts_header),
            "context": e.tts_context.tojson(e.tts_context),
            "payload": e.tts_payload.tojson(e.tts_payload),
        }


# 根据特定信息轮询检查某个请求在服务端的合成状态，每隔10秒钟轮询一次状态.轮询操作非必须，如果设置了回调url，则服务端会在合成完成后主动回调。


def waitLoop4Complete(url, appkey, token, task_id, request_id):
    # fullUrl = url + "?appkey=" + appkey + "&task_id=" + task_id + "&token=" + token + "&request_id=" + request_id

    fullUrl = (
        url
        + "?appkey="
        + appkey
        + "&task_id="
        + task_id
        + "&token="
        + token
        + "&request_id="
        + request_id
    )

    print("fullUrl=", fullUrl)
    host = {
        "Host": "nls-gateway-cn-shanghai.aliyuncs.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
    }
    while True:
        result = urllib.request.urlopen(fullUrl).read()
        print("query result = ", result)
        jsonData = json.loads(result)

        # jsonData["data"]["audio_address"] is None表示还在未合成完成的状态...每隔10秒钟轮询一次状态
        if jsonData["data"]["audio_address"] is None:
            print(" Tts Queuing...please wait...")
            time.sleep(10)
        elif (
            "error_code" in jsonData
            and jsonData["error_code"] == 20000000
            and "data" in jsonData
            and (jsonData["data"]["audio_address"] != "")
        ):
            print("Tts Finished! task_id = " + jsonData["data"]["task_id"])
            print("Tts Finished! audio_address = " + jsonData["data"]["audio_address"])
            break

        else:
            print("Tts Running...")
            time.sleep(10)


# 长文本语音合成restful接口，支持post调用，不支持get请求。发出请求后，可以轮询状态或者等待服务端合成后自动回调（如果设置了回调参数）。


def requestLongTts4Post(tts_body, appkey, token):
    host = "nls-gateway.cn-shanghai.aliyuncs.com"
    url = "https://" + host + "/rest/v1/tts/async"
    #    'https://nls-gateway-cn-shanghai.aliyuncs.com/rest/v1/tts/async'
    # 设置HTTP Headers
    http_headers = {"Content-Type": "application/json"}
    print("The POST request body content: " + tts_body)
    conn = http.client.HTTPSConnection(host)
    # conn = httplib.HTTPConnection(host)
    conn.request(method="POST", url=url, body=tts_body, headers=http_headers)
    response = conn.getresponse()
    print("Response status and response reason:")
    print(response.status, response.reason)
    contentType = response.getheader("Content-Type")
    print(contentType)
    body = response.read()
    if response.status == 200:
        jsonData = json.loads(body)
        print("The request succeed : ", jsonData)
        print("error_code = ", jsonData["error_code"])
        task_id = jsonData["data"]["task_id"]
        request_id = jsonData["request_id"]
        print("task_id = ", task_id)
        print("request_id = ", request_id)
        # 说明：轮询检查服务端的合成状态，轮询操作非必须。如果设置了回调url，则服务端会在合成完成后主动回调。
        waitLoop4Complete(url, appkey, token, task_id, request_id)
    else:
        print("The request failed: " + str(body))


if __name__ == "__main__":
    appKey = Constant().appKey
    token = Constant().token
    text = "今天是周一，天气挺好的。"

    # 拼接HTTP Post请求的消息体内容。
    th = TtsHeader(appKey, token)
    tc = TtsContext("mydevice")
    # TtsRequest对象内容为：发音人、采样率、语音格式、待合成文本内容。
    tr = TtsRequest("xiaoyun", 16000, "wav", False, text)
    # 是否设置回调url，回调url地址，TtsRequest对象。
    tp = TtsPayload(True, "http://134.com", tr)
    tb = TtsBody(th, tc, tp)
    body = json.dumps(tb, default=tb.tojson)
    requestLongTts4Post(str(body), appKey, token)
