## 打开vim

`vim pcfg`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 导入库

```
# -*- coding: utf-8 -*-
import jieba
from nltk.parse import stanford
import os


```{{execute}}


## jieba分词


```
string='他骑自行车去了菜市场。'
seg_list=jieba.cut(string,cut_all=False,HMM=True)
seg_str=' '.join(seg_list)
print(seg_str)

```{{execute}}

## PCFG句法分析


```
root='./stanford-parser-full-2018-10-17/'
parser_path=root+'stanford-parser.jar'
model_path=root+'stanford-parser-3.9.2-models.jar'

##PCFG模型路径
pcfg_path='edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz'

parser=stanford.StanfordParser(path_to_jar=parser_path,path_to_models_jar=model_path,model_path=pcfg_path)

sentence=parser.raw_parse(seg_str)
for line in sentence:
    print(line)


```{{execute}}