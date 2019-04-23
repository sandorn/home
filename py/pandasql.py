#！/usr/bin/env python
#-*-coding:utf-8-*-
'''
__Author__:沂水寒城
功能：pandasql库使用样例
'''

import re
import csv
import pandas as pd
from sklearn.datasets import load_iris
from pandasql import sqldf


def pysqldf(query):
    '''
    使用该函数后可以不再添加locals()参数
    '''
    return sqldf(query, globals())


#pysqldf = lambda q: sqldf(q, globals())


def iris_data_test():
    '''
    iris数据实验
    '''
    iris = load_iris()  #导入数据
    global iris_df
    iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)  #读入数据，形成表

    iris_df.columns = [re.sub("[() ]", "", col) for col in iris_df.columns]  #去除属性名称中的括号和空格
    print('---------------------------------------查看数据描述--------------------------------------')
    print('iris_df')
    print(iris_df)
    print('iris.feature_names')
    print(iris.feature_names)
    print('iris_df.columns')
    print(iris_df.columns)
    print('---------------------------------------------------------------------------------------')
    query1 = "select * from iris_df;"
    query2 = "select sepalwidthcm from iris_df limit 60;"
    print('-------------------------------------------全局查询语句---------------------------------------------')
    print('query1查询结果：')
    print(pysqldf(query1))
    print('query2查询结果：')
    print(pysqldf(query2))

    query3 = "select * from iris_df where sepalwidthcm>4.2;"
    print('----------------------------------------query3------------------------------------------------')
    print(query3)
    print('query3查询结果：')
    print(pysqldf(query3))

    query4 = "select * from iris_df where petallengthcm*petalwidthcm>0.2 and sepallengthcm*sepalwidthcm>20;"
    print('----------------------------------------query4------------------------------------------------')
    print(query4)
    print('query3查询结果：')
    print(pysqldf(query4))


def random_data_test():
    '''
    使用随机数据测试
    '''
    data_matrix = [['zhaoliang', '180', '160', 'pingpang', 'banana', 'Kobe', '3.4'],
                   ['wangliang', '190', '180', 'tennis', 'apple', 'James', '3.1'],
                   ['liliang', '165', '150', 'football', 'strawberry', 'James', '3.3'],
                   ['danliang', '175', '150', 'basketball', 'orange', 'Kobe', '3.5'],
                   ['chengliang', '186', '145', 'swim', 'banana', 'Beke', '2.9'],
                   ['lvliang', '186', '178', 'run', 'monkey', 'Ouwen', '3.0'],
                   ['xinliang', '166', '150', 'jump', 'li', 'paul', '3.1']]
    feature_names = ['xm', 'sg', 'tz', 'ah', 'acsg', 'xhmx', 'km']
    global random_df
    random_df = pd.DataFrame(data_matrix, columns=feature_names)
    print('random_df')
    print(random_df)
    query1 = "select * from random_df where km>3;"
    print('----------------------------------------query1------------------------------------------------')
    print(query1)
    print('query1查询结果：')
    print(pysqldf(query1))

    query2 = "select a.xm, a.xhmx, b.xm, b.xhmx from random_df a left outer join random_df b on a.sg=b.sg;"
    print('----------------------------------------query2------------------------------------------------')
    print(query2)
    print('query2查询结果：')
    print(pysqldf(query2))

    query3 = "select a.xm, b.xm from random_df a left outer join random_df b on a.km=b.km;"
    print('----------------------------------------query3------------------------------------------------')
    print(query3)
    print('查询结果：')
    print(pysqldf(query3))

    query4 = "select xm, sg, ah, km from random_df where tz>150;"
    print('----------------------------------------query4------------------------------------------------')
    print(query4)
    print('query4查询结果前3条记录：')
    print(pysqldf(query4).head(3))


if __name__ == '__main__':
    iris_data_test()
    print('*-' * 80)
    random_data_test()