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

from functools import partial

from xt_ahttp import ahttpGet
from xt_requests import get
from xt_response import ACResponse, htmlResponse
from xt_str import Re_Sub, Str_Clean, Str_Replace
from xt_unicode import AdvancedTextCleaner


def clean_Content(in_str):
    """
    清理文本内容，移除HTML标签、网站信息和多余空白

    参数:
        in_str: 输入文本或文本列表

    返回:
        清理后的文本字符串
    """
    if isinstance(in_str, list):
        in_str = "\n".join(in_str)

    # 使用xt_unicode中的AdvancedTextCleaner进行基础清理
    cleaner = AdvancedTextCleaner()
    cleaned = cleaner.clean_and_normalize(in_str)
    print(111111111111111111111, cleaned)
    sub_rules = [
        (r"<[^>]+>", " "),  # 移除HTML标签
        (
            r"(关注公众号：书友大本营  关注即送现金、点币！|『点此报错』|『加入书签』|笔趣阁手机版阅读网址|笔趣阁手机版|请收藏本站|请记住本书首发域名|百度搜索“笔趣看小说网”手机阅读|请收藏本站|笔趣看)[:：][^\s]*",
            "",
        ),  # 合并网站信息清理规则并移除冒号后内容
        # (r"[;]?\[笔趣看[\s\xa0]*\]", ""),
        (r"", ""),
        (r"https?://[^\s]+", ""),  # 改进URL匹配规则
        (r"\s+", " "),  # 合并连续空格
        (r"^\s+", ""),  # 移除开头的空格
        (r"\s+$", ""),  # 移除结尾的空格
        (r"\s+\S*[:：]\S*\s+", " "),  # 移除中间包含冒号的片段
        ("\u3000", "  "),
        ("\xa0", " "),
        ("\u0009", " "),
        ("\u000b", " "),
        ("\u000c", " "),
        ("\u0020", " "),
        ("\u00a0", " "),
        ("\uffff", " "),
        ("\u000a", " "),
        ("\u000d", " "),
        ("\u2028", " "),
        ("\u2029", " "),
        ("\r", "\n"),
        ("    ", "\n    "),
        ("\r\n", "\n"),
        ("\n\n", "\n"),
    ]
    cleaned = Re_Sub(cleaned, sub_rules)

    # 移除多余空白但保留换行
    cleaned = "\n".join(line.strip() for line in cleaned.split("\n"))

    return cleaned.strip()


def clean_Content0(in_str):
    """清洗内容"""
    clean_list = [
        "', '",
        "&nbsp;",
        ";[笔趣看  www.bigee.com]",
        "https://www.bigee.com。",
        "https://wap.bigee.com",
        "https://www.bigee.com",
        "https://m.bigee.com",
        "https://n.bigee.com",
        "https://www.bigee.cc。",
        "https://www.bigee.cc",
        "https://m.bigee.cc。",
        "https://m.bigee.cc",
        "请收藏本站：",
        "百度搜索“笔趣看小说网”手机阅读:",
        "百度搜索“笔趣看小说网”手机阅读：",
        "请记住本书首发域名:",
        "请记住本书首发域名：",
        "笔趣阁手机版阅读网址:",
        "笔趣阁手机版：",
        "笔趣阁手机版阅读网址：",
        "关注公众号：书友大本营  关注即送现金、点币！",
        "『点此报错』",
        "『加入书签』",
        ";[笔趣看  ]",
        "[笔趣看 ]",
        "[笔趣看\xa0\xa0]",
        "<br />",
        "\t",
    ]
    # clean_list += Invisible_Chars # 不可见字符
    # 格式化html string, 去掉多余的字符，类，script等。
    # (r"<([a-z][a-z0-9]*) [^>]*>", r'<\g<1>>'),
    # (r"<\s*script[^>]*>[^<]*<\s*/\s*script\s*>", ''),
    # (r"</?a.*?>", ''),
    sub_list = [
        (r"<[^>]+>", " "),
        (r"\(https:///[0-9]{0,4}_[0-9]{0,12}/[0-9]{0,16}.html\)", ""),
        (r"\[.*?\]|http.*?\s*\(.*?\)|\s*www.*?\s*\..*?\s*\..*?\s*\..*?", ""),
    ]

    repl_list = [
        ("\u3000", "  "),
        ("\xa0", " "),
        ("\u0009", " "),
        ("\u000b", " "),
        ("\u000c", " "),
        ("\u0020", " "),
        ("\u00a0", " "),
        ("\uffff", " "),
        ("\u000a", " "),
        ("\u000d", " "),
        ("\u2028", " "),
        ("\u2029", " "),
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


def handle_resp(resp):
    if not isinstance(resp, (ACResponse, htmlResponse)):
        return [0, resp, ""]

    try:
        title = resp.query("h1").text()
        content = resp.query("#chaptercontent").text()
        title = "".join(Str_Clean("".join(title), ["\u3000", "\xa0", "\u00a0"]))
        content = clean_Content(content).strip()
        return [resp.index, title, content]
    except Exception as e:
        print(f"出现错误{e!r}")


def 结果处理(resps):
    """传入的是爬虫数据包的集合"""
    texts = []

    for resp in resps:
        if not isinstance(resp, (ACResponse, htmlResponse)):
            continue
        else:
            texts.append(handle_resp(resp))

    texts.sort(key=lambda x: x[0])
    # texts = sorted(texts, key=lambda x: x[0])
    return texts


def get_download_url(url):
    resp = get(url)
    # pyquery
    # pr = resp.pyquery('.listmain dl dd:gt(11)').children() # 从第二个dt开始，获取后面所有的兄弟节点
    # pr = res.pyquery('dt').eq(1).nextAll()  # 从第二个dt开始，获取后面所有的兄弟节点
    # bookname = resp.pyquery('h2').text()
    # urls = [f'https://www.biqukan8.cc{i.attr("href")}' for i in pr.items()]
    # titles = [i.text() for i in pr.items()]

    _xpath = (
        # '//meta[@property="og:novel:book_name"]/@content',
        "//h1/text()",
        "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/@href",
        "//dl/span/dd/a/@href",
        "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/text()",
        "//dl/span/dd/a/text()",
        # '//dt[1]/following-sibling::dd/a/@href',
        # '//dt[1]/following-sibling::dd/a/text()',
        # '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href',
    )
    bookname, temp_urls, temp_urls2, titles, titles2 = resp.xpath(_xpath)
    titles += titles2
    temp_urls += temp_urls2
    bookname = "".join(bookname)
    # urls = ["/".join(url.split("/")[:-3]) + item for item in temp_urls]  # 章节链接
    urls = [f"{url}{''.join(item.split('/')[-1:])}" for item in temp_urls]  # 章节链接
    return bookname, urls, titles


def get_contents(*args, fn=get):
    index, url = args[0:2]
    resp = fn(url, *args[2:])

    if not isinstance(resp, (ACResponse, htmlResponse)):
        return [0, resp, ""]

    # pyquery
    title = resp.query("h1").text()
    content = resp.query("#chaptercontent").text()
    # _xpath = ['//h1/text()', '//*[@id="chaptercontent"]/text()']
    # title, content = resp.xpath(_xpath)

    title = "".join(Str_Clean("".join(title), ["\u3000", "\xa0", "\u00a0"]))
    content = clean_Content(content).strip()

    return [index, title, content]


ahttp_get_contents = partial(get_contents, fn=ahttpGet)


if __name__ == "__main__":
    # url = "https://www.bigee.cc/book/6909/"
    # bookname, urls, titles = get_download_url(url)
    # print(bookname, urls, titles)
    # res = get_contents(0, urls[0])
    # print(res)
    def test_clean_content():
        """测试clean_Content函数"""
        test_cases = [
            ("正常文本", "Hello World"),
            (
                "带HTML标签",
                "<p>Hello<br/>World</p>",
            ),
            ("带特殊字符", "Hello\u3000World\xa0!\u2029"),
            (
                "带网站信息",
                "Hello 百度搜索“笔趣看小说网”手机阅读:   请收藏本站：https://www.bigee.com World  \n 请收藏本站：",
            ),
            ("多行文本", ["Line1", "Line2\t", "Line3  "]),
        ]

        print("=== 开始测试 clean_Content ===")
        for name, input_text in test_cases:
            result = clean_Content(input_text)
            print(f"{name}: ")
            print(f"  输入: {repr(input_text)}")
            print(f"  输出: {repr(result)}")

        print("=== 测试完成 ===")

    test_clean_content()
