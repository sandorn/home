# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-19 08:41:17
FilePath     : /CODE/xjLib/xt_alitts/cfg.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import configparser
from typing import Optional

from nls.token import getToken
from pydantic import BaseModel, Field
from xt_class import ReDictMixin
from xt_enum import StrEnum

config = configparser.ConfigParser()
config.read(".vscode/CFG.ini")


class Constant:
    """Constant : 常量参数"""

    appKey = config.get("AliTTS", "ACCESS_APPKEY")
    accessKeyId = config.get("AliTTS", "ACCESS_KeyId")
    accessKeySecret = config.get("AliTTS", "ACCESS_Secret")

    token = property(lambda cls: getToken(cls.accessKeyId, cls.accessKeySecret))

    @property  # 第二种方法
    def _token(self):
        return getToken(self.accessKeyId, self.accessKeySecret)


class SpeechArgs(BaseModel, ReDictMixin):
    """TTS参数"""

    text: str = Field(" ", min_length=1)  # 假设text字段必须提供
    long_tts: bool = False
    aformat: str = "wav"  # 合成出来音频的格式，默认为pcm。支持pcm、wav、mp3
    sample_rate: int = 16000  # 识别音频采样率，默认值：16000 Hz。支持16000、8000
    voice: str = "aifei"  # 发音人，默认为xiaoyun
    volume: int = 50  # 音量大小，取值范围0~100，默认值：50
    speech_rate: int = 0  # 语速，取值范围-500~500，默认值：0
    pitch_rate: int = 0  # 语调，取值范围-500~500，默认值：0
    wait_complete: bool = True  # 是否阻塞到合成完成
    start_timeout: int = 10  # 和云端连接建立超时，默认值：10秒
    completed_timeout: int = 60  # 从连接建立到合成完成超时，默认值：60秒
    ping_interval: int = 8  # Ping包发送间隔，默认值：8秒。无需间隔可设置为0或None。
    ping_timeout: Optional[int] = None
    # 是否检查Pong包超时，默认值：None。None为不检查Pong包是否超时。
    ex: dict = {}  # 用户提供的额外参数，该字典内容会以key:value形式合并进请求的payload段中，详情可参见接口说明章节中的请求数据 {'enable_subtitle': True},  #输出每个字在音频中的时间位置


class Voice(StrEnum):
    xiaoyun = ("xiaoyun", "小云")
    aida = ("aida", "艾达")
    ailun = ("ailun", "艾伦")
    kenny = ("kenny", "肯尼")
    aijing = ("aijing", "艾婧")
    aixia = ("aixia", "艾夏")
    aifei = ("aifei", "艾菲")


if __name__ == "__main__":
    resss = Constant()
    print(Constant().appKey)
    print(Constant().token)
    # res = SpeechArgs()
    # res.text = "你好"
    # print(res, res.get_dict())
