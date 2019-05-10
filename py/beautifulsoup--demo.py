html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
from bs4 import BeautifulSoup
# 获取所有a标签节点内容
c_showurl_bf = BeautifulSoup(html_doc)
c_showurl = c_showurl_bf.find_all('a')

#查找已经获取a标签节点中所有连接
for link in c_showurl:
    print(link.name, link['href'], link.get_text())
