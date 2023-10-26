# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:19
LastEditTime : 2023-10-26 16:47:01
FilePath     : /CODE/xjLib/xt_Ls_Bqg.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from xt_Ahttp import ahttpGet
from xt_Requests import get_tretry
from xt_Response import htmlResponse
from xt_String import Re_Sub, Str_Clean, Str_Replace


def clean_Content(in_str):
    """清洗内容"""
    clean_list = [
        "', '",
        "&nbsp;",
        ";[笔趣看  www.biqukan.com]",
        "www.biqukan.com。",
        "wap.biqukan.com",
        "www.biqukan.com",
        "m.biqukan.com",
        "n.biqukan.com",
        "www.biqukan8.cc。",
        "www.biqukan8.cc",
        "m.biqukan8.cc。",
        "m.biqukan8.cc",
        "百度搜索“笔趣看小说网”手机阅读:",
        "百度搜索“笔趣看小说网”手机阅读：",
        "请记住本书首发域名:",
        "请记住本书首发域名：",
        "笔趣阁手机版阅读网址:",
        "笔趣阁手机版阅读网址：",
        "关注公众号：书友大本营  关注即送现金、点币！",
        ";[笔趣看  ]",
        "[笔趣看 ]",
        "[笔趣看\xa0\xa0]",
        "<br />",
        "\t",
    ]
    # clean_list += Invisible_Chars # 不可见字符
    # 格式化html string, 去掉多余的字符，类，script等。
    #(r"<([a-z][a-z0-9]*) [^>]*>", r'<\g<1>>'),
    #(r"<\s*script[^>]*>[^<]*<\s*/\s*script\s*>", ''),
    #(r"</?a.*?>", ''),
    sub_list = [
        (r"\(https:///[0-9]{0,4}_[0-9]{0,12}/[0-9]{0,16}.html\)", ''),
        (r'\[.*?\]|http.*?\s*\(.*?\)|\s*www.*?\s*\..*?\s*\..*?\s*\..*?', ''),
    ]
    repl_list = [
        ("\u3000", "  "),
        ("\xa0", " "),
        ("\u0009", " "),
        ("\u000B", " "),
        ("\u000C", " "),
        ("\u0020", " "),
        ("\u00a0", " "),
        ("\uFFFF", " "),
        ("\u000A", "\n"),
        ("\u000D", "\n"),
        ("\u2028", "\n"),
        ("\u2029", "\n"),
        ("\r", "\n"),
        ("    ", "\n    "),
        ("\r\n", "\n"),
        ("\n\n", "\n"),
    ]

    # 如果输入是列表或元组，则将其连接为一个字符串
    if isinstance(in_str, (list, tuple)):
        in_str = "\n".join([item.strip("\r\n\u3000\xa0  ") for item in in_str])
    # 剥离字符串两端的空白字符和换行符
    in_str = in_str.strip("\r\n ")

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
        if resp is None:
            continue
        _xpath = (
            "//h1/text()",
            '//*[@id="content"]/text()',
        )
        _title, _showtext = resp.xpath(_xpath)
        title = ("".join(_title).replace("\u3000",
                                         " ").replace("\xa0", " ").replace(
                                             "\u00a0", " "))
        content = clean_Content(_showtext)
        # if len(content) < 10: print(resp, '||||||||||||||||||||||||||', resp.text)
        _texts.append([resp.index, title, content])

    _texts.sort(key=lambda x: x[0])
    return _texts


def get_download_url(target):
    resp = get_tretry(target)
    assert isinstance(resp, htmlResponse)
    # #pyquery
    # pr = resp.pyquery('.listmain dl dd:gt(11)').children() # 从第二个dt开始，获取后面所有的兄弟节点
    # pr = res.pyquery('dt').eq(1).nextAll()  # 从第二个dt开始，获取后面所有的兄弟节点
    # bookname = resp.pyquery('h2').text()
    # urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    # titles = [i.text() for i in pr.items()]

    _xpath = (
        # '//meta[@property="og:novel:book_name"]/@content',
        "//h2/text()",
        "//dt[2]/following-sibling::dd/a/@href",
        "//dt[2]/following-sibling::dd/a/text()",
        # '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href',
    )
    bookname, temp_urls, titles = resp.xpath(_xpath)
    bookname = bookname[0]
    urls = ["/".join(target.split("/")[:-2]) + item
            for item in temp_urls]  # 章节链接
    return bookname, urls, titles


def get_biqugse_download_url(target):
    resp = get_tretry(target)
    assert isinstance(resp, htmlResponse)
    _xpath = [
        '//meta[@property="og:title"]//@content',
        "//dt[2]/following-sibling::dd/a/@href",
        "//dt[2]/following-sibling::dd/a/text()",
        # '//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()',
    ]
    bookname, temp_urls, titles = resp.xpath(_xpath)

    bookname = bookname[0]
    baseurl = "/".join(target.split("/")[:-2])
    urls = [baseurl + item for item in temp_urls]  # # 章节链接
    return bookname, urls, titles


def get_contents(index, target):
    resp = get_tretry(target)
    assert isinstance(resp, htmlResponse)

    # #pyquery
    title = resp.pyquery("h1").text()
    content = resp.pyquery("#content").text()

    # _xpath = ('//h1/text()', '//*[@id="content"]/text()')
    # _title, content = resp.xpath(_xpath)

    title = ("".join(Str_Clean("".join(title), ["\u3000", "\xa0", "\u00a0"])))
    content = clean_Content(content).strip()
    return [index, title, content]


def ahttp_get_contents(args):
    index, target = args
    resp = ahttpGet(target)
    assert isinstance(resp, htmlResponse)
    _xpath = [
        "//h1/text()",
        '//*[@id="content"]/text()',
    ]
    title, content = resp.xpath(_xpath)
    title = ("".join(Str_Clean("".join(title), ["\u3000", "\xa0", "\u00a0"])))
    content = clean_Content(content)
    return [index, title, content]


if __name__ == "__main__":
    url = "https://www.biqukan8.cc/0_288/"
    bookname, urls, titles = get_download_url(url)
    print(bookname)
    res = get_contents(1, urls[1])
    print(res)
