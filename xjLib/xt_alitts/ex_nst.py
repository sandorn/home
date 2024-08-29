# !/usr/bin/env python
"""
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
"""

from threading import Semaphore, Thread

from nls import NlsSpeechTranscriber
from xt_alitts.cfg import Constant
from xt_alitts.state import on_state_cls
from xt_alitts.util import handle_result

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token
Sem = Semaphore(2)  # 限制线程并发数


class NST(on_state_cls):
    """语音转文字  NlsSpeechTranscriber"""

    all_Thread = []
    result_dict = {}

    def __init__(self, file_name, tid=None):
        self.__th = Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.__file_name = file_name
        self.start()

    def start(self):
        self.__data = open(self.__file_name, "rb").read()
        self.__th.start()
        self.all_Thread.append(self.__th)

    @classmethod
    def stop_all(cls):
        """停止线程池， 所有线程停止工作"""
        while cls.all_Thread:
            _thread = cls.all_Thread.pop()
            _thread.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""

        try:
            cls.stop_all()
            res, cls.result_dict = cls.result_dict, {}
            return handle_result(res)
        except Exception:
            return {}

    def _on_sentence_end(self, message, *args):
        """相当于:_on_completed"""
        self.result_dict[str(self.__id)] = message
        return message

    def __thread_run(self):
        with Sem:
            print(f"{self.__id}: thread start..")

            _NST_ = NlsSpeechTranscriber(
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

            print(f"{self.__id}: session start")

            _NST_.start(
                aformat="pcm",
                enable_intermediate_result=True,
                enable_punctuation_prediction=True,
                enable_inverse_text_normalization=True,
                sample_rate=16000,
                ch=1,
                timeout=10,
                ping_interval=8,
                ping_timeout=None,
                ex={},
            )

            slices = [self.__data[i : i + 640] for i in range(0, len(self.__data), 640)]
            for __s in slices:
                _NST_.send_audio(bytes(__s))

            _NST_.stop()
            print(f"{self.__id}: NST stopped.")


def execute_nst(_in_file_list):
    if isinstance(_in_file_list, str):
        _ = [NST(_in_file_list, 1)]
    elif isinstance(_in_file_list, list):
        _ = [NST(file, index + 1) for index, file in enumerate(_in_file_list)]
    else:
        raise TypeError(f"TODO_NST: {_in_file_list} is not a file | file list.")

    res_list, dictMerged = NST.wait_completed()
    return res_list, dictMerged


if __name__ == "__main__":
    _in_file_list = ["D:/11.wav"]
    _in_file_list = "D:/11.wav"

    res_list, dictMerged = execute_nst(_in_file_list)

    print(dictMerged)
    print(res_list)
