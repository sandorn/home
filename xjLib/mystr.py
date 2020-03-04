# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-14 13:57:28
@LastEditors: Even.Sand
@LastEditTime: 2020-03-02 12:32:42
'''
import re

import hashlib


def md5(txt):
    data = txt
    m = hashlib.md5(data.encode("utf-8", 'ignore'))
    return (m.hexdigest())


def myAlign(text, distance=0):
    # #print打印对齐
    if distance == 0:
        return text
    slen = distance - len(text.encode('gbk', 'ignore'))
    text = text + ' ' * slen
    return text


def align(str1, distance, alignment='left'):
    # #print打印对齐
    length = len(str1.encode('gbk', 'ignore'))
    slen = distance - length if distance > length else 0
    if (slen % 2) == 1:
        slen = slen + 1

    if alignment == 'left':
        str1 = str1 + ' ' * slen
    elif alignment == 'right':
        str1 = ' ' * slen + str1
    elif alignment == 'center':
        str1 = ' ' * (slen // 2) + str1 + ' ' * (slen // 2)
    return str1


def cn2num(章节编号):
    # 实现了中文向阿拉伯数字转换
    # 用于从小说章节名提取id来排序
    #!待调试
    chs_arabic_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                      '十': 10, '百': 100, '千': 10 ** 3, '万': 10 ** 4,
                      '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                      '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
                      '拾': 10, '佰': 100, '仟': 10 ** 3, '萬': 10 ** 4,
                      '亿': 10 ** 8, '億': 10 ** 8, '幺': 1,
                      '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                      '7': 7, '8': 8, '9': 9}

    num_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '零', '千',
                '百', ]

    def get_tit_num(title):
        result = ''
        for char in title:
            if char in num_list:
                result += char
        return result

    chinese_digits = get_tit_num(章节编号)
    result = 0
    tmp = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char = chinese_digits[count]
        curr_digit = chs_arabic_map[curr_char]
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result = result + tmp
            result = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result = 0
            tmp = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result


# 章节数字转换
def change2num(章节编号):
    num_enum = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2
    }
    multi_cov = {'百': 100, '十': 10}
    m = 0
    mc = 1
    rev_name = 章节编号[::-1]
    for t_str in rev_name:
        if t_str in num_enum:
            m += num_enum[t_str] * mc
        if t_str in multi_cov:
            mc = multi_cov[t_str]
    # 第十二章，第十章特例
    if 章节编号 == '十':
        m += 10
    return m


def Ex_Re_Sub(oldtext, *args, **kwds):
    '''
    用法 newtext=Ex_Re_Sub(oldtext,{'\n\n':'\n'}):
    '''
    adict = dict(*args, **kwds)
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, oldtext)


def list2file(_filename, _list_texts, br='\t'):
    # 函数说明:将爬取的文章内容写入文件,只能1层
    print('[' + _filename + ']开始保存......', flush=True)
    _list_texts.sort()
    with open(_filename, 'w', encoding='utf-8') as f:
        f.write('   key   \tpage\tindex\ttitle\turl\t\n')
        for key in _list_texts:  # 区分关键字
            for index in key:  # 区分记录index
                [f.write(str(v) + br) for v in index]
                f.write('\n')

    print('[' + _filename + ']保存完成。', flush=True)
    # # 下面换行问题
    # #[f.write(str(v) + '\t') for key in lists for index in key for v in index]


def savefile(_filename, _list_texts, br='\t'):
    # 函数说明:将爬取的文章内容写入文件,迭代多层
    # #多层次的list 或 tuple写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    with open(_filename, 'w', encoding='utf-8') as f:

        def each(data):
            for index, value in enumerate(data):
                if isinstance(value, list) or isinstance(value, tuple):
                    each(value)
                else:
                    f.write(str(value) + br)
                    if index == len(data) - 1:
                        f.write('\n')

        each(_list_texts)

    print('保存完成。', flush=True)


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,list) or isinstance(variate,tuple):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def get_stime():
    import datetime

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return time_now


def get_litetime():
    import datetime

    time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    return time_now


if __name__ == "__main__":
    res = ([1, 2, 3, 4, 5], [11, 46,
                             87], [125232], [5667, 2356, 26, 6215, 9741, 23525])
    res2 = [
        'and', 'B', ['not', 'A'], [1, 2, 1, [2, 1], [1, 1, [2, 2, 1]]],
        ['not', 'A', 'A'], ['or', 'A', 'B', 'A'], 'B'
    ]
    savefile('d:/1.txt', res2)
    # for i in flatten(12141.98792):
    #   print(i)
