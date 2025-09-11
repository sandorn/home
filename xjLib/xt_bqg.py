# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-14 23:30:19
LastEditTime : 2023-10-27 15:59:02
FilePath     : /CODE/xjLib/xt_bqg.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

from functools import partial

from xt_ahttp import ahttp_get
from xt_requests import get
from xt_response import ACResponse, htmlResponse
from xt_str import format_html_string, re_sub, str_clean


def clean_content(in_str):
    """
    清理文本内容,移除HTML标签、网站信息和多余空白

    参数:
        in_str: 输入文本或文本列表

    返回:
        清理后的文本字符串
    """
    if isinstance(in_str, list):
        in_str = '\n'.join(in_str)

    # 使用xt_str中的format_html_string进行HTML基础清理
    cleaned = format_html_string(in_str)

    # 应用业务特定清理规则
    business_rules = [
        (
            r'(关注公众号：书友大本营  关注即送现金、点币！|『点此报错』|『加入书签』|笔趣阁手机版阅读网址|笔趣阁手机版|请收藏本站|请记住本书首发域名|百度搜索“笔趣看小说网”手机阅读|请收藏本站|笔趣看)[:：][^\s]*',
            '',
        ),  # 移除网站推广信息
        (r'https?://[^\s]+', ''),  # 移除URL链接
        (r'\s+\S*[:：]\S*\s+', ' '),  # 移除中间包含冒号的特殊片段
    ]
    cleaned = re_sub(cleaned, business_rules)

    # 使用str_clean进行最终清理
    # Define strings to be removed
    trims = []
    return str_clean(cleaned, trims)


def resp_handle(resp):
    if not isinstance(resp, (ACResponse, htmlResponse)):
        return [0, resp, '']

    try:
        title = resp.query('h1').text()
        content = resp.query('#chaptercontent').text()
        title = ''.join(str_clean(''.join(title), ['\u3000', '\xa0', '\u00a0']))
        content = clean_content(content).strip()
        return [resp.index, title, content]
    except Exception as e:
        mylog(f'出现错误{e!r}')


def resps_handle(resps):
    """传入的是爬虫数据包的集合"""
    texts = []

    for resp in resps:
        if not isinstance(resp, (ACResponse, htmlResponse)):
            continue
        else:
            texts.append(resp_handle(resp))

    texts.sort(key=lambda x: x[0])
    # texts = sorted(texts, key=lambda x: x[0])
    return texts


def get_download_url(url):
    resp = get(url)
    xpath_list = (
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
    bookname, temp_urls, temp_urls2, titles, titles2 = resp.xpath(xpath_list)
    titles += titles2
    temp_urls += temp_urls2
    bookname = ''.join(bookname)
    # urls = ["/".join(url.split("/")[:-3]) + item for item in temp_urls]  # 章节链接
    urls = [f"{url}{''.join(item.split('/')[-1:])}" for item in temp_urls]  # 章节链接
    return bookname, urls, titles


def get_contents(*args, fn=get):
    index, url = args[0:2]
    resp = fn(url, *args[2:])

    if not isinstance(resp, (ACResponse, htmlResponse)):
        return [0, resp, '']

    # pyquery
    title = resp.query('h1').text()
    content = resp.query('#chaptercontent').text()
    # _xpath = ['//h1/text()', '//*[@id="chaptercontent"]/text()']
    # title, content = resp.xpath(_xpath)

    title = ''.join(str_clean(''.join(title), ['\u3000', '\xa0', '\u00a0']))
    content = clean_content(content).strip()

    return [index, title, content]


ahttp_get_contents = partial(get_contents, fn=ahttp_get)


if __name__ == '__main__':
    from xt_wraps import LogCls

    mylog = LogCls()

    # url = "https://www.bigee.cc/book/6909/"
    # bookname, urls, titles = get_download_url(url)
    # mylog(bookname, urls, titles)
    # res = get_contents(0, urls[0])
    # mylog(res)
    def test_clean_content():
        """测试clean_Content函数"""
        test_cases = [
            ('正常文本', 'Hello World'),
            (
                '带HTML标签',
                '<p>Hello<br/>World</p>',
            ),
            ('带特殊字符', 'Hello\u3000World\xa0!\u2029'),
            (
                '带网站信息',
                'Hello 百度搜索“笔趣看小说网”手机阅读:   请收藏本站：https://www.bigee.com World  \n 请收藏本站：',
            ),
            ('多行文本', ['Line1', 'Line2\t', 'Line3  ']),
        ]

        mylog('=== 开始测试 clean_Content ===')
        for name, input_text in test_cases:
            result = clean_content(input_text)
            mylog(f'{name}: ')
            mylog(f'  输入: {input_text!r}')
            mylog(f'  输出: {result!r}')

        mylog('=== 测试完成 ===')

    # test_clean_content()

    mylog(
        33333333333333333333,
        resp := get_download_url('https://www.bigee.cc/book/6909/'),
    )
