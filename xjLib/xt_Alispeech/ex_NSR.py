# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-24 17:49:06
FilePath     : /xjLib/xt_Alispeech/ex_NSR.py
LastEditTime : 2022-11-28 17:23:18
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


class NSR(on_state_cls):
    '''语音转文字  NlsSpeechRecognizer'''
    all_Thread = []  # 类属性或类变量,实例公用
    result_dict = {}  # 类属性或类变量,实例公用

    def __init__(self, file_name, tid=None):
        self.__th = threading.Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.start(file_name)
        self.all_Thread.append(self.__th)

    def loadfile(self, filename):
        with open(filename, 'rb') as f:
            self.__data = f.read()

    def start(self, filename):
        self.loadfile(filename)
        self.__th.start()

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            _thread = self.all_Thread.pop()
            _thread.join()  # @单例无效

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            res, cls.result_dict = cls.result_dict, {}
            return res
        except Exception:
            return None

    def _on_completed(self, message, *args):
        self.result_dict[self.__id] = message

    def __thread_run(self):
        print('thread:{} start..'.format(self.__id))

        nsrr = nls.NlsSpeechRecognizer(
            token=_ACCESS_TOKEN,
            appkey=_ACCESS_APPKEY,
            on_start=self._on_start,
            on_result_changed=self._on_result_changed,
            on_completed=self._on_completed,
            on_error=self._on_error,
            on_close=self._on_close,
            callback_args=[self.__id],
        )

        print('{}: session start'.format(self.__id))

        res = nsrr.start(
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
            nsrr.send_audio(bytes(i))
            time.sleep(0.01)

        res = nsrr.stop()
        print('{}: NSR stopped:{}'.format(self.__id, res))


if __name__ == '__main__':

    _in_file_list = [
        'D:/UserData/xinjun/Downloads/alibabacloud-nls-python-sdk-1.0.0/tests/test1.pcm',
        'D:/UserData/xinjun/Downloads/alibabacloud-nls-python-sdk-1.0.0/tests/test1.wav',
        #'D:/UserData/xinjun/Downloads/alibabacloud-nls-python-sdk-1.0.0/tests/tts_test.wav',
    ]

    for index, file in enumerate(_in_file_list):
        tack = NSR(file, index + 1)
    res = tack.wait_completed()  # result_dict

    res_list, dictMerged = handle_ex_nsx_result(res)
    print(dictMerged)
    print(res_list)
