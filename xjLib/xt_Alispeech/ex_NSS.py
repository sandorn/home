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
from xt_Alispeech.conf import Constant, SpeechArgs
from xt_Alispeech.on_state import on_state_cls
from xt_Time import get_10_timestamp

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token
import os


class NSS(on_state_cls):
    '''文字转语音  NlsSpeechSynthesizer'''
    all_Thread = []  # 类属性或类变量,实例公用
    result_dict = {}  # 类属性或类变量,实例公用

    def __init__(self, text, tid=None, args_dict={}):
        self._th = threading.Thread(target=self.__thread_run)
        self.__id = tid or id(self._th)
        self.args_dict = args_dict
        self.__text = text
        self.__file_name = str(self.__id) + '_' + str(get_10_timestamp()) + '_tts.' + self.args_dict['aformat']
        self.start()
        self.all_Thread.append(self._th)

    def start(self):
        self.__f = open(self.__file_name, "wb")  # #无文件则创建
        self._th.start()

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            _thread = self.all_Thread.pop()
            _thread.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_dict = cls.result_dict, {}
            return res
        except Exception:
            return None

    def _on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def _on_completed(self, message, *args):
        with open(self.__file_name, "rb+") as f:
            self.__data = f.read()

        self.result_dict[self.__id] = self.__data
        return self.__data

    def _on_close(self, *args):
        self.__f.close()
        if not self.args_dict['savefile']: os.remove(self.__file_name)

    def __thread_run(self):
        print("thread:{} start..".format(self.__id))

        tts = nls.NlsSpeechSynthesizer(
            token=_ACCESS_TOKEN,
            appkey=_ACCESS_APPKEY,
            long_tts=self.args_dict.get('long_tts', False),
            on_metainfo=self._on_metainfo,
            on_data=self._on_data,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
            callback_args=[self.__id],
        )

        print("{}: session start".format(self.__id))

        res = tts.start(
            text=self.__text,
            voice=self.args_dict.get('voice', 'Aida'),
            aformat=self.args_dict.get('aformat', 'mp3'),
            sample_rate=self.args_dict.get('sample_rate', 16000),
            volume=self.args_dict.get('volume', 50),
            speech_rate=self.args_dict.get('speech_rate', 0),
            pitch_rate=self.args_dict.get('pitch_rate', 0),
            wait_complete=self.args_dict.get('wait_complete', True),
            start_timeout=self.args_dict.get('start_timeout', 10),
            completed_timeout=self.args_dict.get('completed_timeout', 60),
            ex=self.args_dict.get('ex', {}),
            # {'enable_subtitle': True},  #输出每个字在音频中的时间位置
        )

        print("{}: NSS done with result:{}".format(self.__id, res))


def NSS_TTS(_in_text: list, update_args_dict: dict = {}):

    args_dict = SpeechArgs().get_dict()
    args_dict.update(update_args_dict)

    if type(_in_text) in [tuple, list]:
        for index, text in enumerate(_in_text):
            task = NSS(text, tid=index + 1, args_dict=args_dict)
    else:
        task = NSS(_in_text, tid=1, args_dict=args_dict)

    result_dict = task.wait_completed()
    return result_dict


if __name__ == '__main__':
    _text_list = [
        '2022世界杯小组赛C组第二轮，阿根廷2-0力克墨西哥，重新掌握出线主动权。第64分钟，梅西世界波破门，打入个人世界杯第8个进球，进球数追平马拉多纳。',
        '第87分钟，恩索·费尔南德斯锁定胜局！目前，波兰积4分，阿根廷和沙特同积3分，阿根廷以净胜球优势排名第二，墨西哥积1分。',
    ]

    res = NSS_TTS(_text_list)
    print(7777777777777777, '主程序结束', len(res))
    for k, v in res.items():
        print(k, type(k), len(v))

    ##########################################################
    '''
    @classmethod
    def my_func(self, message, *args):
        print("my_func ||||||||{}|||||||||:{}".format(message, args))
        print('my_func XXXXXXXXXXXXXXXXXXXXXXXX', self._th)

    _temp_args['text'] = _text_list[0]
    res = NSS_TTS(1, _text_list[0], 'name_', _temp_args, {'_on_completed': my_func})


    class TTS(NSS):
        def _on_close(self, *args):
            print("on_close:{}".format(args))

    tack = TTS("1_tts.wav", 1, t)
    tack.start()
    def _on_close(self, *args):
        print("on_close:{}".format(args))


    TTS2 = NSS
    TTS2._on_close = _on_close

    tack2 = TTS2("2_tts.wav", 1, t)
    tack2.start()
    '''
