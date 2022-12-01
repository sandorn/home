# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-24 20:43:33
FilePath     : /xjLib/xt_Alispeech/on_state.py
LastEditTime : 2022-12-01 18:52:51
Github       : https://github.com/sandorn/home
==============================================================
'''


class on_state_cls:

    def _on_sentence_begin(self, message, *args):
        ...

    def _on_sentence_end(self, message, *args):
        ...

    def _on_start(self, message, *args):
        ...

    def _on_error(self, message, *args):
        ...

    def _on_close(self, *args):
        ...

    def _on_result_changed(self, message, *args):
        ...

    def _on_completed(self, message, *args):
        ...

    def _on_metainfo(self, message, *args):
        ...

    def _on_data(self, data, *args):
        ...


class on_state_primitive:

    def _on_sentence_begin(self, message, *args):
        print("_on_sentence_begin message=>{}: args=>{}".format(message, args))

    def _on_sentence_end(self, message, *args):
        print("_on_sentence_end message=>{}: args=>{}".format(message, args))

    def _on_start(self, message, *args):
        print("_on_start message=>{}: args=>{}".format(message, args))

    def _on_error(self, message, *args):
        print("_on_error message=>{}: args=>{}".format(message, args))

    def _on_result_changed(self, message, *args):
        print("_on_chg message=>{}: args=>{}".format(message, args))

    def _on_metainfo(self, message, *args):
        print("_on_metainfo message=>{}: args=>{}".format(message, args))

    def _on_data(self, data, *args):
        print("_on_data data=>{}: args=>{}".format(data, args))

    def _on_completed(self, message, *args):
        '''早于_on_close'''
        print("_on_completed message=>{}: args=>{}".format(message, args))

    def _on_close(self, *args):
        '''最后执行'''
        print("_on_close: args=>{}".format(args))
