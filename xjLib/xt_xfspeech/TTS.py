# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-11-08 09:15:07
LastEditTime : 2023-11-08 09:15:53
FilePath     : /CODE/xjLib/xt_xfspeech/TTS.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import os
import ssl
from datetime import datetime
from time import mktime
from typing import Text
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
from xt_xfspeech.cfg import APPID, APIKey, APISecret

#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，
        # 更多个性化参数在 https://console.xfyun.cn/services/tts
        self.BusinessArgs = {
            "aue": "lame",
            "auf": "audio/L16;rate=16000",
            "vcn": "x2_xiaohou",
            # "xiaoyan",  "x4_lingfeizhe_zl"
            "tte": "utf8",
            "speed": 50,
            "volume": 50,
            "pitch": 50,
        }
        self.Data = {
            "status": 2,
            "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")
        }
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += f"date: {date}" + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'),
                                 signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(
            encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line",
            signature_sha)
        authorization = base64.b64encode(
            authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        return f'{url}?{urlencode(v)}'


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(message)
        if status == 2:
            print("on_message ||| ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print(f"sid:{sid} call error:{errMsg} code is:{code}")
        else:

            with open('./demo.mp3', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws, *args):
    print('''### closed ###''', ws, args)


def Ws_Run(strtext=None):
    # 收到websocket连接建立的处理
    def on_open(ws):

        def run(*args):
            d = {
                "common": wsParam.CommonArgs,
                "business": wsParam.BusinessArgs,
                "data": wsParam.Data,
            }

            d = json.dumps(d)
            print("------>开始发送文本数据")
            ws.send(d)
            if os.path.exists('./demo.mp3'):
                os.remove('./demo.mp3')

        thread.start_new_thread(run, ())

    wsParam = Ws_Param(APPID=APPID,
                       APISecret=APISecret,
                       APIKey=APIKey,
                       Text=strtext or "这是一个语音合成示例")

    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    str1 = '''
你从小靠翻垃圾吃剩饭
含辛茹苦十年将四个妹妹养大成人
至此落得癌症晚期
却仍躲在地下室吃着过期的方便面
可如今身价千亿的妹妹们
明知道你的情况
却不愿意掏一分钱来救你
因为你在她们心中是一个人渣
是一个S害养父母的变态
在她们眼中
你只是想要父母留下的千万家产
但这一切的真相只有你自己知道
在小时候被养父母领养后
才知道他们其实是对变态夫妻
每当养父要对妹妹们拳脚相加时
你都会及时阻止
并让他把怒火发泄到你的身上
也许是老天看不过眼
一场车祸把两夫妻带走
留下了你们兄妹5人
但随之而来的是巨额的负债
和数不清的麻烦
为了不露宿街头
你拼命的赚钱
把吃的全给4个妹妹
自己却一直饿着肚子
可就算这样
她们也没有改变对你的看法
    '''
    Ws_Run(str1)
