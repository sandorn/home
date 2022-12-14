# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-16 19:45:03
#FilePath     : /xjLib/test/string__doc__.py
#LastEditTime : 2020-06-16 19:45:05
#Github       : https://github.com/sandorn/home
#==============================================================
'''
'''
    #统计一个list中各个元素出现的次数
    #方法1，使用字典
    from random import randint
    data = [randint(1,10) for _ in rang(10)]
    # 把data里的数据作为key来创建一个字典，且value初始化为0
    dic = dict.fromkeys(data, 0)
    for x in data:
    dic[x] += 1
    #dic 中key为元素，value为该元素出现次数

    #方法2，使用Counter()
    from collections import Counter()
    data = [randint(1,10) for _ in range(10)]
    # 得到的dic2和方法1的dic一样，一条代码解决问题！
    dic2 = Counter(data)
    # 并且还可以使用most_common(n)方法来直接统计出出现频率最高的n个元素
    dic2.most_common(2)
    # 输出一个list ,其中的元素为（key,value）的键值对，类似[(6, 4), (3, 2)]这样"

    #对字典排序
    #以上一例子的dic作为排序对象
    dic = {0: 1, 2: 2, 4: 4, 6: 1, 7: 1, -6: 1}
    dic_after = sorted(dic.items(), key=lambda x:x[1])
    # 如果想按key来排序则sorted(dic.items(), key=lambda x:x[0])
    # dic_after为一个列表： [(0, 1), (6, 1), (7, 1), (-6, 1), (2, 2), (4, 4)]

    #正则匹配查找
    import re
    sentence = 'this is a test, not testing.'
    it = re.finditer('\\btest\\b', sentence)
    for match in it:
        print 'match position: ' + str(match.start()) +'-'+ str(match.end())

    #使用正则表达式分割文本
    import re
    s = 'ab,wer.wer,wer|wer||,wwer wer,wer3'
    re.split(r'[,|.]+', s)
    Out[6]: ['ab', 'wer', 'wer', 'wer', 'wer', 'wwer wer', 'wer3']"

    # 分割为所有单词组成的list, W匹配非字母数字及下划线
    import re
    result = re.split('W+', text)


    #使用正则表达式提取文本
    import re
    #用(?P<year>...)括住一个群，并命名为year
    m = re.search('output_(?P<year>d{4})', 'output_1986.txt')
    print(m.group('year') #输出1986


    #正则 调整文本格式
    import re
    s = '1991-02-28'
    re.sub(r'(d{4})-(d{2})-(d{2})', r'\\1/\\2/\\3')
    #Out[6]: '1991/02/28'

    #利用set是一个不同的对象的集合，删除列表中的重复元素。然且维持顺序
    from collections import OrderedDict
    x = [1, 8, 4, 5, 5, 5, 8, 1, 8]
    list(OrderedDict.fromkeys(x))"

    #筛选列表中的数据
    #列表解析
    from random import randint
    data = [randint(-10,10) for _ in range(10)]
    data_after=[x for x in data if x > 0]
    # or
    targetList = [v for v in targetList if not v.strip()=='']
    # or
    targetList = filter(lambda x: len(x)>0, targetList)

    #筛选字典中的数据，字典解析
    from random import randint
    d = {x: randint(60,100) for x in range(1,21)}
    d_after = {k:v for k,v in d.items() if v > 90}

    #使用命名元组为每个元素命名
    from collections import namedtuple
    Student = namedtuple('Student', ['name', 'age', 'sex'])
    s = Student('aaa',18,'male')
    s2= Student(name='bbb', age=12, sex='female')

    if s.name == 'aaa':
        pass
'''
