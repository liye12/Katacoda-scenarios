#!/usr/bin/env python
# encoding: utf-8
"""
@Desc：产生测试数据集来测试贝叶斯分类器的预测能力
"""
import random


def random_attr(pair):
    # 生成0-1之间的随机数
    return pair[random.randint(0, 1)]


def gen_attrs():
    # 特征值的取值集合
    sets = [('long', 'not_long'), ('sweet', 'not_sweet'), ('yellow', 'not_yellow')]
    test_datasets = []
    for i in range(20):
        # 使用map函数来生成一组特征值
        test_datasets.append(list(map(random_attr, sets)))
    return test_datasets

# print(gen_attrs())
