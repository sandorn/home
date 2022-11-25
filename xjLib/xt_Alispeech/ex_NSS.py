# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-24 21:36:44
FilePath     : /xjLib/xt_Alispeech/ex_NSS.py
LastEditTime : 2022-11-24 21:50:30
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading

import nls
from xt_Alispeech.conf import Constant
from xt_Alispeech.on_state import on_state_cls

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token


class NSS(on_state_cls):
    '''文字转语音  NlsSpeechSynthesizer'''
    result_dict = {}

    def __init__(self, file_name, tid=None, NssArgs=None):
        self.__th = threading.Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.args_dict = NssArgs
        self.__file_name = file_name

    def start(self):
        self.__f = open(self.__file_name, "wb")
        self.__th.start()

    def _on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def _on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def __thread_run(self):
        print("thread:{} start..".format(self.__id))

        tts = nls.NlsSpeechSynthesizer(
            token=_ACCESS_TOKEN,
            appkey=_ACCESS_APPKEY,
            long_tts=self.args_dict['long_tts'] or False,
            on_metainfo=self._on_metainfo,
            on_data=self._on_data,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
            callback_args=[self.__id],
        )

        print("{}: session start".format(self.__id))

        res = tts.start(
            text=self.args_dict['text'],
            voice=self.args_dict['voice'] or 'Aida',
            aformat=self.args_dict['aformat'] or 'wav',
            sample_rate=self.args_dict['sample_rate'] or 16000,
            volume=self.args_dict['volume'] or 50,
            speech_rate=self.args_dict['speech_rate'] or 0,
            pitch_rate=self.args_dict['pitch_rate'] or 0,
            wait_complete=self.args_dict['wait_complete'] or True,
            start_timeout=self.args_dict['start_timeout'] or 10,
            completed_timeout=self.args_dict['completed_timeout'] or 60,
            ex=self.args_dict['ex'] or {},
            # {'enable_subtitle': True},  #输出每个字在音频中的时间位置
        )
        print("{}: NSS done with result:{}".format(self.__id, res))


if __name__ == '__main__':
    _text_list = [
        '大壮正想去摘取花瓣，谁知阿丽和阿强突然内讧，阿丽拿去手枪向树干边的阿强射击，两声枪响，阿强直接倒入水中',
    ]

    from xt_Alispeech.conf import SpeechArgs
    t = SpeechArgs().get_dict()

    t['text'] = _text_list[0]

    class TTS(NSS):

        def _on_close(self, message, *args):
            print("on_close:{}".format(message))

    tack = TTS("1_tts.wav", 1, t)
    tack.start()
    '''
    def _on_close(self, message, *args):
        print("on_close:{}".format(message))

    TTS2 = NSS
    TTS2._on_close = _on_close

    tack2 = TTS2("2_tts.wav", 1, t)
    tack2.start()
    '''
