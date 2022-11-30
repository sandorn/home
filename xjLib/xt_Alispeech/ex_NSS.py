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
import os
from threading import Semaphore, Thread

import nls
from xt_Alispeech.conf import Constant, SpeechArgs
from xt_Alispeech.on_state import on_state_cls
from xt_String import str_split_limited_list
from xt_Time import get_10_timestamp

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token
sem = Semaphore(2)  # 限制线程并发数


class NSS(on_state_cls):
    '''文字转语音  NlsSpeechSynthesizer'''
    all_Thread = []  # 类属性或类变量,实例公用
    result_list = []  # 类属性或类变量,实例公用

    def __init__(self, text, tid=None, args_dict={}):
        self.__th = Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.args_dict = args_dict
        self.__text = text
        self.__file_name = str(self.__id) + '_' + str(get_10_timestamp()) + '_tts.' + self.args_dict['aformat']
        self.start()

    def start(self):
        self.__f = open(self.__file_name, "wb")  # #无文件则创建
        self.__th.start()
        self.all_Thread.append(self.__th)

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
            res, cls.result_list = cls.result_list, []
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
        self.result_list.append([self.__id, self.__data])
        return self.__data

    def _on_close(self, *args):
        self.__f.close()
        if not self.args_dict['savefile']: os.remove(self.__file_name)

    def __thread_run(self):
        with sem:
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


def NSS_TTS(_in_text: list, update_args: dict = {}):

    args_dict = SpeechArgs().get_dict()
    args_dict.update(update_args)

    if type(_in_text) == str: _in_text = str_split_limited_list(_in_text)

    if type(_in_text) in [tuple, list]:
        for index, text in enumerate(_in_text):
            NSS(text, tid=index + 1, args_dict=args_dict)

    result_list = NSS.wait_completed()
    return result_list


if __name__ == '__main__':
    _text = []

    res_list = NSS_TTS(_text, {'savefile': False})
    res_list.sort(key=lambda x: x[0])
    f = open('test.mp3', "wb")
    for item in res_list:
        f.write(item[1])
    f.close()
