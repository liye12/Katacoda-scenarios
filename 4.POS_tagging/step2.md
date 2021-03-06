## 打开vim

`vim pos`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 词性配置

```
# -*- coding: utf-8 -*-
import numpy as np

SMOOTHNESS = 1e-8
START = 'start'  # 句始tag
END = 'end'  # 句末tag
NOUN = 'subj'  # 名词
ADV = 'adv'  # 副词
ADJ = 'adj'  # 形容词
```{{execute}}

## 数据预处理
```
corpus = np.array([
    ('我', NOUN), ('很', ADV), ('菜', ADJ), ('。', END),
    ('我', NOUN), ('好', ADV), ('菜', ADJ), ('。', END),
    ('我', NOUN), ('很', ADV), ('好', ADJ), ('。', END),
    ('他', NOUN), ('很', ADV), ('菜', ADJ), ('。', END),
    ('他', NOUN), ('好', ADV), ('菜', ADJ), ('。', END),
    ('他', NOUN), ('很', ADV), ('好', ADJ), ('。', END),
    ('菜', NOUN), ('很', ADV), ('好', ADJ), ('。', END),
    ('我', NOUN), ('菜', ADJ), ('。', END),
    ('我', NOUN), ('好', ADJ), ('。', END),
    ('他', NOUN), ('菜', ADJ), ('。', END),
    ('他', NOUN), ('好', ADJ), ('。', END),
    ('菜', NOUN), ('好', ADJ), ('。', END),
    ('我', NOUN), ('好', ADV), ('好', ADJ), ('。', END),
    ('他', NOUN), ('好', ADV), ('好', ADJ), ('。', END),
], dtype=str)

words = sorted(set(corpus[:, 0]))
tags = sorted(set(corpus[:, 1]))

W = len(words)  # 词汇量
T = len(tags)  # 词性种类数

word2id = {words[i]: i for i in range(W)}
tag2id = {tags[i]: i for i in range(T)}
id2tag = {i: tags[i] for i in range(T)}
```{{execute}}

## 隐马尔科夫模型训练
```
emit_p = np.zeros((T, W)) + SMOOTHNESS  # emission_probability
start_p = np.zeros(T) + SMOOTHNESS  # start_probability
trans_p = np.zeros((T, T)) + SMOOTHNESS  # transition_probability

prev_tag = START  # 前一个tag
for word, tag in corpus:
    wid, tid = word2id[word], tag2id[tag]
    emit_p[tid][wid] += 1
    if prev_tag == START:
        start_p[tid] += 1
    else:
        trans_p[tag2id[prev_tag]][tid] += 1
    prev_tag = START if tag == END else tag  # 句尾判断

# 频数 --> 概率对数
start_p = np.log(start_p / sum(start_p))
for i in range(T):
    emit_p[i] = np.log(emit_p[i] / sum(emit_p[i]))
    trans_p[i] = np.log(trans_p[i] / sum(trans_p[i]))

```{{execute}}

## 请输出你的测试字符串(默认字符串：菜好好。)
```

sentence = "菜好好。" 
```{{execute}}

## 维特比算法
```
obs = [word2id[w] for w in sentence.strip()]  # 观测序列
le = len(obs)  # 序列长度

# 动态规划矩阵
dp = np.zeros((le, T))  # 记录节点最大概率对数
path = np.zeros((le, T), dtype=int)  # 记录上个转移节点

for j in range(T):
	dp[0][j] = start_p[j] + emit_p[j][obs[0]]

for i in range(1, le):
	for j in range(T):
		dp[i][j], path[i][j] = max((dp[i - 1][k] + trans_p[k][j] + emit_p[j][obs[i]], k)for k in range(T))

# 隐序列
states = [np.argmax(dp[le - 1])]
# 从后到前的循环来依次求出每个单词的词性
for i in range(le - 2, -1, -1):
	states.insert(0, path[i + 1][states[0]])

# 打印
for word, tid in zip(sentence, states):
	print(word, id2tag[tid])


```{{execute}}



## 测试

```
x = '菜好好菜'
viterbi(x)
```{{execute}}

