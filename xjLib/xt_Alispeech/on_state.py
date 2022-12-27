# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-27 18:59:04
FilePath     : /xjLib/xt_Alispeech/on_state.py
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
        print(f"_on_sentence_begin message=>{message}: args=>{args}")

    def _on_sentence_end(self, message, *args):
        print(f"_on_sentence_end message=>{message}: args=>{args}")

    def _on_start(self, message, *args):
        print(f"_on_start message=>{message}: args=>{args}")

    def _on_error(self, message, *args):
        print(f"_on_error message=>{message}: args=>{args}")

    def _on_result_changed(self, message, *args):
        print(f"_on_chg message=>{message}: args=>{args}")

    def _on_metainfo(self, message, *args):
        print(f"_on_metainfo message=>{message}: args=>{args}")

    def _on_data(self, data, *args):
        print(f"_on_data data=>{data}: args=>{args}")

    def _on_completed(self, message, *args):
        '''早于_on_close'''
        print(f"_on_completed message=>{message}: args=>{args}")

    def _on_close(self, *args):
        '''最后执行'''
        print(f"_on_close: args=>{args}")
