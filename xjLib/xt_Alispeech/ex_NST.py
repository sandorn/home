# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-24 17:41:59
FilePath     : /xjLib/xt_Alispeech/ex_NST.py
LastEditTime : 2022-11-24 20:47:47
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading
import time

import nls
from xt_Alispeech.conf import Constant, handle_ex_nsx_result
from xt_Alispeech.on_state import on_state_cls

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token


class NST(on_state_cls):
    '''语音转文字  NlsSpeechTranscriber'''
    result_dict = {}

    def __init__(self, file_name, tid=None):
        self.__th = threading.Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.start(file_name)

    def loadfile(self, filename):
        with open(filename, "rb") as f:
            self.__data = f.read()

    def start(self, filename):
        self.loadfile(filename)
        self.__th.start()
        self.__th.join()

    def _on_sentence_end(self, message, *args):
        self.result_dict[self.__id] = message

    def __thread_run(self):

        print("thread:{} start..".format(self.__id))

        nstr = nls.NlsSpeechTranscriber(
            token=_ACCESS_TOKEN,
            appkey=_ACCESS_APPKEY,
            on_sentence_begin=self._on_sentence_begin,
            on_sentence_end=self._on_sentence_end,
            on_start=self._on_start,
            on_result_changed=self._on_result_changed,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
            callback_args=[self.__id],
        )

        print("{}: session start".format(self.__id))

        res = nstr.start(
            aformat="pcm",
            enable_intermediate_result=True,
            enable_punctuation_prediction=True,
            enable_inverse_text_normalization=True,
            sample_rate=16000,
            ch=1,
            timeout=10,
            ping_interval=8,
            ping_timeout=None,
            ex=None,
        )

        self.__slices = zip(*(iter(self.__data), ) * 640)
        for i in self.__slices:
            nstr.send_audio(bytes(i))
            time.sleep(0.01)

        # &nstr.ctrl(ex={"test": "nweargs"})

        res = nstr.stop()
        print("{}: NST stopped:{}".format(self.__id, res))


if __name__ == '__main__':

    _in_file_list = [
        'alibabacloud-nls-python-sdk-1.0.0/tests/test1.pcm',
        'alibabacloud-nls-python-sdk-1.0.0/tests/test1.wav',
        #'alibabacloud-nls-python-sdk-1.0.0/tests/tts_test.wav',
    ]

    for index, file in enumerate(_in_file_list):
        tack = NST(file, index + 1)
    res = tack.result_dict

    res_list, dictMerged = handle_ex_nsx_result(res)
    print(dictMerged)
    print(res_list)
