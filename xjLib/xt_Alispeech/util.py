# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-10-18 11:44:46
FilePath     : /CODE/xjLib/xt_Alispeech/util.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
import shutil

from pydub import AudioSegment
from xt_File import get_desktop
from xt_Time import get_10_timestamp


def handle_result(res):
    '''处理 ex_NSR/ex_NST 结果'''
    dict_merged = {}
    res_list = []

    for key, values in res.items():
        _dict = eval(values)
        dict_merged[key] = {**_dict['header'], **_dict['payload']}
        res_list.append((key, dict_merged[key]['result']))

    return res_list, dict_merged


def get_voice_data(voice_data_list):
    '''情形1-不保存文件,返回音频数据,用于朗读'''
    return [[index, open(item[1], 'rb').read()]
            for index, item in enumerate(voice_data_list)]


def save_sound_file(voice_data_list, path=None):
    '''情形2-保存音频文件指定到位置或桌面
    Args:
        voice_data_list (list): 音频数据列表
        path (str, optional): 保存路径，默认为桌面

    Returns:
        list: 更新后的音频数据列表
    '''
    if path is None: path = get_desktop()

    for index, item in enumerate(voice_data_list):
        basename = os.path.basename(item[1])
        dest_path = os.path.join(path, basename)
        shutil.move(item[1], dest_path)
        voice_data_list[index][1] = dest_path
        # $[[1, 'D:\\path\\1.mp3'], [2, 'D:\\path\\2.mp3'],]

    return voice_data_list


def merge_sound_file(voice_data_list, args, path=None):
    '''情形3-合并音频,删除过程文件
    Args:
        voice_data_list (list): 音频数据列表
        args (dict): 音频参数
        path (str, optional): 保存路径，默认为桌面
    Returns:
        list: 合并后的音频文件列表
    '''
    if path is None: path = get_desktop()
    # 将声音列表初始化为AudioSegment格式
    sound_list = [
        AudioSegment.from_file(item[1], format=args['aformat'])
        for item in voice_data_list
    ]
    # [[item[0], AudioSegment.from_file(item[1], format=format)] for item in voice_data_list]

    # 使用sum函数来快速完成声音文件相加，无需循环
    SumSound = sum(sound_list)

    # $保存音频文件
    __fname = f"{path}\\{get_10_timestamp()}_{args['voice']}_tts.{args['aformat']}"
    SumSound.export(__fname, format=args['aformat'])  # 保存文件

    # $[[1, 'D:\\Desktop\\1.mp3'],]
    return [[1, __fname]]
