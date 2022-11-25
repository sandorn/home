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
LastEditTime : 2022-11-24 20:43:35
Github       : https://github.com/sandorn/home
==============================================================
'''


class on_state_cls:

    def _on_sentence_begin(self, message, *args):
        pass

    def _on_sentence_end(self, message, *args):
        pass

    def _on_start(self, message, *args):
        pass

    def _on_error(self, message, *args):
        pass

    def _on_close(self, *args):
        pass

    def _on_result_changed(self, message, *args):
        pass

    def _on_completed(self, message, *args):
        pass

    def _on_metainfo(self, message, *args):
        pass

    def _on_data(self, data, *args):
        pass


class on_state_primitive:

    def _on_sentence_begin(self, message, *args):
        print("_on_sentence_begin:{}".format(message))

    def _on_sentence_end(self, message, *args):
        print("_on_sentence_end:{}".format(message))

    def _on_start(self, message, *args):
        print("_on_start:{}".format(message))

    def _on_error(self, message, *args):
        print("_on_error args=>{}".format(args))

    def _on_close(self, *args):
        print("_on_close: args=>{}".format(args))

    def _on_result_changed(self, message, *args):
        print("_on_chg:{}".format(message))

    def _on_completed(self, message, *args):
        print("_on_completed:args=>{} message=>{}".format(args, message))

    def _on_metainfo(self, message, *args):
        print("_on_metainfo message=>{}".format(message))

    def _on_data(self, data, *args):
        print("_on_data data=>{}".format(data))
