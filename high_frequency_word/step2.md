## 打开vim

`vim high_frequency_word`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 导入库函数
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

## 读取数据
```
def get_content(path):
    with open(path,'r',encoding='gbk',errors='ignore') as f:
        content= ''
        for l in f:
            l=l.split()
            content += str(l)
        return content
```{{execute}}

## 定义高频词统计函数
```
def get_TF(words,topK=10):
    tf_dic={}
    for w in words:
        tf_dic[w]=tf_dic.get(w,0)+1
    return sorted(tf_dic.items(),key=lambda x:x[1],reverse=True)[:topK]
```{{execute}}

## 过滤停用词
```
def stop_words(path):
    with open(path,'r',encoding='utf8',errors='ignore') as f:
        return [l.strip() for l in f]
```{{execute}}

## 主函数
```
def main():
    import glob
    import random
    import jieba
    
    files=glob.glob('./data/news/C000013/*.txt')
    corpus=[get_content(x) for x in files]
    
    sample_inx=random.randint(0,len(corpus))
    split_words=[x for x in jieba.cut(corpus[sample_inx]) if x not in stop_words('./stop_words.utf8')]
    print('样本之一：'+corpus[sample_inx])
    print('样本分词效果：'+'/'.join(split_words))
    print('样本TopK（10）词：'+str(get_TF(split_words)))
```{{execute}}




## 点击ESC 推出vim编辑模型
保存并退出vim,输入以下命令 
:wq


