# -*- coding:utf-8 -*-
import xJlib as x

list_1=[]
#1.使用append()函数，向列表中追加数据,会把添加的数据放在列表的最后
#object：对象，要添加到列表中的数据
list_1.append('2018-1-23')
print("list_1:【",list_1,"】是{}".format(x.getType(list_1)) )
#2.使用insert(index,object) 函数，向列表中插入一条数据
# index 索引 object 要插入的数据 如果超出最大索引，会将数据放在列表最后。若index为负值，位置会从后向前查找，最后一条数据索引为-1
list_1.insert(4,'oppo')
print("list_1:【",list_1,"】是{}".format(x.getType(list_1)) )
#3.使用extend()函数，可以将一个可迭代对象的所有数据追加到该列表中
#extend(iterable)
#可迭代对象   例如： 列表 字符串 字典 元组
list_2 =['a','b','c','e','f']
list_1.extend(list_2)
print("list_2:【",list_2,"】是{}".format(x.getType(list_2)) )
print("list_1:【",list_1,"】是{}".format(x.getType(list_1)) )

#index()函数 可以根据数据，查找数据的索引
#1.数据 2. 开始搜索的位置3.结束搜索的位置
#如果数据不在列表中（或不在指定范围），会出现异常错误
# 'hello' is not in list 原因1：列表中确实没有该元素 原因2：指定的范围没有该元素
index = list_1.index('oppo',0,5)
print(index)
list_1[3] = True
print(list_1)
#根据索引修改数据
list_1[index] = 'vivo'
print(list_1)
