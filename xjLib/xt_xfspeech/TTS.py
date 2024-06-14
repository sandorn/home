# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-11-08 09:15:07
LastEditTime : 2023-11-08 09:15:53
FilePath     : /CODE/xjLib/xt_xfspeech/TTS.py
Github       : https://github.com/sandorn/home
==============================================================
https://www.xfyun.cn/doc/tts/online_tts/API.html#%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B
错误码链接:https://www.xfyun.cn/document/error-code [code返回错误码时必看]
"""

import _thread as thread
import base64
import hashlib
import hmac
import json
import os
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
from xt_xfspeech.cfg import APPID, APIKey, APISecret

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param:
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {'app_id': self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            'aue': 'lame',
            'auf': 'audio/L16;rate=16000',
            'vcn': 'xiaoyan',
            'tte': 'utf8',
            'speed': 50,
            'volume': 50,
            'pitch': 50,
        }
        self.Data = {
            'status': 2,
            'text': str(base64.b64encode(self.Text.encode('utf-8')), 'UTF8'),
        }
        # 使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        # self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = 'host: ' + 'ws-api.xfyun.cn' + '\n'
        signature_origin += 'date: ' + date + '\n'
        signature_origin += 'GET ' + '/v2/tts ' + 'HTTP/1.1'
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = 'api_key="{}", algorithm="{}", headers="{}", signature="{}"'.format(self.APIKey, 'hmac-sha256', 'host date request-line', signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {'authorization': authorization, 'date': date, 'host': 'ws-api.xfyun.cn'}
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message['code']
        sid = message['sid']
        audio = message['data']['audio']
        audio = base64.b64decode(audio)
        status = message['data']['status']
        print(message)
        if status == 2:
            print('ws is closed')
            ws.close()
        if code != 0:
            errMsg = message['message']
            print(f'sid:{sid} call error:{errMsg} code is:{code}')
        else:
            with open('./demo.mp3', 'ab') as f:
                f.write(audio)

    except Exception as e:
        print('receive msg,but parse exception:', e)


# 收到websocket错误的处理
def on_error(ws, *args):
    print('### error:', *args)


# 收到websocket关闭的处理
def on_close(ws, *args):
    print('### closed ###', *args)


# 收到websocket连接建立的处理


def Ws_Run(strtext=None):
    # 收到websocket连接建立的处理
    def on_open(ws):
        def run(*args):
            d = {
                'common': wsParam.CommonArgs,
                'business': wsParam.BusinessArgs,
                'data': wsParam.Data,
            }
            d = json.dumps(d)
            print('------>开始发送文本数据')
            ws.send(d)
            if os.path.exists('./demo.mp3'):
                os.remove('./demo.mp3')

        thread.start_new_thread(run, ())

    wsParam = Ws_Param(
        APPID=APPID,
        APISecret=APISecret,
        APIKey=APIKey,
        Text=strtext or '这是一个语音合成示例',
    )
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})


if __name__ == '__main__':
    str1 = """
    2023年，子公司管理部根据公司“正规化、体系化、制度化、专业化”的管理要求，调整原有的投后管理为主的模式，现阶段对子公司的管理会以财务管控型为主、局部操作型管控为辅。根据管理需求，选聘管理人员充实子公司经营管理层、建立并完善子公司管理制度、整理母子公司管理流程并稳妥推进优化、开展经营及离任审计并严肃处理有关违规违纪人员，积极跟进整改审计发现的问题；根据子公司不同业态和发展阶段差异，有侧重点的编制2024年经营计目标，匹配相对应的组织绩效考核体系，为子公司发展步入正轨打下了坚实的基础。
    """
    Ws_Run(str1)
