#!/usr/bin/env python
# encoding: utf-8
"""
@Desc：使用贝叶斯分类器对测试结果进行分类
"""
import operator
import bayes_classfier
import generate_attires


def main():
    test_datasets = generate_attires.gen_attrs()
    classfier = bayes_classfier.navie_bayes_classifier()
    for data in test_datasets:
        print("特征值：", end='\t')
        print(data)
        print("预测结果：", end='\t')
        res = classfier.get_label(*data)  # 表示多参传入
        print(res)  # 预测属于哪种水果的概率
        print('水果类别：', end='\t')
        # 对后验概率排序，输出概率最大的标签
        print(sorted(res.items(), key=operator.itemgetter(1), reverse=True)[0][0])


if __name__ == '__main__':
    # 表示模块既可以被导入（到 Python shell 或者其他模块中），也可以作为脚本来执行。
    # 当模块被导入时，模块名称是文件名；而当模块作为脚本独立运行时，名称为 __main__。
    # 让模块既可以导入又可以执行

    main()
