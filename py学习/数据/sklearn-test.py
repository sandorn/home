# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-24 00:58:49
LastEditTime : 2022-12-24 00:59:10
FilePath     : /py学习/数据/sklearn-test.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import matplotlib.pyplot as plt
from sklearn import datasets

iris = datasets.load_iris()
features = iris.data
target = iris.target
print(features.shape, target.shape)
print(iris.feature_names)

boston = datasets.load_boston()
boston_features = boston.data
boston_target = boston.target
print(boston_features.shape, boston_target.shape)
print(boston.feature_names)

digits = datasets.load_digits()
digits_features = digits.data
digits_target = digits.target
print(digits_features.shape, digits_target.shape)

img = datasets.load_sample_image('flower.jpg')
print(img.shape)
plt.imshow(img)
plt.show()

data, target = datasets.make_blobs(n_samples=1000, n_features=2, centers=4, cluster_std=1)
plt.scatter(data[:, 0], data[:, 1], c=target)
plt.show()

data, target = datasets.make_classification(n_classes=4, n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1)
print(data.shape)
plt.scatter(data[:, 0], data[:, 1], c=target)
plt.show()

x, y = datasets.make_regression(n_samples=10, n_features=1, n_targets=1, noise=1.5, random_state=1)
print(x.shape, y.shape)
plt.scatter(x, y)
plt.show()
