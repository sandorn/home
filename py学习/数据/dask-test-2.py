# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-04 15:41:34
LastEditTime : 2023-01-04 15:41:35
FilePath     : /py学习/数据/dask-test-2.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import dask.array as da

x = da.random.uniform(
    low=0,
    high=10,
    size=(10000, 10000),  # normal numpy code
    chunks=(1000, 1000))  # break into chunks of size 1000x1000

y = x + x.T - x.mean(axis=0)  # Use normal syntax for high level algorithms

# DataFrames
import dask.dataframe as dd

df = dd.read_csv(
    '2018-*-*.csv',
    parse_dates='timestamp',  # normal Pandas code
    blocksize=64000000)  # break text into 64MB chunks

s = df.groupby('name').balance.mean()  # Use normal syntax for high level algorithms

# Bags / lists
import dask.bag as db

b = db.read_text('*.json').map(json.loads)
total = (b.filter(lambda d: d['name'] == 'Alice').map(lambda d: d['balance']).sum())
