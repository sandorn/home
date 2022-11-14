# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion :  string  |  dict  |  list  |  tupe  |  json
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-02-14 13:57:28
FilePath     : /xjLib/xt_String.py
LastEditTime : 2021-04-14 18:05:09
# Github       : https://github.com/sandorn/home
# ==============================================================
'''

import hashlib
import json
import random
import re
from functools import reduce


def Ex_md5(data):
    """将string转化为MD5"""
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest


def Ex_sha1(data):
    my_sha = hashlib.sha1()
    my_sha.update(data.encode("utf-8", 'ignore'))
    my_sha_Digest = my_sha.hexdigest()
    return my_sha_Digest


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    保序去重
    :param iterable:
    :param keep: 去重的同时要对element做的操作
    :param key: 使用哪一部分去重
    :param reverse: 是否反向去重
    :return:
    """
    result = list()
    duplicator = list()
    if reverse:
        iterable = reversed(iterable)
    for i in iterable:
        keep_field = keep(i)
        key_words = key(i)
        if key_words not in duplicator:
            result.append(keep_field)
            duplicator.append(key_words)
    return list(reversed(result)) if reverse else result


def chain_all(iterobj):
    """连接多个序列或字典"""
    iterobj = list(iterobj)
    if not iterobj:
        return []
    if isinstance(iterobj[0], dict):
        result = {}
        for i in iterobj:
            result.update(i)
    else:
        result = reduce(lambda x, y: list(x) + list(y), iterobj)
    return result


def align(str1, distance=66, alignment='left'):
    # #居中打印为string类方法
    if alignment == 'center':
        return str1.center(distance, ' ')

    # #print打印对齐
    length = len(str1.encode('gbk', 'ignore'))
    slen = distance - length if distance > length else 0

    if alignment == 'left':
        str1 = str1 + ' ' * slen
    elif alignment == 'right':
        str1 = ' ' * slen + str1
    return str1


def Str_Replace(replacement, trims):
    """
    # @字符替换，不支持正则
    replacement:欲处理的字符串
    trims:list内包含tuple或list
    trims[0]:查找,trims[1]:替换
    """
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item[0], item[1])
    # return replacement

    # 第二种方法  # replacement 为初始值，最后传入，在lambda中最先接收
    return reduce(lambda strtmp, item: strtmp.replace(item[0], item[1]), trims, replacement)


def Str_Clean(replacement, trims):
    """
    # @字符清除，不支持正则
    replacement:欲处理的字符串
    trims:list内包含tuple或list
    """
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item, '')
    # return replacement

    # 第二种方法  # replacement 为初始值，最后传入，在lambda中最先接收
    return reduce(lambda strtmp, item: strtmp.replace(item, ''), trims, replacement)


def Re_Sub(replacement, trims=None):
    """
    # @re.sub正则替换，自写表达式
    replacement:欲处理的字符串
    trims:list内包含tuple或list
    trims[0]:查找字符串,trims[1]:替换字符串
    """
    # 第一种方法
    if trims is None:
        # #格式化html string, 去掉多余的字符，类，script等。
        trims = [(r'\n', ''), (r'\t', ''), (r'\r', ''), (r'  ', ''), (r'\u2018', "'"), (r'\u2019', "'"), (r'\ufeff', ''), (r'\u2022', ":"), (r"<([a-z][a-z0-9]*)\ [^>]*>", r'<\g<1>>'), (r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', ''), (r"</?a.*?>", '')]

    def run(trims, replacement):
        return re.sub(replacement[0], replacement[1], trims)

    return reduce(run, trims, replacement)

    # 第二种写法，用lamda # replacement为初始值，最后传入，在lambda中最先接收
    # return reduce(lambda str_tmp, replacement: re.sub(replacement[0], replacement[1], str_tmp), trims, replacement)


def Re_Compile(replacement, trims_dict):
    """
    # ! re.compile正则替换，自写表达式，字典key受限，暂留
    replacement:欲处理的字符串
    trims_dict:dict
    用法=Re_Compile(replacement,{'A':'aaa','B':'bbb'})
    """
    pattern = re.compile('|'.join(trims_dict.keys()))
    return pattern.sub(lambda m: trims_dict[m.group(0)], replacement)


def string_split_limited_list(string, maxlen=300):
    # #仅按照长度分割
    # #newText = [string[i:i+maxlen] for i in range(0, len(string), maxlen)]
    newText = []
    _temp = ''

    _temp_list = string.strip().split('\n')
    line_Text = [item.strip() for item in _temp_list]
    line_Text[0] = line_Text[0] + '。'  # 章节标题加间隔

    for index, text in enumerate(line_Text):
        if len(text) > maxlen:
            if _temp != '':
                newText.append(_temp)
                _temp = ''

            temp = text.strip().split('。')
            long = round(len(temp) / 2)
            newText.append('。'.join(temp[:long]) + '。')
            newText.append('。'.join(temp[long:]))
            continue

        if len(_temp) < maxlen:
            if len(_temp + text.strip()) < maxlen:
                _temp += text
                # @ 标记1
            else:
                newText.append(_temp)
                newText.append(text)
                _temp = ''

    # @ 标记1,最后处理临时变量
    if _temp != '':
        newText.append(_temp)
        _temp = ''

    return newText


def dict2qss(dict_tmp):
    '''字典形式的QSS转字符串'''
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    isinstance(dict_tmp, dict)
    temp = json.dumps(dict_tmp)
    qss = Str_Replace(temp, [(',', ';'), ('"', ''), (': {', '{')])
    return qss.strip('{}')


def groupby(iterobj, key):
    """
    自实现groupby，return: 字典对象
    itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    """
    groups = dict()
    for item in iterobj:
        groups.setdefault(key(item), []).append(item)
    return groups


def random_char(length=20, string=[]):
    """实现指定长度的随机数"""
    for i in range(length):
        x = random.randint(1, 2)
        if x == 1:
            y = str(random.randint(0, 9))
        else:
            y = chr(random.randint(97, 122))
        string.append(y)
    string = ''.join(string)
    return string


def class_add_dict(in_obj):
    '''把对象转换成字典'''
    in_obj.__dict__ = {key: getattr(in_obj, key) for key in dir(in_obj) if not key.startswith('__') and not callable(getattr(in_obj, key))}
    return in_obj.__dict__


'''
lists = ['神奇', '建投', '证券', '有限公司', '今天', '投资', '了', '一', '款',"神迹",'游戏']
replace_dict = {'神奇':"奇幻","神迹":"奇迹"}
new_lists =[replace_dict[i] if i in replace_dict else i for i in lists]
'''
