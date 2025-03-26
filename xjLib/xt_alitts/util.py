# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-03-25 10:08:27
FilePath     : /CODE/xjLib/xt_alitts/util.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import shutil

from pydub import AudioSegment
from xt_file import get_desktop
from xt_time import get_timestamp


def handle_result(res):
    """处理 ex_NSR/ex_NST 结果"""
    dict_merged = {}
    res_list = []

    for key, values in res.items():
        _dict = eval(values)
        dict_merged[key] = {**_dict["header"], **_dict["payload"]}
        res_list.append((key, dict_merged[key]["result"]))

    return res_list, dict_merged


def get_voice_data(voice_data_list):
    """情形1-不保存文件,返回音频数据,用于朗读"""
    return [
        [index, open(item[1], "rb").read()]
        for index, item in enumerate(voice_data_list)
    ]


def save_sound_file(voice_data_list, path=None):
    """情形2-保存音频文件指定到位置或桌面
    Args:
        voice_data_list (list): 音频数据列表
        path (str, optional): 保存路径，默认为桌面

    Returns:
        list: 更新后的音频数据列表
    """
    path = path or get_desktop()

    for index, item in enumerate(voice_data_list):
        basename = os.path.basename(item[1])
        dest_path = os.path.join(path, basename)
        shutil.move(item[1], dest_path)
        voice_data_list[index][1] = dest_path

    return voice_data_list


def merge_sound_file(voice_data_list, args, path=None):
    """情形3-合并音频,删除过程文件
    Args:
        voice_data_list (list): 音频数据列表
        args (dict): 音频参数
        path (str, optional): 保存路径，默认为桌面
    Returns:
        list: 合并后的音频文件列表
    """
    path = path or get_desktop()

    # 将声音列表初始化为AudioSegment格式
    sound_list = [
        AudioSegment.from_file(item[1], format=args["aformat"])
        for item in voice_data_list
    ]

    # 使用sum函数来快速完成声音文件相加，无需循环
    sum_sound = sum(sound_list)

    # 保存音频文件
    fname = f"{path}/{get_timestamp()}_{args['voice']}_tts.{args['aformat']}"
    sum_sound.export(fname, format=args["aformat"])  # 保存文件

    return [[1, fname]]


class AudioProcessor:
    def __init__(self, voice_data_list, path=None):
        self.voice_data_list = voice_data_list
        self.path = path or get_desktop()

    def handle_result(self, res):
        """处理 ex_NSR/ex_NST 结果"""
        dict_merged = {}
        res_list = []

        for key, values in res.items():
            _dict = eval(values)  # 注意：eval使用需谨慎
            dict_merged[key] = {**_dict["header"], **_dict["payload"]}
            res_list.append((key, dict_merged[key]["result"]))

        return res_list, dict_merged

    def get_voice_data(self):
        """情形1-不保存文件,返回音频数据,用于朗读"""
        return [
            [index, self._read_file(item[1])]
            for index, item in enumerate(self.voice_data_list)
        ]

    def _read_file(self, file_path):
        """读取文件内容"""
        with open(file_path, "rb") as file:
            return file.read()

    def save_sound_file(self):
        """情形2-保存音频文件指定到位置或桌面
        Returns:
            list: 更新后的音频数据列表
        """
        for index, item in enumerate(self.voice_data_list):
            dest_path = self._move_file(
                item[1], os.path.join(self.path, os.path.basename(item[1]))
            )
            self.voice_data_list[index][1] = dest_path

        return self.voice_data_list

    def _move_file(self, src_path, dest_path):
        """移动文件到指定路径"""
        shutil.move(src_path, dest_path)
        return dest_path

    def merge_sound_file(self, args):
        """情形3-合并音频,删除过程文件
        Args:
            args (dict): 音频参数
        Returns:
            list: 合并后的音频文件列表
        """
        sound_list = self._load_audio_segments()
        sum_sound = sum(sound_list)
        fname = self._generate_filename(args)
        sum_sound.export(fname, format=args["aformat"])  # 保存文件

        return [[1, fname]]

    def _load_audio_segments(self):
        """加载音频段"""
        return [
            AudioSegment.from_file(item[1], format=item[1].split(".")[-1])
            for item in self.voice_data_list
        ]

    def _generate_filename(self, args):
        """生成音频文件名"""
        return f"{self.path}/{get_timestamp()}_{args['voice']}_tts.{args['aformat']}"


# 使用示例
# voice_data_list = [[1, 'path/to/audio1.mp3'], [2, 'path/to/audio2.mp3']]
# processor = AudioProcessor(voice_data_list)
# processor.save_sound_file()
# merged_files = processor.merge_sound_file({'voice': 'example', 'aformat': 'mp3'})
