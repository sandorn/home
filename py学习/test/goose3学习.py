# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-09 12:47:17
#FilePath     : /py学习/goose3学习.py
#LastEditTime : 2020-06-09 13:32:40
#Github       : https://github.com/sandorn/home
#==============================================================
"""

from goose3 import Goose
from xt_str import Ex_Re_Clean, Ex_Str_Replace

from goose3.text import StopWordsChinese

# 初始化，设置中文分词
# g = Goose({'stopwords_class': StopWordsChinese})

g = Goose({"stopwords_class": StopWordsChinese})

# 文章地址
url = "https://www.biqukan.com/38_38836/497783246.html"
# 获取文章内容
article = g.extract(url="https://www.biqukan.com/38_38836/488979096.html")


temp_list = ["', '", "&nbsp;", r";\[笔趣看  www.biqukan.com\]", r"\(https://www.biqukan.com/[0-9]{1,4}_[0-9]{3,8}/[0-9]{3,14}.html\)", "www.biqukan.com。", "wap.biqukan.com", "www.biqukan.com", "m.biqukan.com", "n.biqukan.com", "百度搜索“笔趣看小说网”手机阅读:", "百度搜索“笔趣看小说网”手机阅读：", "请记住本书首发域名:", "请记住本书首发域名：", "笔趣阁手机版阅读网址:", "笔趣阁手机版阅读网址：", "<br />", r";\[笔趣看  \]", r"\[笔趣看 \]"]
adict = {"<br />": "\n", "\r\r": "\n", "\r": "\n", "    ": "\n    ", "\n\n\n": "\n", "\n\n": "\n", "\n\n": "\n"}

# 显示正文
newtext = Ex_Re_Clean(article.cleaned_text, temp_list)
newtext = Ex_Str_Replace(newtext, adict)


print(article.meta_keywords)
print(newtext)
print(article.infos)


"""
#!处理小说效果不错，但效率偏低
# title  # 第一章 孟川和云青萍_沧元图_玄幻小说_笔趣阁
# meta_keywords  #沧元图, 第一章 孟川和云青萍
# cleaned_text   #正文

for item in article.__dict__:
    print(item, article.__dict__[item])

_title  #@
_cleaned_text  #@
_meta_description
_meta_lang
_meta_favicon
_meta_keywords  #@
_meta_encoding
_canonical_link
_domain
_top_node
_top_image
_tags
_opengraph
_tweets
_movies
_links
_authors
_final_url
_link_hash
_raw_html
_schema
_doc
_raw_doc
_publish_date
_publish_datetime_utc
_additional_data
"""
