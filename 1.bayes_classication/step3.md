## 打开vim

`vim generate_attires.py`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 产生测试数据集来测试贝叶斯分类器的预测能力
```
#!/usr/bin/env python
# encoding: utf-8

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

```{{execute}}

## 点击ESC 退出vim编辑模型
保存并退出vim,输入以下命令 
`:wq`{{execute}}


## 打开vim

`vim classification`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 测试：使用贝叶斯分类器对测试结果进行分类
```
#!/usr/bin/env python
# encoding: utf-8
import os
import sys
sys.path.append('./')
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

```{{execute}}

## 点击ESC 推出vim编辑模型
保存并退出vim,输入以下命令 
:wq

## 运行代码

`python3 classification`{{execute}}
