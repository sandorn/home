fruit1 = 'apples'
fruit2 = 'bananas'
fruit3 = 'pears'
'''要求：
输出字符串’There are apples, bananas, pears on the table’

1. 用+符号拼接
用+拼接字符串如下：'''

str = 'There are' + fruit1 + ',' + fruit2 + ',' + fruit3 + ' on the table'
print(str)
'''该方法效率比较低，不建议使用

2. 用%符号拼接
用%符号拼接方法如下：
'''
str = 'There are %s, %s, %s on the table.' % (fruit1, fruit2, fruit3)
print(str)
#除了用元组的方法，还可以使用字典如下：

str = 'There are %(fruit1)s,%(fruit2)s,%(fruit3)s on the table' % {
    'fruit1': fruit1,
    'fruit2': fruit2,
    'fruit3': fruit3
}
print(str)
#该方法比较通用

#. 用join()方法拼接
#join()`方法拼接如下

temp = ['There are ', fruit1, ',', fruit2, ',', fruit3, ' on the table']
''.join(temp)
print(temp)
#该方法使用与序列操作
'''4. 用format()方法拼接
用format()方法拼接如下:'''

str = 'There are {}, {}, {} on the table'
str.format(fruit1, fruit2, fruit3)
print(str)

#还可以指定参数对应位置：

str = 'There are {2}, {1}, {0} on the table'
str.format(fruit1, fruit2, fruit3)  #fruit1出现在0的位置
print(str)

#同样，也可以使用字典：

str = 'There are {fruit1}, {fruit2}, {fruit3} on the table'
str.format(fruit1=fruit1, fruit2=fruit2, fruit3=fruit3)
print("字典:", str)
'''
5. 用string模块中的Template对象
用string模块中的Template对象如下：'''

from string import Template
str = Template(
    'There are ${fruit1}, ${fruit2}, ${fruit3} on the table')  #此处用的是{}，别搞错了哦
str.substitute(
    fruit1=fruit1, fruit2=fruit2,
    fruit3=fruit3)  #如果缺少参数，或报错如果使用safe_substitute()方法不会
str.safe_substitute(fruit1=fruit1, fruit2=fruit2)
print("string模块中的Template:", str)
#输出'There are apples, bananas, ${fruit3} on the table'