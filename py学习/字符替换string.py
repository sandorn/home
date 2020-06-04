# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-11 12:56:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-11 13:15:34
'''
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile

text = '''
咔嚓嚓一阵，似有骨头断裂的声响传出，力魔仰面倒飞，杨开的身影也抑制不住地往后倒退十几丈，双脚落下之地，出现一个个深坑，地面以脚印为中心朝四周裂开。

血魔一怔之下，杨开已然杀到，苍龙枪中传出龙吟之声，摄人心神，人面如玉枪如龙，直朝血魔捣去。
圣的气息，那气息起伏不定，好似受到了什么惊吓一般，煌煌逃窜如丧家之犬。

杨开冲他咧嘴一笑：“丧家之犬的哀嚎真是难听！”

杨开知她心中所想，缓缓摇头道：“中计了，这不是他本体，也不知道是不是法身之类的存在。”

这个与自己出身同一个故土的小子，成长的度真是惊人至极。

大乱之世，必是妖孽丛生之时，眼前这个，可以说是妖孽中的妖孽了。




“可有什么收获？”

“有一点，但是跟我们想的不一样。”杨开眉头紧皱。



在小玄界之中，'那力魔如何能够反抗？杨开以世界之主的力量压迫，倒确实问出来一点东西。
'''

txt = Ex_Re_Sub(
    text,
    {
        "'": '',
        ' ': ' ',
        '\xa0': ' ',
        # '\x0a': '\n',  #!错误所在，可能导致\n\n查找不到
        '[]': '',
        '\r': '\n',
        '\n\n': '\n',

    }
)


print('E' * 10, txt)
