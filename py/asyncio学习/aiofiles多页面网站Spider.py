# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 21:44:49
@LastEditors: Even.Sand
@LastEditTime: 2020-03-02 21:44:50
'''
from aspider import AttrField, TextField, Item, Spider
import aiofiles


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
