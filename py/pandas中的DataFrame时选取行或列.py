import numpy as np
import pandas
'''
ser = pandas.Series(np.arange(3.))
data = pandas.DataFrame(
    np.arange(16).reshape(4, 4), index=list('abcd'), columns=list('wxyz'))
data['w']  #选择表格中的'w'列，使用类字典属性,返回的是Series类型
data.w  #选择表格中的'w'列，使用点属性,返回的是Series类型
data[['w']]  #选择表格中的'w'列，返回的是DataFrame属性
data[['w', 'z']]  #选择表格中的'w'、'z'列
data[0:2]  #返回第1行到第2行的所有行，前闭后开，包括前不包括后
data[1:2]  #返回第2行，从0计，返回的是单行，通过有前后值的索引形式，
#如果采用data[1]则报错
data.[1:2]  #返回第2行的第三种方法，返回的是DataFrame，跟data[1:2]同
data['a':'b']  #利用index值进行切片，返回的是**前闭后闭**的DataFrame,,即末端是包含的
data.irow(0)  #取data的第一行
data.icol(0)  #取data的第一列
data.head( ) #返回data的前几行数据，默认为前五行，需要前十行则dta.head(10)
data.tail( ) #返回data的后几行数据，默认为后五行，需要后十行则data.tail(10)
ser.iget_value(0)  #选取ser序列中的第一个
ser.iget_value(-1)  #选取ser序列中的最后一个，这种轴索引包含索引器的series不能采用ser[-1]去获取最后一个，这回引起歧义。
data.iloc[-1]  #选取DataFrame最后一行，返回的是Series
data.iloc[-1:]  #选取DataFrame最后一行，返回的是DataFrame
data.loc['a', ['w', 'x']]  #返回‘a’行'w'、'x'列，这种用于选取行索引列索引已知
data.iat[1, 1]  #选取第二行第二列，用于已知行、列位置的选取。'''

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

data = DataFrame(
    np.arange(15).reshape(3, 5),
    index=['one', 'two', 'three'],
    columns=['a', 'b', 'c', 'd', 'e'])

data
#对列的操作方法有如下几种
#data.icol(0)  #选取第一列
data['a']
data.a
data[['a']]
data.iloc[:, [0, 1, 2]]  #不知道列名只知道列的位置时
data.iloc[1, [0]]  #选择第2行第1列的值
data.iloc[[1, 2], [0]]  #选择第2,3行第1列的值
data.iloc[1:3, [0, 2]]  #选择第2-4行第1、3列的值
data.iloc[1:2, 2:4]  #选择第2-3行，3-5（不包括5）列的值
data.iloc[data.a > 5, 3]
data.iloc[data.b > 6, 3:4]  #选择'b'列中大于6所在的行中的第4列，有点拗口
data.iloc[data.a > 5, 2:4]  #选择'a'列中大于5所在的行中的第3-5（不包括5）列
data.iloc[data.a > 5, [2, 2, 2]]  #选择'a'列中大于5所在的行中的第2列并重复3次
#还可以行数或列数跟行名列名混着用
data.iloc[1:3, ['a', 'e']]
data.iloc['one':'two', [2, 1]]
data.iloc[['one', 'three'], [2, 2]]
data.iloc['one':'three', ['a', 'c']]
data.iloc[['one', 'one'], ['a', 'e', 'd', 'd', 'd']]

#对行的操作有如下几种：
data[1:2]  #（不知道列索引时）选择第2行，不能用data[1]，可以用data.loc[1]
data.irow(1)  #选取第二行
data.iloc[1]  #选择第2行
data['one':'two']  #当用已知的行索引时为前闭后闭区间，这点与切片稍有不同。
data.iloc[1:3]  #选择第2到4行，不包括第4行，即前闭后开区间。
data.iloc[-1:]  #取DataFrame中最后一行，返回的是DataFrame类型
#**注意**这种取法是有使用条件的，只有当行索引不是数字索引时才可以使用，否则可以选用`data[-1:]`--返回DataFrame类型或`data.irow(-1)`--返回Series类型
data[-1:]  #跟上面一样，取DataFrame中最后一行，返回的是DataFrame类型
data.iloc[-1]  #取DataFrame中最后一行，返回的是Series类型，这个一样，行索引不能是数字时才可以使用
data.tail(1)  #返回DataFrame中的最后一行
data.head(1)  #返回DataFrame中的第一行
