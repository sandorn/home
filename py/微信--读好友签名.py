# coding:utf-8
import itchat
import re

# 先登录
itchat.login()

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
for i in friends:
    # 获取个性签名
    signature = i["Signature"]
print(signature)

tList = []
for i in friends:
    # 获取个性签名
    signature = i["Signature"].strip().replace("span", "").replace(
        "class", "").replace("emoji", "")
    # 正则匹配过滤掉emoji表情，例如emoji1f3c3等
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    #print(signature)
    tList.append(signature)

# 拼接字符串
text = "".join(tList)

# jieba分词
import jieba
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)

# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image

# 这里要选择字体存放路径，这里是Mac的，win的字体在windows／Fonts中
my_wordcloud = WordCloud(
    background_color="white",
    max_words=2000,
    max_font_size=40,
    random_state=42,
    font_path='windows／Fonts/Arial Unicode.ttf').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
'''
# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image

d = os.path.dirname(__file__)
print(d)
filepath = d+ "/" +"wechat.jpg"
print(filepath)
pass
alice_coloring = np.array(Image.open(filepath))
my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                         max_font_size=40, random_state=42,
                         font_path='/Users/sebastian/Library/Fonts/Arial Unicode.ttf')\
    .generate(wl_space_split)

image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

# 保存图片 并发送到手机
filepath2 = d+ "/" +"wechat_cloud.jpg"
my_wordcloud.to_file(filepath2)
itchat.send_image(filepath2, 'filehelper')
'''
