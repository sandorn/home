# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : string  |  dict  |  list  |  tupe  |  json
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-02-25 04:31:14
FilePath     : /CODE/xjLib/xt_String.py
Github       : https://github.com/sandorn/home
==============================================================
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
    return my_md5.hexdigest()


def Ex_sha1(data):
    my_sha = hashlib.sha1()
    my_sha.update(data.encode("utf-8", 'ignore'))
    return my_sha.hexdigest()


def encrypt_str(data, algorithm='md5'):
    """ 用不同算法对字符串进行加密
    :param data: 待加密的字符串
    :param algorithm: 加密算法，可以是 md5 or sha1
    :return: 密文
    """
    if algorithm == 'md5':
        my_encrypt = hashlib.md5()
    elif algorithm == 'sha1':
        my_encrypt = hashlib.sha1()
    else:
        print('Unsupported algorithm.')
        return False

    my_encrypt.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    return my_encrypt.hexdigest()


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    增强去重功能，解决了重复元素可能覆盖的问题
    :param iterable: 需要去重的可迭代对象
    :param keep: 需要保留的元素，例如只保留某个字段
    :param key: 重复元素的判断字段
    :param reverse: 是否反向去重
    :return: 去重后的可迭代对象
    """
    # 创建一个字典存储重复的key和其他值
    duplicator = {}
    # 使用列表来存储有效的值
    result = []
    if reverse: iterable = reversed(iterable)
    # 遍历所有元素
    for i in iterable:
        # 调用keep函数获取该元素值
        keep_field = keep(i)
        # 调用key函数获取该元素key值
        key_words = key(i)
        # 如果key值在字典中不存在，则将元素填入字典，并将该元素添加到result列表中
        if key_words not in duplicator:
            duplicator[key_words] = keep_field
            result.append(keep_field)
    return list(reversed(result)) if reverse else result


def align(str1, distance=66, alignment='L'):
    # #居中打印为string类方法
    if alignment == 'C': return str1.center(distance, ' ')
    if not isinstance(str1, str): str1 = str(str1)
    # #print打印对齐
    length = len(str1.encode('utf-8', 'ignore'))
    slen = max(0, distance - length)

    if alignment == 'L':
        aligned_str = f"{str1}{' ' * slen}"
    elif alignment == 'R':
        aligned_str = f"{' ' * slen}{str1}"
    else:
        raise ValueError(
            "Alignment must be one of 'left', 'center', or 'right'")
    return aligned_str


def remove_all_blank(value, keep_blank=True):
    """移除所有不可见字符,默认保留空格"""
    if keep_blank:
        return ''.join(ch for ch in value if ch.isprintable())
    else:
        # return ''.join(filter(lambda c: c.isprintable() and not c.isspace(), value))
        return ''.join(ch for ch in value
                       if ch.isprintable() and not ch.isspace())


def clean_invisible_chars(text):
    '''定义要清除的不可见字符的正则表达式'''
    invisible_chars_pattern = r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+'
    return re.sub(invisible_chars_pattern, '', text)


def Str_Replace(replacement: str, trims: list[list | tuple]):
    """
    # @字符替换，不支持正则
    replacement:欲处理的字符串
    trims: list[list | tuple], [('a', 'A'), ('b', 'B'), ('c', 'C')]
    trims[0]:查找,trims[1]:替换
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item[0], item[1])
    # return replacement
    # 第二种方法  # replacement 为初始值,最后传入,在lambda中最先接收
    """

    return reduce(
        lambda strtmp, item: strtmp.replace(
            item[0],
            item[1],
        ),
        trims,
        replacement,
    )


def Str_Clean(replacement: str, trims: list | tuple) -> str:
    """
    # @字符清除，不支持正则
    replacement:欲处理的字符串
    trims: list | tuple
    """
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item, '')
    # return replacement

    # 第二种方法  # replacement 为初始值，最后传入，在lambda中最先接收
    return reduce(
        lambda strtmp, item: strtmp.replace(
            item,
            "",
        ),
        trims,
        replacement,
    )


def Re_Sub(replacement: str, trims: list[list | tuple]):
    """
    @ re.sub正则替换,自写表达式
    replacement:欲处理的字符串
    trims:: list[list | tuple]
    trims[0]:查找字符串,trims[1]:替换字符串
    """
    # lamda表达式,参数与输入值顺序相反
    if trims is None: return replacement

    return reduce(
        lambda str_tmp, item: re.sub(
            item[0],
            item[1],
            str_tmp,
        ),
        trims,
        replacement,
    )


def Re_Compile(replacement: str, trimsL: list[list | tuple]):
    """
    re.compile正则替换,自写表达式
    replacement:欲处理的字符串
    trims: list[list | tuple]
    用法=Re_Compile(replacement,[('A', 'aaa'), ('B', 'bbb')])
    """

    # for trim in trimsL:
    #     pattern = re.compile(trim[0])
    #     replacement = pattern.sub(trim[1], replacement)
    # return replacement
    if not isinstance(replacement, str):
        raise TypeError(f"Expected str, got {type(replacement)}")
    if not isinstance(trimsL, list):
        raise TypeError(f"Expected list, got {type(trimsL)}")
    if not all(isinstance(t, (tuple, list)) for t in trimsL):
        raise TypeError(f"Expected list of lists or tuples, got {trimsL}")

    pattern = re.compile('|'.join(t[0] for t in trimsL))
    return pattern.sub(
        lambda x: next((t[1] for t in trimsL if t[0] == x.group()), x.group()),
        replacement,
    )


def str_split_limited_list(intext, mixnum=100, maxnum=280):
    return ([intext] if len(intext) < mixnum else re.findall(
        r'[\s\S]{' + str(mixnum) + ',' + str(maxnum) + '}。', intext))


def str2list(intext, maxlen=300):
    """
    将输入的字符串分割成若干个段落，每个段落的长度不超过 maxlen。
    """
    # 按照句号（。）将原始字符串分割为一组子串
    sentence_list = re.split(
        '。', Str_Replace(intext, [['\r', '。'], ['\n', '。'], [' ', '']]))
    # 过滤掉空子串，并添加句号
    sentence_list = [f'{item}。' for item in sentence_list if item]

    paragraph_list = []
    current_paragraph = ''
    for sentence in sentence_list:
        # 如果当前段落长度不超过最大长度，则继续添加新的句子
        if len(current_paragraph + sentence) <= maxlen:
            current_paragraph += sentence
        else:
            # 否则，当前段落结束，添加到段落列表中
            paragraph_list.append(current_paragraph)
            current_paragraph = sentence

    # 处理最后一个段落
    if current_paragraph:
        paragraph_list.append(current_paragraph)

    return paragraph_list


def dict2qss(dict_tmp: dict):
    '''字典形式的QSS转字符串。弃用!
        qdarkstyle.utils.scss._dict_to_scss 替代
    '''
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    temp = json.dumps(dict_tmp)
    qss = Str_Replace(temp, [(',', ';'), ('"', ''), (': {', '{')])
    return qss.strip("{}")


def groupby(iterobj, key):
    """
    自实现groupby,return: 字典对象
    itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    """
    groups = {}
    for item in iterobj:
        groups.setdefault(key(item), []).append(item)
    return groups


def random_char(length=20):
    """实现指定长度的随机数"""
    res_str = []
    for _ in range(length):
        x = random.randint(1, 2)
        y = str(random.randint(0, 9)) if x == 1 else chr(
            random.randint(97, 122))
        res_str.append(y)
    return ''.join(res_str)


def class_add_dict(in_obj):
    '''把对象转换成字典'''
    # in_obj.__dict__ = {key: getattr(in_obj, key) for key in dir(in_obj) if not key.startswith('__') and not callable(getattr(in_obj, key))}
    in_obj.__dict__ = {
        key: value
        for key, value in vars(in_obj).items()
        if not key.startswith('__') and not callable(value)
    }
    return in_obj.__dict__


if __name__ == '__main__':

    def test_str_replace(self):
        replacement = 'aaabbbccc'
        trims = [('a', 'A'), ('b', 'B'), ('c', 'C')]

        Str_Replace(replacement, trims)

    # test_str_replace()

    def test_str_clean():
        test_str = "###hello?world"
        result = Str_Clean(test_str, ["#", "?"])

        assert result == "hello|world", result

    # test_str_clean()

    def test_Re_Sub():
        replacement = "This\n is \u2018a\u2019 test\ufeff string"
        trims = [("\n", ""), ("\u2018", "'"), ("\u2019", "'"), ("\ufeff", "")]
        expected_result = "This is 'a' test string"
        result = Re_Sub(replacement, trims)
        assert result == expected_result, result

    # test_Re_Sub()

    def test_Re_Compile():
        replacement = 'hello A and B'
        trims_list = [('A', 'aaa'), ('B', 'bbb')]
        result = Re_Compile(replacement, trims_list)
        print(result)

    # test_Re_Compile()
    str2 = "Powe, on；the 2333, 。哈哈 ！！\U0001f914看看可以吗？一行代码就可以了！^_^"
    # print(remove_all_blank(str2, keep_blank=False))
    print(clean_invisible_chars(str2))
