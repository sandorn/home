# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:19
LastEditTime : 2023-10-27 15:59:02
FilePath     : /CODE/xjLib/xt_Ls_Bqg.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from functools import partial

from xt_Ahttp import ahttpGet
from xt_Requests import get
from xt_Response import htmlResponse
from xt_String import Re_Sub, Str_Clean, Str_Replace


def clean_Content(in_str):
    """清洗内容"""
    clean_list = [
        "', '",
        '&nbsp;',
        ';[笔趣看  www.biqukan.com]',
        'www.biqukan.com。',
        'wap.biqukan.com',
        'www.biqukan.com',
        'm.biqukan.com',
        'n.biqukan.com',
        'www.biqukan8.cc。',
        'www.biqukan8.cc',
        'm.biqukan8.cc。',
        'm.biqukan8.cc',
        '百度搜索“笔趣看小说网”手机阅读:',
        '百度搜索“笔趣看小说网”手机阅读：',
        '请记住本书首发域名:',
        '请记住本书首发域名：',
        '笔趣阁手机版阅读网址:',
        '笔趣阁手机版阅读网址：',
        '关注公众号：书友大本营  关注即送现金、点币！',
        ';[笔趣看  ]',
        '[笔趣看 ]',
        '[笔趣看\xa0\xa0]',
        '<br />',
        '\t',
    ]
    # clean_list += Invisible_Chars # 不可见字符
    # 格式化html string, 去掉多余的字符，类，script等。
    # (r"<([a-z][a-z0-9]*) [^>]*>", r'<\g<1>>'),
    # (r"<\s*script[^>]*>[^<]*<\s*/\s*script\s*>", ''),
    # (r"</?a.*?>", ''),
    sub_list = [
        (r'\(https:///[0-9]{0,4}_[0-9]{0,12}/[0-9]{0,16}.html\)', ''),
        (r'\[.*?\]|http.*?\s*\(.*?\)|\s*www.*?\s*\..*?\s*\..*?\s*\..*?', ''),
    ]
    repl_list = [
        ('\u3000', '  '),
        ('\xa0', ' '),
        ('\u0009', ' '),
        ('\u000b', ' '),
        ('\u000c', ' '),
        ('\u0020', ' '),
        ('\u00a0', ' '),
        ('\uffff', ' '),
        ('\u000a', '\n'),
        ('\u000d', '\n'),
        ('\u2028', '\n'),
        ('\u2029', '\n'),
        ('\r', '\n'),
        ('    ', '\n    '),
        ('\r\n', '\n'),
        ('\n\n', '\n'),
    ]

    # 如果输入是列表或元组，则将其连接为一个字符串
    if isinstance(in_str, (list, tuple)):
        in_str = '\n'.join([item.strip('\r\n\u3000\xa0  ') for item in in_str])
    # 剥离字符串两端的空白字符和换行符
    in_str = in_str.strip('\r\n ')

    # 使用Str_Clean函数清理字符串
    in_str = Str_Clean(in_str, clean_list)
    # 使用Re_Sub函数替换子字符串
    in_str = Re_Sub(in_str, sub_list)  # type: ignore
    # 使用Str_Replace函数替换字符
    in_str = Str_Replace(in_str, repl_list)

    return in_str


def 结果处理(resps):
    """传入的是爬虫数据包的集合"""
    _texts = []

    for resp in resps:
        if not isinstance(resp, htmlResponse):
            continue
        _xpath = ('//h1/text()', '//*[@id="chaptercontent"]/text()')
        _title, _showtext = resp.xpath(_xpath)
        title = ''.join(_title).replace('\u3000', ' ').replace('\xa0', ' ').replace('\u00a0', ' ')
        content = clean_Content(_showtext)
        _texts.append([resp.index, title, content])

    _texts.sort(key=lambda x: x[0])
    return _texts


def get_download_url(target):
    resp = get(target)
    if not isinstance(resp, htmlResponse):
        return '', '', ''
    # pyquery
    # pr = resp.pyquery('.listmain dl dd:gt(11)').children() # 从第二个dt开始，获取后面所有的兄弟节点
    # pr = res.pyquery('dt').eq(1).nextAll()  # 从第二个dt开始，获取后面所有的兄弟节点
    # bookname = resp.pyquery('h2').text()
    # urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    # titles = [i.text() for i in pr.items()]

    _xpath = (
        # '//meta[@property="og:novel:book_name"]/@content',
        '//h1/text()',
        "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/@href",
        '//dl/span/dd/a/@href',
        "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/text()",
        '//dl/span/dd/a/text()',
        # '//dt[1]/following-sibling::dd/a/@href',
        # '//dt[1]/following-sibling::dd/a/text()',
        # '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href',
    )
    bookname, temp_urls, temp_urls2, titles, titles2 = resp.xpath(_xpath)
    titles += titles2
    temp_urls += temp_urls2
    bookname = bookname[0]
    urls = ['/'.join(target.split('/')[:-3]) + item for item in temp_urls]  # 章节链接
    return bookname, urls, titles


def get_contents(index, target, fn=get):
    resp = fn(target)
    if not isinstance(resp, htmlResponse):
        return [0, resp, '']
    # pyquery
    title = resp.pyquery('h1').text()
    content = resp.pyquery('#chaptercontent').text()
    # _xpath = ['//h1/text()', '//*[@id="chaptercontent"]/text()']
    # title, content = resp.xpath(_xpath)

    title = ''.join(Str_Clean(''.join(title), ['\u3000', '\xa0', '\u00a0']))
    content = clean_Content(content).strip()
    return [index, title, content]


ahttp_get_contents = partial(get_contents, fn=ahttpGet)


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    # 'https://www.biquge11.cc/read/11159/'
    bookname, urls, titles = get_download_url(url)
    # print(bookname, urls, titles)
    res = get_contents(0, urls[0])
    # print(res)
