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
    if alignment == 'center': return str1.center(distance, ' ')
    if not isinstance(str1, str): str1 = str(str1)
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


def str_split_limited_list(intext, mix=100, max=280):
    if len(intext) < mix:
        out_text = (intext, )
    else:
        out_text = re.findall(r'[\s\S]{' + str(mix) + ',' + str(max) + '}。', intext)
    return out_text


def str_split_limited_list_0(string, maxlen=300):
    # @出现超出长度的字符串
    # newText = [string[i:i+maxlen] for i in range(0, len(string), maxlen)]
    newText = []
    _temp = ''

    _temp_list = string.strip().split('\n')
    line_Text = [item.strip() for item in _temp_list]
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
    if isinstance(dict_tmp, dict):
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


upprintable_chars = [
    '\U0001f50d',
    '\u200b',
    '\ue627',
    '\U0001f640',
    '\U0001f236',
    '\U0001f468',
    '\U0001f44a',
    '\U0001f602',
    '\U0001f4b0',
    '\U0001f937',
    '\U0001f61f',
    '\U0001f31f',
    '\U0001f494',
    '\U0001f62d',
    '\U0001f436',
    '\U0001f605',
    '\U0001f914',
    '\U0001f449',
    '\U0001f4a9',
    '\U0001f973',
    '\U0001f251',
    '\U0001f414',
    '\xa0',
    '\U0001f649',
    '\u0160',
    '\U0001f44c',
    '\U0001f44d',
    '\u2795',
    '\u2b06',
    '\ufffc',
    '\U0001f44b',
    '\U0001f4a2',
    '\u270c',
    '\U0001f470',
    '\U0001f64a',
    '\U0001f631',
    '\u270a',
    '\U0001f60a',
    '\U0001f250',
    '\U0001f601',
    '\U0001f64b',
    '\U0001f434',
    '\U0001f923',
    '\U0001f92e',
    '\U0001f375',
    '\u263a',
    '\U0001f643',
    '\U0001f1fa',
    '\u30fb',
    '\U0001f64f',
    '\u2b55',
    '\U0001f31a',
    '\U0001f6be',
    '\U0001f990',
    '\U0001f338',
    '\U0001f921',
    '\U0001f474',
    '\U0001f606',
    '\U0001f917',
    '\u26a0',
    '\U0001f9e7',
    '\U0001f36d',
    '\U0001f9ce',
    '\U0001f21a',
    '\U0001f604',
    '\U0001f97a',
    '\U0001f48d',
    '\U0001f926',
    '\u2764',
    '\U0001f497',
    '\U0001f947',
    '\U0001f6ac',
    '\U0001f4a5',
    '\U0001f613',
    '\U0001f644',
    '\U0001f360',
    '\U0001f357',
    '\U0001f600',
    '\u0669',
    '\u27a1',
    '\U0001f4aa',
    '\U0001f972',
    '\U0001f38a',
    '\U0001f426',
    '\U0001f440',
    '\U0001f645',
    '\U0001f198',
    '\U0001f389',
    '\U0001f44f',
    '\U0001f339',
    '\U0001f622',
    '\U0001f9ee',
    '\U0001f5e1',
    '\U0001f970',
    '\u261d',
    '\U0001f92d',
    '\U0001f985',
    '\U0001f630',
    '\U0001f38e',
    '\U0001f9e0',
    '\U0001f466',
    '\U0001f981',
    '\U0001f4ab',
    '\u2716',
    '\U0001f3ac',
    '\ufe0f',
    '\U0001f976',
    '\U0001f451',
    '\u20e3',
    '\U0001f37b',
    '\u2601',
    '\U0001f4dd',
    '\U0001f9da',
    '\U0001f43e',
    '\U0001f95c',
    '\U0001f1e8',
    '\u0b67',
    '\U0001f4bc',
    '\U0001faa1',
    '\U0001f467',
    '\U0001f61c',
    '\u22ef',
    '\u2708',
    '\U0001f381',
    '\U0001f922',
    '\U0001f525',
    '\xb4',
    '\U0001f437',
    '\U0001f957',
    '\U0001f62e',
    '\U0001f934',
    '\u2753',
    '\u2062',
    '\U0001f34b',
    '\u2b50',
    '\U0001f34a',
    '\U0001f22f',
    '\U0001f33f',
    '\U0001f4a1',
    '\U0001f438',
    '\U0001f924',
    '\U0001f1f7',
    '\U0001f343',
    '\U0001f33c',
    '\U0001f4f0',
    '\U0001f349',
    '\U0001f49e',
    '\U0001f48c',
    '\u40fc',
    '\ufffd',
    '\U0001f4d6',
    '\U0001f4a4',
    '\U0001f940',
    '\u26ab',
    '\U0001f913',
    '\U0001f42f',
    '\u41b3',
    '\U0001f42d',
    '\U0001f3ab',
    '\U0001f951',
    '\U0001d7cf',
    '\U0001f648',
    '\U0001f42e',
    '\U0001f46e',
    '\uff61',
    '\U0001f47f',
    '\u2763',
    '\U0001f33b',
    '\u2728',
    '\U0001f3ca',
    '\U0001f408',
    '\U0001f95f',
    '\U0001f47b',
    '\u02f6',
    '\u2005',
    '\u274c',
    '\U0001f348',
    '\U0001f412',
    '\U0001d7f3',
    '\U0001f92a',
    '\U0001f6cd',
    '\u2022',
    '\U0001f31d',
    '\U0001f308',
    '\U0001f612',
    '\u2661',
    '\U0001f3e0',
    '\U0001f492',
    '\u2776',
    '\ua4a6',
    '\U0001f550',
    '\U0001f4b8',
    '\U0001f9b4',
    '\u2714',
    '\U0001f347',
    '\U0001f63f',
    '\U0001f3c6',
    '\u26f8',
    '\U0001f621',
    '\u203c',
    '\U0001f607',
    '\U0001f491',
    '\U0001f447',
    '\U0001f4f7',
    '\U0001f46b',
    '\U0001f3ef',
    '\u27a4',
    '\U0001f618',
    '\U0001f60d',
    '\U0001f351',
    '\u2003',
    '\u275d',
    '\U0001f9d0',
    '\U0001f610',
    '\U0001f344',
    '\u270d',
    '\u27ad',
    '\ua0c5',
    '\u2665',
    '\u200d',
    '\U0001f6f0',
    '\U0001f4f1',
    '\U0001d7da',
    '\u2705',
    '\U0001f62a',
    '\u2696',
    '\u261e',
    '\U0001f614',
    '\u23e9',
    '\U0001f91f',
    '\U0001f512',
    '\U0001f23a',
    '\U0001f4e2',
    '\u2006',
    '\u26f0',
    '\U0001f9f1',
    '\U0001d7d0',
    '\U0001f442',
    '\U0001f52e',
    '\u2797',
    '\U0001f63e',
    '\U0001f91e',
    '\U0001f624',
    '\U0001f40e',
    '\U0001f60b',
    '\U0001f60e',
    '\xde',
    '\U0001f9ca',
    '\u2713',
    '\U0001f199',
    '\U0001f620',
    '\U0001f62f',
    '\u279d',
    '\U0001fa86',
    '\U0001f448',
    '\U0001f490',
    '\U0001f628',
    '\u2757',
    '\U0001f92b',
    '\U0001f61e',
    '\U0001f35e',
    '\U0001f60c',
    '\u246f',
    '\U0001f46c',
    '\U0001f92c',
    '\U0001f46d',
    '\uff65',
    '\U0001f501',
    '\u2796',
    '\U0001fab6',
    '\U0001f3c4',
    '\U0001f62c',
    '\U0001f475',
    '\U0001f4a3',
    '\ub208',
    '\xbf',
    '\U0001f9cd',
    '\xd0',
    '\U0001f3a3',
    '\U0001f623',
    '\U0001f327',
    '\U0001f517',
    '\U0001f603',
    '\u2718',
    '\U0001f5a4',
    '\U0001f634',
    '\u2002',
    '\U0001f627',
    '\U0001f41e',
    '\U0001f4ec',
    '\U0001f68b',
    '\u2b07',
    '\U0001f68c',
    '\u2603',
    '\u262a',
    '\U0001f92f',
    '\u265b',
    '\xb2',
    '\U0001f49c',
    '\u11ba',
    '\U0001f6ab',
    '\U0001f98b',
    '\U0001f697',
    '\u2207',
    '\U0001f3f7',
    '\U0001fad3',
    '\U0001f505',
    '\u2614',
    '\U0001f6b2',
    '\U0001f30c',
    '\u25aa',
    '\u10e6',
    '\U0001f633',
    '\U0001f632',
    '\U0001f390',
    '\U0001f41f',
    '\U0001f19a',
    '\U0001f464',
    '\U0001f40f',
    '\u26fd',
    '\u26b0',
    '\U0001f3a7',
    '\U0001f332',
    '\U0001f431',
    '\U0001f40d',
    '\U0001f641',
    '\U0001f611',
    '\u231b',
    '\xfe',
    '\U0001fa78',
    '\U0001f986',
    '\U0001f3b9',
    '\U0001f4d5',
    '\U0001f69c',
    '\U0001f918',
    '\U0001f3b8',
    '\U0001f353',
    '\u25ab',
    '\u3297',
    '\u4d8a',
    '\u2122',
    '\U0001f64c',
    '\U0001f971',
    '\uc7ac',
    '\U0001f636',
    '\U0001f4ce',
    '\U0001f484',
    '\U0001f38b',
    '\U0001f49b',
    '\u0e51',
    '\U0001f609',
    '\U0001f386',
    '\U0001f34e',
    '\U0001f4a7',
    '\u010e',
    '\U0001f52a',
    '\U0001f963',
    '\U0001f004',
    '\u2639',
    '\U0001f346',
    '\U0001f419',
    '\U0001f450',
    '\xa5',
    '\U0001f91d',
    '\U0001f402',
    '\U0001f380',
    '\U0001f416',
    '\U0001f975',
    '\U0001f4cd',
    '\U0001f915',
    '\U0001f3b5',
    '\u202c',
    '\u25c8',
    '\U0001f90f',
    '\U0001f352',
    '\U0001f446',
    '\U0001f485',
    '\u26a1',
    '\U0001fad6',
    '\U0001f478',
    '\u2200',
    '\U0001f95d',
    '\U0001f337',
    '\U0001f4fa',
    '\U0001f409',
    '\U0001f37e',
    '\U0001f460',
    '\U0001f62b',
    '\U0001f53b',
    '\U0001f9d7',
    '\u2b05',
    '\U0001f539',
    '\U0001f635',
    '\u2028',
    '\U0001f30a',
    '\U0001f499',
    '\u4d97',
    '\U0001f919',
    '\u270f',
    '\U0001f4dc',
    '\U0001f237',
    '\U0001f646',
    '\u0ca5',
    '\U0001f350',
    '\u2618',
    '\U0001f363',
    '\U0001f932',
    '\U0001f420',
    '\U0001f930',
    '\u2579',
    '\u2600',
    '\U0001f194',
    '\U0001f1f0',
    '\u04f0',
    '\u314b',
    '\U0001f384',
    '\U0001f47d',
    '\U0001f629',
    '\U0001f6c0',
    '\U0001f514',
    '\U0001f4af',
    '\U0001f493',
    '\U0001f36b',
    '\U0001f928',
    '\U0001f430',
    '\U0001f495',
    '\U0001f98d',
    '\u202d',
    '\U0001f4e3',
    '\U0001f619',
    '\U0001f9f6',
    '\U0001f382',
    '\u25b6',
    '\U0001f4e9',
    '\U0001f6f5',
    '\u0150',
    '\xb3',
    '\U0001f95b',
    '\U0001f3a9',
    '\U0001f496',
    '\U0001f411',
    '\U0001f371',
    '\u0f40',
    '\u06ec',
    '\U0001f511',
    '\U0001f233',
    '\U0001f988',
    '\u27bf',
    '\u0b87',
    '\u25b8',
    '\u2765',
    '\u3405',
    '\U0001f345',
    '\U0001f4c6',
    '\U0001f476',
    '\u36ac',
    '\U0001d559',
    '\U0001f95a',
    '\U0001f596',
    '\u035f',
    '\U0001f693',
    '\U0001f625',
    '\U0001f942',
    '\U0001f48b',
    '\U0001f689',
    '\u2740',
    '\U0001f342',
    '\u0dc6',
    '\u0e40',
    '\u0ca1',
    '\U0001f927',
    '\U0001f695',
    '\U0001f637',
    '\U0001f961',
    '\U0001f33e',
    '\U0001f49a',
    '\U0001f41b',
    '\U0001f9c5',
    '\u2660',
    '\u202a',
    '\U0001f4a6',
    '\U0001f41c',
    '\U0001f910',
    '\u0e2d',
    '\U0001f3bc',
    '\u207d',
    '\U0001f96c',
    '\U0001f319',
    '\U0001f483',
    '\U0001f33a',
    '\u2af8',
    '\u202e',
    '\U0001f444',
    '\U0001f36c',
    '\U0001f362',
    '\U0001f3ba',
    '\U0001f4b3',
    '\ue031',
    '\U0001f3e1',
    '\u3164',
    '\U0001fa9e',
    '\U0001f9f8',
    '\u2744',
    '\U0001f41d',
    '\U0001f9f9',
    '\U0001f4b2',
    '\U0001f90d',
    '\U0001f37a',
    '\U0001f6fa',
    '\U0001f498',
    '\U0001f9c7',
    '\u260e',
    '\U0001f531',
    '\u2194',
    '\U0001f4ee',
    '\u1566',
    '\U0001f232',
    '\U0001f698',
    '\U0001f51d',
    '\U0001f3cd',
    '\u2049',
    '\u1111',
    '\U0001f370',
    '\U0001f980',
    '\U0001fa84',
    '\U0001f445',
    '\xc0',
    '\U0001f616',
    '\U0001f48a',
    '\u02d8',
    '\U0001f90c',
    '\U0001f99a',
    '\U0001f608',
    '\U0001f98c',
    '\U0001f61d',
    '\U0001f6cb',
    '\U0001f400',
    '\U0001f456',
    '\u2328',
    '\U0001f53a',
    '\U0001f4c8',
    '\U0001f535',
    '\U0001f44e',
    '\U0001f3f4',
    '\U0001f647',
    '\U0001f48f',
    '\U0001f590',
    '\U0001f91c',
    '\U0001f31e',
    '\U0001f638',
    '\U0001fa96',
    '\U0001f7e2',
    '\U0001f534',
    '\U0001f324',
    '\U0001f37d',
    '\u266a',
    '\U0001f6ae',
    '\u270b',
    '\U0001f364',
    '\U0001f422',
    '\U0001f642',
    '\u2779',
    '\xf1',
    '\xa1',
    '\U0001f3ad',
    '\U0001f978',
    '\u0e3f',
    '\u231a',
    '\U0001f330',
    '\U0001f367',
    '\U0001f334',
    '\u2615',
    '\u23f0',
    '\U0001f94a',
    '\u0295',
    '\U0001f3e5',
    '\U0001f9ff',
    '\U0001f46a',
    '\U0001f93a',
    '\U0001f935',
    '\U0001f3d0',
    '\U0001f933',
    '\ue768',
    '\u208d',
    '\U0001f310',
    '\u269c',
    '\U0001f3a8',
    '\U0001f6bf',
    '\U0001f9e1',
    '\u23eb',
    '\u3299',
    '\U0001f415',
    '\U0001f48e',
    '\u2f25',
    '\u9fba',
    '\U0001f372',
    '\u379e',
    '\U0001fa82',
    '\U0001f52c',
    '\U0001f9c4',
    '\u2702',
    '\ua9c1',
    '\u25c2',
    '\U0001f98a',
    '\U0001f3a4',
    '\u2755',
    '\U0001f56f',
    '\ua426',
    '\U0001f37c',
    '\u2726',
    '\U0001f964',
    '\u25b7',
    '\u21e8',
    '\U0001f358',
    '\U0001f373',
    '\U0001f42c',
    '\U0001f34d',
    '\u2662',
    '\u2651',
    '\U0001f911',
    '\u2604',
    '\U0001f6b9',
    '\U0001f929',
    '\U0001f36a',
    '\u196c',
    '\U0001f6cf',
    '\u301c',
    '\U0001f35c',
    '\U0001f6f9',
    '\u203a',
    '\u26ea',
    '\U0001f538',
    '\U0001f457',
    '\U0001f383',
    '\uff89',
    '\U0001f96e',
    '\U0001f60f',
    '\U0001f1ee',
    '\u200e',
    '\U0001f427',
    '\U0001f4a8',
    '\U0001f96d',
    '\U0001f388',
    '\U0001f9a2',
    '\U0001f49d',
    '\U0001f513',
    '\U0001f3bf',
    '\xc4',
    '\U0001f595',
    '\U0001f96b',
    '\U0001f30e',
    '\U0001f369',
    '\U0001fa80',
    '\U0001f325',
    '\U0001f335',
    '\ub85c',
    '\U0001f43a',
    '\u2470',
    '\uccab',
    '\u272a',
    '\xa6',
    '\u3030',
    '\U0001f9e2',
    '\uff9f',
    '\U0001f6a4',
    '\U0001f336',
    '\U0001f6b6',
    '\U0001f91a',
    '\U0001f50a',
    '\xbd',
    '\u20ab',
    '\u2611',
    '\u032e',
    '\u3873',
    '\u0b90',
    '\U000fe4ed',
    '\U001003ae',
    '\U0001f399',
    '\u267e',
    '\U0001f6f8',
    '\u45a1',
    '\U0001f443',
    '\uae30',
    '\U0001f557',
    '\xaf',
    '\U0001f9b6',
    '\U0001f302',
    '\U0001f4e8',
    '\U0001f944',
    '\u0f0a',
    '\U0001f974',
    '\u0e05',
    '\U0001f4d2',
    '\U0001f340',
    '\U0001f481',
    '\U0001f51a',
    '\u200c',
    '\U0001d648',
    '\U0001f573',
    '\U0001f3b6',
    '\U0001f6d2',
    '\U0001f471',
    '\u23f1',
    '\U0001f486',
    '\U0001f1f1',
    '\U0001f192',
    '\U0001f331',
    '\ue4e1',
    '\xfb',
    '\U0001f51f',
    '\U0001f423',
    '\u261c',
    '\u0ae2',
    '\U0001f916',
    '\U0001f305',
    '\U0001f699',
    '\u2590',
    '\u25d8',
    '\U0001f477',
    '\u06f0',
    '\xae',
    '\u2592',
    '\u278a',
    '\U0001f35a',
    '\U0001f559',
    '\u053e',
    '\U0001f54a',
    '\U0001f3e6',
    '\U0001f3b2',
    '\u25fe',
    '\U0001f4c9',
    '\u2710',
    '\U0001f64e',
    '\U0001fa90',
    '\u2754',
    '\U0001f639',
    '\U0001f9ec',
    '\u325b',
    '\xa3',
    '\U0001f235',
    '\U0001f1f3',
    '\U0001f341',
    '\U0001f3d8',
    '\u27a8',
    '\U0001f43c',
    '\u22b1',
    '\u24de',
    '\U0001f3c0',
    '\u263c',
    '\U0001f9d2',
    '\u25d5',
    '\u25e6',
    '\u25a5',
    '\u25bf',
    '\xac',
    '\xba',
    '\u1d40',
    '\u25d9',
    '\u1d2c',
    '\u2027',
    '\U0001f3ee',
    '\u25ac',
    '\u2449',
    '\U0001f452',
    '\U0001f4c0',
    '\U0001f4da',
    '\U0001f9d3',
    '\U0001f4de',
    '\u25a3',
    '\u269b',
    '\u0f80',
    '\ue804',
    '\u260f',
    '\uc131',
    '\u25c4',
    '\U0001f0cf',
    '\u36c7',
    '\U0001f9dc',
    '\U0001d400',
    '\U0001f417',
    '\u260c',
    '\xa9',
    '\u0e01',
    '\U0001f4b7',
    '\U0001f6b8',
    '\u2732',
    '\U0001f35d',
    '\u2602',
    '\U0001f1f9',
    '\u2778',
    '\u1d35',
    '\U0001f1ec',
    '\U0001d663',
    '\U0001f68a',
    '\U0001f3dd',
    '\U0001d653',
    '\U0001f984',
    '\U0001d412',
    '\U0001f9e8',
    '\ua9bf',
    '\U0001f5fe',
    '\u2f12',
    '\U0001f68e',
    '\u2620',
    '\ue14c',
    '\u25d1',
    '\U0001f333',
    '\u2663',
    '\U0001d413',
    '\U0001d54b',
    '\U0001f684',
    '\U0001fa70',
    '\U0001d47e',
    '\U0001d7d2',
    '\U0001f195',
    '\u2777',
    '\U0001f1ef',
    '\u1d39',
    '\U0001f42b',
    '\ue004',
    '\U0001d4f0',
    '\u25cd',
    '\U0001f58d',
    '\uff62',
    '\U0001f69d',
    '\U0001f6d7',
    '\U0001f528',
    '\ub098',
    '\U0001f5bc',
    '\U0001f931',
    '\u25e1',
    '\U0001f6bd',
    '\U0001f425',
    '\ue412',
    '\U0001f4bd',
    '\xe2',
    '\u2061',
    '\U0001f685',
    '\U0001f5ef',
    '\u2727',
    '\U0001f4b6',
    '\ue12e',
    '\u375a',
    '\U0001f996',
    '\u0f58',
    '\U0001f61a',
    '\U0001f377',
    '\U0001f314',
    '\ue41d',
    '\U0001f43b',
    '\U0001f4cc',
    '\U0001f43d',
    '\u21d2',
    '\U0001f3c3',
    '\U0001f55b',
    '\ufeff',
    '\U0001f615',
    '\u2202',
    '\U000201a4',
    '\U0001f51c',
    '\u20ac',
    '\u36f0',
    '\u261f',
    '\U0001f4f2',
    '\U0001f31b',
    '\ue0ed',
    '\u4dae',
    '\ue022',
    '\U0001f558',
    '\U0001f4b5',
    '\u262f',
    '\U0001f365',
    '\uc18c',
    '\u22c8',
    '\xad',
    '\uf0d8',
    '\U0001f912',
    '\U0001f429',
    '\U0001f4e1',
    '\U0001f3df',
    '\ue021',
    '\u26bd',
    '\u27b0',
    '\U0001f3c5',
    '\ue10e',
    '\U0001f459',
    '\U0001f49f',
    '\ue536',
    '\U0001f40a',
    '\u03ea',
    '\U0001f413',
    '\ue112',
    '\u25ba',
    '\ue32e',
    '\uff64',
    '\ue115',
    '\ue404',
    '\ue312',
    '\u0301',
    '\u032f',
    '\u20dd',
    '\u0847',
    '\U0001d7f1',
    '\U0001d7d1',
    '\U0001d7d4',
    '\U0001f428',
    '\U0001d7ef',
    '\u0171',
    '\u203e',
    '\U0001f95e',
    '\U0001f999',
    '\u277b',
    '\u0eb4',
    '\U0001f6eb',
    '\U0001f3f0',
    '\U0001f4f8',
    '\U0001d41c',
    '\U0001d5ee',
    '\U0001f421',
    '\U0001f171',
    '\ua34f',
    '\U0001d7d9',
    '\u029a',
    '\u20db',
    '\U0001f432',
    '\U0001f4e6',
    '\U0001f950',
    '\U0001d7ce',
    '\u014c',
    '\U0001f35f',
    '\u014e',
    '\U0001f954',
    '\u1f62',
    '\u2b1b',
    '\xd4',
    '\u25e0',
    '\U0001f3e9',
    '\u0ca0',
    '\U0001f69a',
    '\u1b44',
    '\u04e7',
    '\xd3',
    '\U0001d652',
    '\u0178',
    '\uc601',
    '\U0001f9d5',
    '\U0001f506',
    '\u3142',
    '\u016c',
    '\xd5',
    '\U0001f38f',
    '\U0001f321',
    '\U0001f354',
    '\u0308',
    '\U0001f6a3',
    '\u2668',
    '\u0364',
    '\u0e47',
    '\U0001f3e7',
    '\U0001f578',
    '\u2323',
    '\xd2',
    '\U0001f30b',
    '\U0001f3eb',
    '\U0001f393',
    '\U0001f3ae',
    '\U0001f9b1',
    '\U0001f385',
    '\u25ca',
    '\xd8',
    '\U0001f3c2',
    '\U0001f52b',
    '\u2f45',
    '\u317f',
    '\U0001f47c',
    '\U0001f51b',
    '\u0fb3',
    '\U0001f5e3',
    '\u0125',
    '\xd6',
    '\u02ae',
    '\U0001d464',
    '\U0001d552',
    '\u3268',
    '\U0001d7f0',
    '\u035e',
    '\U0001f3fe',
    '\U0001f463',
    '\u277a',
    '\U0001f941',
    '\u1d57',
    '\u0e21',
    '\u0e17',
    '\u0e34',
    '\U0001f959',
    '\u207e',
    '\u016e',
    '\U0001f962',
    '\u2af7',
    '\u034f',
    '\U0001f4d9',
    '\u0648',
    '\U0001f692',
    '\u1564',
    '\U0001f3de',
    '\U0001f4bb',
    '\u26e9',
    '\u26aa',
    '\U0001f6f3',
    '\U0001f536',
    '\U0001f9fb',
    '\U0001f3db',
    '\U0001f4a0',
    '\u0329',
    '\U0001f955',
    '\U0001f57a',
    '\U0001f303',
    '\U0001f304',
    '\U0001f560',
    '\U0001f4fd',
    '\U0001f5dd',
    '\U0001f366',
    '\U0001f3d9',
    '\U0001d4a2',
    '\u1d34',
    '\U0001f965',
    '\U0001f9ea',
    '\u2721',
    '\u2730',
    '\u029c',
    '\xdd',
    '\U0001d644',
    '\u0361',
    '\U0001f32b',
    '\U0001f307',
    '\U0001f516',
    '\uffe8',
    '\U0001f433',
    '\U0001f3b1',
    '\U0001f3fd',
    '\U0001f30d',
    '\u2712',
    '\u2699',
    '\u030c',
    '\U0001f680',
    '\u1dc5',
    '\U0001f37f',
    '\U0001d46e',
    '\u1d55',
    '\U0001f407',
    '\U0001f359',
    '\u26f1',
    '\u2652',
    '\U0001f4ad',
    '\U0001f6ba',
    '\U0001f925',
    '\U0001f465',
    '\u0952',
    '\U0001f9b5',
    '\U0001f9b3',
    '\U0001f6a2',
    '\U0001f694',
    '\U0001f4d3',
    '\u2039',
    '\U0001f508',
    '\U0001f33d',
    '\U0001f1ed',
    '\xb8',
    '\u1d17',
    '\u0967',
    '\u2134',
    '\u25d2',
    '\U0001f9fa',
    '\ucc28',
    '\U0001f3dc',
    '\U0001f193',
    '\U0001f4ed',
    '\u2b1c',
    '\U0001f4b4',
    '\U0001f943',
    '\uac74',
    '\U0001f405',
    '\ucc98',
    '\U0001f41a',
    '\U0001f361',
    '\u278b',
    '\u0455',
    '\U0001f34f',
    '\u22b9',
    '\u2666',
    '\U0001f455',
    '\u0f72',
    '\U0001f5d1',
    '\u0665',
    '\U0001f328',
    '\U0001f1e6',
    '\U0001d4db',
    '\U0001f9b2',
    '\U0001d656',
    '\U0001f45c',
    '\U0001f441',
    '\ufe0e',
    '\u0e1f',
    '\ufecc',
    '\U0001d7d3',
    '\U0001f1f2',
    '\U0001f32c',
    '\U0001f9d6',
    '\u3160',
    '\u263b',
    '\u2591',
    '\u266b',
    '\u06e9',
    '\U0001f9b0',
    '\U0001f96a',
    '\U0001f686',
    '\ufe20',
    '\U0001f17c',
    '\U0001f63a',
    '\u06f6',
    '\U0001f376',
    '\U0001f35b',
    '\u0348',
    '\U0001f64d',
    '\U0001f4bf',
    '\U0001f5fb',
    '\U0001f9d4',
    '\u275c',
    '\U0001f379',
    '\U0001f1f5',
    '\u2c19',
    '\u22db',
    '\u24e5',
    '\u2650',
    '\U0001f480',
    '\u25a6',
    '\u25a7',
    '\u2749',
    '\u20de',
    '\u02b0',
    '\U0001f554',
    '\u1d48',
    '\U0001d4fd',
    '\u2695',
    '\U0001f439',
    '\U0001f9b7',
    '\U0001f3a5',
    '\u266f',
    '\u0f3e',
    '\U0001f4fb',
    '\uc5ed',
    '\u203f',
    '\U0001f6f4',
    '\U0001d40c',
    '\u260d',
    '\u0e23',
    '\U0001f31c',
    '\u2fa5',
    '\u2653',
    '\u0e07',
    '\u27b9',
    '\u1d33',
    '\U0001f9c0',
    '\u24ff',
    '\u02e1',
    '\u277e',
    '\U0001d65e',
    '\U0001d5e5',
    '\uce74',
    '\u26c4',
    '\U0001f3cc',
    '\U0001d430',
    '\u1ba8',
    '\U0001f958',
    '\U0001f6c1',
    '\U0001d7f5',
    '\U0001d642',
    '\U0001d418',
    '\U0001d407',
    '\u210d',
    '\u277d',
    '\U0001f1e7',
    '\u22cc',
    '\u03af',
    '\u266c',
    '\u2580',
    '\U0001d486',
    '\u277c',
    '\u1d43',
    '\U0001f3a6',
    '\U0001d4f8',
    '\U0001d63f',
    '\uff6a',
    '\uff63',
    '\u2709',
    '\u1d3e',
    '\U0001f45b',
    '\U0001f4c4',
    '\U0001f3e8',
    '\xee',
    '\uadfc',
    '\u0f0b',
    '\U0001f36f',
    '\u17b5',
    '\U0001f519',
    '\ud32c',
    '\uc694',
    '\ud3ec',
    '\ud2b8',
    '\ube44',
    '\U0001f510',
    '\U0001f4cb',
    '\uc608',
    '\u25c3',
    '\u2659',
    '\U0001f170',
    '\u2023',
    '\xbe',
    '\U0001f63b',
    '\uac1c',
    '\u2648',
    #'\u033',
]
'''
lists = ['神奇', '建投', '证券', '有限公司', '今天', '投资', '了', '一', '款',"神迹",'游戏']
replace_dict = {'神奇':"奇幻","神迹":"奇迹"}
new_lists =[replace_dict[i] if i in replace_dict else i for i in lists]
'''
