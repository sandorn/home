# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 16:57:09
#FilePath     : /xjLib/xt_Alispeech/conf.py
#LastEditTime : 2020-07-22 13:27:36
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import os
import shutil

from pydub import AudioSegment
from xt_File import get_desktop
from xt_Time import get_10_timestamp


def handle_ex_nsx_result(res):
    '''处理 ex_NSR ex_NST 结果'''
    dictMerged = {}
    res_list = []
    for key, values in res.items():
        _dict = eval(values)

        dictMerged[key] = dict(_dict['header'], **_dict['payload'])
        res_list.append((key, dictMerged[key]['result']))
    return (res_list, dictMerged)


def get_voice_data(voice_file_list):
    '''情形1-不保存文件,返回音频数据,用于朗读'''
    for index, item in enumerate(voice_file_list):
        with open(item[1], 'rb') as f:
            __data = f.read()
        os.remove(item[1])
        voice_file_list[index][1] = __data

    # $[[1, b'xxxx'], [2, b'xxxx'], [3, b'xxxx'],]
    return voice_file_list


def save_sound_file(voice_file_list, path=None):
    '''情形2-保存音频文件指定到位置或桌面'''
    if path is None: path = get_desktop() or ''
    for index, item in enumerate(voice_file_list):
        shutil.move(item[1], path)
        voice_file_list[index][1] = path + "\\" + item[1].split("\\")[-1]

        # $[[1, 'D:\\path\\1.mp3'], [2, 'D:\\path\\2.mp3'], [3, 'D:\\path\\3.mp3'],]
    return voice_file_list


def merge_sound_file(voice_file_list, args, path=None):
    '''情形3-合并音频,删除过程文件'''
    if path is None: path = get_desktop() or ''
    sound_list = [[item[0], AudioSegment.from_file(item[1], format=args['aformat']), os.remove(item[1])] for item in voice_file_list]

    SumSound: AudioSegment = sound_list.pop(0)[1]  # 第一个文件
    for item in sound_list:
        SumSound += item[1]  # 把声音文件相加

    # $保存音频文件
    __fname = f"{path}\\{get_10_timestamp()}_{args['voice']}_tts.{args['aformat']}"
    SumSound.export(__fname, format=args['aformat'])  # 保存文件
    voice_file_list = [[1, __fname]]

    # $[[1, 'D:\\Desktop\\1.mp3'],]
    return voice_file_list


VIOCE = [
    ('知米_多情感', 'zhimi_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知燕_多情感', 'zhiyan_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知贝_多情感', 'zhibei_emo', '多种情感童声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('知甜_多情感', 'zhitian_emo', '多种情感女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小云', 'xiaoyun', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
    ('小刚', 'xiaogang', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '否', '否', 'lite版'),
    ('若兮', 'ruoxi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思琪', 'siqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
    ('思佳', 'sijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思诚', 'sicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K/24K', '是', '否', '标准版'),
    ('艾琪', 'aiqi', '温柔女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾佳', 'aijia', '标准女声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾诚', 'aicheng', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾达', 'aida', '标准男声', '通用场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('宁儿', 'ninger', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('瑞琳', 'ruilin', '标准女声', '通用场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思悦', 'siyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('艾雅', 'aiya', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾夏', 'aixia', '亲和女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾美', 'aimei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾雨', 'aiyu', '自然女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾悦', 'aiyue', '温柔女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾婧', 'aijing', '严厉女声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小美', 'xiaomei', '甜美女声', '客服场景', '中文及中英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('艾娜', 'aina', '浙普女声', '客服场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('伊娜', 'yina', '浙普女声', '客服场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('思婧', 'sijing', '严厉女声', '客服场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
    ('思彤', 'sitong', '儿童音', '童声场景', '纯中文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('小北', 'xiaobei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K/24K', '是', '否', '标准版'),
    ('艾彤', 'aitong', '儿童音', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('艾薇', 'aiwei', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('艾宝', 'aibao', '萝莉女声', '童声场景', '纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('Harry', 'harry', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Abby', 'abby', '美音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('Andy', 'andy', '美音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Eric', 'eric', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Emily', 'emily', '英音女声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Luna', 'luna', '英音女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('Luca', 'luca', '英音男声', '英文场景', '英文场景', '8K/16K', '否', '否', '标准版'),
    ('Wendy', 'wendy', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('William', 'william', '英音男声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('Olivia', 'olivia', '英音女声', '英文场景', '英文场景', '8K/16K/24K', '否', '否', '标准版'),
    ('姗姗', 'shanshan', '粤语女声', '方言场景', '标准粤文及粤英文混合场景', '8K/16K/24K', '否', '否', '标准版'),
    ('小玥', 'chuangirl', '四川话女声', '方言场景', '中文及中英文混合场景', '8K/16K', '否', '否', '标准版'),
    ('Lydia', 'lydia', '英中双语女声', '英文场景', '英文及英中文混合场景', '8K/16K', '是', '否', '标准版'),
    ('艾硕', 'aishuo', '自然男声', '客服场景', '中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('青青', 'qingqing', '中国台湾话女声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
    ('翠姐', 'cuijie', '东北话女声', '方言场景', '中文场景', '8K/16K', '否', '是', '标准版'),
    ('小泽', 'xiaoze', '湖南重口音男声', '方言场景', '中文场景', '8K/16K', '否', '否', '标准版'),
    ('智香', 'tomoka', '日语女声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
    ('智也', 'tomoya', '日语男声', '多语种场景', '日文场景', '8K/16K', '是', '否', '标准版'),
    ('Annie', 'annie', '美语女声', '英文场景', '英文场景', '8K/16K', '是', '否', '标准版'),
    ('佳佳', 'jiajia', '粤语女声', '方言场景', '标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('Indah', 'indah', '印尼语女声', '多语种场景', '纯印尼语场景', '8K/16K', '否', '否', '标准版'),
    ('桃子', 'taozi', '粤语女声', '方言场景', '支持标准粤文（简体）及粤英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('柜姐', 'guijie', '亲切女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Stella', 'stella', '知性女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Stanley', 'stanley', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Kenny', 'kenny', '沉稳男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Rosa', 'rosa', '自然女声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('Farah', 'farah', '马来语女声', '多语种场景', '仅支持纯马来语场景', '8K/16K', '否', '否', '标准版'),
    ('马树', 'mashu', '儿童剧男声', '通用场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '标准版'),
    ('小仙', 'xiaoxian', '亲切女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('悦儿', 'yuer', '儿童剧女声', '通用场景', '仅支持纯中文场景', '8K/16K', '是', '否', '标准版'),
    ('猫小美', 'maoxiaomei', '活力女声', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('知飞', 'zhifei', '激昂解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
    ('知伦', 'zhilun', '悬疑解说', '超高清场景', '支持中文及中英文混合场景', '8K/16K', '是', '否', '精品版'),
    ('艾飞', 'aifei', '激昂解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('亚群', 'yaqun', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('巧薇', 'qiaowei', '卖场广播', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('大虎', 'dahu', '东北话男声', '方言场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('ava', 'ava', '美语女声', '英文场景', '仅支持纯英文场景', '8K/16K', '是', '否', '标准版'),
    ('艾伦', 'ailun', '悬疑解说', '直播场景', '支持中文及中英文混合场景', '8K/16K', '是', '是', '标准版'),
    ('杰力豆', 'jielidou', '治愈童声', '童声场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('老铁', 'laotie', '东北老铁', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('老妹', 'laomei', '吆喝女声', '直播场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('艾侃', 'aikan', '天津话男声', '方言场景', '仅支持纯中文场景', '8K/16K', '是', '是', '标准版'),
    ('Tala', 'tala', '菲律宾语女声', '多语种场景', '仅支持菲律宾语场景', '8K/16K', '否', '否', '标准版'),
    ('Tien', 'tien', '越南语女声', '多语种场景', '仅支持越南语场景', '8K/16K', '否', '否', '标准版'),
    ('Becca', 'becca', '美语客服女声', '美式英语', '支持纯英语场景', '8K/16K', '否', '否', '标准版'),
    ('Kyong', 'Kyong', '韩语女声', '韩语场景', '韩语', '8K/16K', '否', '否', '标准版'),
    ('masha', 'masha', '俄语女声', '俄语场景', '俄语', '8K/16K', '否', '否', '标准版'),
]
