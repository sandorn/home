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
from xt_Alispeech.conf import (
    Constant,
    SpeechArgs,
    get_voice_data,
    merge_sound_file,
    save_sound_file,
)
from xt_Alispeech.on_state import on_state_cls
from xt_String import str_split_limited_list
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
            print("{}: thread start..".format(self.__id))

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

            print("{}: session start".format(self.__id))

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
            print('{}: NSS stopped.'.format(self.__id))


def TODO_TTS(_in_text, renovate_args: dict = {}, readonly=False, merge=False):
    # $处理参数
    args = SpeechArgs().get_dict()
    args.update(renovate_args)

    if isinstance(_in_text, str):  # $整段文字要合并
        _in_text = str_split_limited_list(_in_text)
        merge = True
    assert isinstance(_in_text, list)

    # $运行主程序
    [NSS(text, tid=index + 1, args=args) for index, text in enumerate(_in_text)]
    datalist = NSS.wait_completed()

    # $处理结果
    assert isinstance(datalist, list)
    datalist.sort(key=lambda x: x[0])

    if readonly: return get_voice_data(datalist)
    if not merge: return save_sound_file(datalist)
    if merge: merge_sound_file(datalist, args)


if __name__ == '__main__':

    _text = '''
    财务科目排查要点

一、总公司及分支公司排查要点
（一）应收应付类科目检查及清理
1.业务类应收科目
对“应收保费”科目，应按照保单号、应收日期、宽限期截止日、保单状态逐笔分析；对“垫交保费”和“保户质押贷款”科目应按照保单号、垫交日期或质押贷款日期、保单状态逐笔进行分析，保证财务与业务数据核对相符。
2.业务类预收和应付科目
各分公司对“预收保费”科目应按照投保单号、预收账龄逐笔核对，保证业务与财务数据相符。年末余额主要为暂收客户的尚未签单或生效的保费，或者其他保全加费等。对于长期挂账的预收保费应与业务部门进行确认，对于预收保费明细账户余额异常的，应查明原因后进行账务处理，保证数据正确。对“应付赔付款”明细科目余额应逐项核对，与业务部门进行数据核实，确认数据是否合理，保证财务数据与业务数据核对一致。对于存在的差异或者长期挂账的应付数据，应及时查找原因并上报总公司审核后进行账务处理。
3.清理“应付佣金”和“应付手续费”
对“应付佣金”和“应付手续费”科目进行清理，年末余额应为当年据实发生的应付未付的佣金和手续费。对于长期挂账的数据应查找原因，如果属于确实不再支付的项目应进行清理，在上报总公司审核后进行账务处理。
4.核实“应付职工薪酬”
财务部门应与人力资源部对“应付职工薪酬”各明细项目进行核实确认，年末余额应为经人力资源部确认的据实发生的各项应付明细余额，如有不符，应查明原因并及时处理。对于已经计提但确实不再需要支付的数据，经人力资源部审核后进行相应的账务处理。
5.核对投资类应收科目
对“应收利息”及“应收股利”科目进行核实，对账户余额分类整理、及时清理，保证应收利息及股利数据的真实和准确。对投资业务的应收款和预付款进行逐项核实，结合其基础资产风险情况、担保及信用增级情况和诉讼判决执行情况等综合判断是否涉及减值损失，并根据《君康人寿保险股份有限公司应收应付款项管理办法（2018修订版）》要求计提减值准备。
6.核对费用类应收应付科目
对于费用应收及预付项目，应逐项核实是否符合费用计提条件，不得少计、漏记费用。对于长期挂账的应收应付项目，应核实挂账原因，并根据公司相关制度进行处理。
7.核对再保类应收应付
对于再保业务形成的应收应付款项，对已出账单部分，应与账单金额充分核对，保证余额与账单金额一致；对未出账单部分，应以产品精算部与再保公司达成一致的预估方法入账。
8.梳理或有事项
公司法务部应梳理公司存在的未决诉讼，并在12月28日前提交财务管理部（若期后诉讼情况发生变动的，应及时更新）。符合负债确认条件的，应按照会计准则要求确认对应负债。'''

    out_file = TODO_TTS(_text, merge=True)
    print(out_file)
