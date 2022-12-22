# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-24 21:36:44
LastEditTime : 2022-12-03 16:33:15
FilePath     : /xjLib/xt_Alispeech/ex_NSS.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
from threading import Semaphore, Thread

import nls
from PyQt5.QtCore import QThread
from xt_Alispeech.cfg import Constant, SpeechArgs
from xt_Alispeech.on_state import on_state_cls
from xt_Alispeech.util import get_voice_data, merge_sound_file, save_sound_file
from xt_String import str2list
from xt_Time import get_10_timestamp

_ACCESS_APPKEY = Constant().appKey
_ACCESS_TOKEN = Constant().token
Sem = Semaphore(2)  # 限制线程并发数


class NSS(on_state_cls):
    '''文字转语音  NlsSpeechSynthesizer'''
    all_Thread = []  # 类属性或类变量,实例公用
    data_list = []  # 类属性或类变量,实例公用

    def __init__(self, text, tid=None, args={}):
        self.__th = Thread(target=self.__thread_run)
        self.__id = tid or id(self.__th)
        self.args = args
        self.__text = text
        __fname = f"{self.__id}_{get_10_timestamp()}_{self.args['voice']}_tts.{ self.args['aformat']}"
        self.__file_name = f"{os.getenv('TMP')}\\{__fname}"

        self.start()

    def start(self):
        self.__f = open(self.__file_name, "wb")  # #无文件则创建
        self.__th.start()
        self.all_Thread.append(self.__th)

    def stop_all(self):
        """停止线程池， 所有线程停止工作"""
        for _ in range(len(self.all_Thread)):
            _thread = self.all_Thread.pop(0)
            _thread.join()

    @classmethod
    def wait_completed(cls):
        """等待全部线程结束，返回结果"""
        try:
            cls.stop_all(cls)  # !向stop_all函数传入self 或cls ,三处保持一致
            datalist, cls.data_list = cls.data_list, []
            return datalist
        except Exception:
            return []

    def _on_data(self, data, *args):
        try:
            self.__f.write(data)
            QThread.msleep(100)
        except Exception as e:
            print("write data failed:", e)

    def _on_completed(self, message, *args):
        res = [self.__id, self.__file_name]
        self.data_list.append(res)
        return res

    def _on_close(self, *args):
        self.__f.close()

    def __thread_run(self):
        with Sem:
            print("thread {}: start..".format(self.__id))

            _NSS_ = nls.NlsSpeechSynthesizer(
                token=_ACCESS_TOKEN,
                appkey=_ACCESS_APPKEY,
                long_tts=self.args.get('long_tts', False),
                on_metainfo=self._on_metainfo,
                on_data=self._on_data,
                on_completed=self._on_completed,
                on_error=self._on_error,
                on_close=self._on_close,
                callback_args=[self.__id],
            )

            _NSS_.start(
                text=self.__text,
                voice=self.args.get('voice', 'Aida'),
                aformat=self.args.get('aformat', 'mp3'),
                sample_rate=self.args.get('sample_rate', 16000),
                volume=self.args.get('volume', 50),
                speech_rate=self.args.get('speech_rate', 0),
                pitch_rate=self.args.get('pitch_rate', 0),
                wait_complete=self.args.get('wait_complete', True),
                start_timeout=self.args.get('start_timeout', 10),
                completed_timeout=self.args.get('completed_timeout', 60),
                ex=self.args.get('ex', {}),
                # {'enable_subtitle': True},  #输出每个字在音频中的时间位置
            )

            QThread.msleep(100)
            print('thread {}: NSS stopped.'.format(self.__id))


def TODO_TTS(_in_text, renovate_args: dict = {}, readonly=False, merge=False):
    # $处理参数
    args = SpeechArgs().get_dict()
    args.update(renovate_args)

    if isinstance(_in_text, str):  # $整段文字要合并
        _in_text = str2list(_in_text)
        merge = True
    assert isinstance(_in_text, list)

    # $运行主程序
    [NSS(text, tid=index + 1, args=args) for index, text in enumerate(_in_text)]
    datalist = NSS.wait_completed()

    # $处理结果
    assert isinstance(datalist, list)
    datalist.sort(key=lambda x: x[0])

    if readonly: return get_voice_data(datalist)
    if merge: return merge_sound_file(datalist, args)
    else: return save_sound_file(datalist)


if __name__ == '__main__':

    _text = '''
立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年
“青年强，则国家强。当代中国青年生逢其时，施展才干的舞台无比广阔，实现梦想的前景无比光明。”习近平总书记在党的二十大报告中勉励广大青年坚定不移听党话、跟党走，怀抱梦想又脚踏实地，敢想敢为又善作善成，立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年，让青春在全面建设社会主义现代化国家的火热实践中绽放绚丽之花。
未来属于青年，希望寄予青年。认真学习贯彻党的二十大精神，广大青年纷纷表示，一定牢记习近平总书记嘱托，坚定理想信念，筑牢精神之基，厚植爱国情怀，矢志不渝跟党走，以实现中华民族伟大复兴为己任，增强做中国人的志气、骨气、底气，不负时代，不负韶华，不负党和人民的殷切期望。
'''

    out_file = TODO_TTS(_text, {'aformat': 'wav'}, readonly=True)

    from PyQt5.QtCore import QThread
    from xt_Alispeech.Play import qthread_play, thread_play

    for oufile in out_file:
        task = qthread_play(oufile[1])
        task.join()
        # task2 = thread_play(oufile[1])
        # QThread.msleep(10000)
        # task2.stop()
