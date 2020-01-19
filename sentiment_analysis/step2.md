## 打开vim

`vim lstm`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 导入库

```
# -*- coding: utf-8 -*-
from keras.layers.core import Activation, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split
import collections
import nltk
import numpy as np
```{{execute}}



## 数据导入，在开始之前，我们先对所用数据做个初步探索。
## 特别地，我们需要知道数据中有多少个不同的单词，每句话由多少个单词组成。


```
maxlen = 0
word_freqs = collections.Counter()
num_recs = 0
with open('./training.txt','r+',encoding='gbk') as f:
    for line in f:
        label, sentence = line.strip().split("\t")
        words = nltk.word_tokenize(sentence.lower())
        if len(words) > maxlen:
            maxlen = len(words)
        for word in words:
            word_freqs[word] += 1
        num_recs += 1
print('max_len ',maxlen)
print('nb_words ', len(word_freqs))

```{{execute}}


## 输出以后一共有 2324 个不同的单词，包括标点符号。每句话最多包含 42 个单词。
## 根据不同单词的个数(nb_words)，我们可以把词汇表的大小设为一个定值，并且对于不在词汇表里的单词，把它们用伪单词 UNK 代替。 
##根据句子的最大长度 (max_lens)，我们可以统一句子的长度，把短句用 0 填充。依前所述，我们把 VOCABULARY_SIZE 设为 2002。包含训练数据中按词频从大到小排序后的前 2000 个单词，外加一个伪单词 UNK 和填充单词 0。 最大句子长度 MAX_SENTENCE_LENGTH 设为40。

```
MAX_FEATURES = 2000
MAX_SENTENCE_LENGTH = 40
```{{execute}}

## 接下来建立两个lookup tables，分别是 word2index 和 index2word，用于单词和数字转换。
```
vocab_size = min(MAX_FEATURES, len(word_freqs)) + 2
word2index = {x[0]: i+2 for i, x in enumerate(word_freqs.most_common(MAX_FEATURES))}
word2index["PAD"] = 0
word2index["UNK"] = 1
index2word = {v:k for k, v in word2index.items()}
X = np.empty(num_recs,dtype=list)
y = np.zeros(num_recs)
i=0
with open('./training.txt','r+',encoding='gbk') as f:
    for line in f:
        label, sentence = line.strip().split("\t")
        words = nltk.word_tokenize(sentence.lower())
        seqs = []
        for word in words:
            if word in word2index:
                seqs.append(word2index[word])
            else:
                seqs.append(word2index["UNK"])
        X[i] = seqs
        y[i] = int(label)
        i += 1
X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)
```{{execute}}

## 最后是划分数据，80% 作为训练数据，20% 作为测试数据。
```
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2, random_state=42)
```{{execute}}

## 数据准备好后，就可以上模型了。这里损失函数用 binary_crossentropy， 优化方法用 adam。 至于 EMBEDDING_SIZE , HIDDEN_LAYER_SIZE , 以及训练时用到的BATCH_SIZE 和 NUM_EPOCHS 这些超参数，就凭经验多跑几次调优了。
```
EMBEDDING_SIZE = 128
HIDDEN_LAYER_SIZE = 64
BATCH_SIZE = 32
NUM_EPOCHS = 10
model = Sequential()
model.add(Embedding(vocab_size, EMBEDDING_SIZE,input_length=MAX_SENTENCE_LENGTH))
model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss="binary_crossentropy", optimizer="adam",metrics=["accuracy"])
		
```{{execute}}

## 网络构建好后就是上数据训练了。用 10 个 epochs 和 batch_size 取 32 来训练这个网络。在每个 epoch， 我们用测试集当作验证集。
```
model.fit(Xtrain, ytrain, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,validation_data=(Xtest, ytest))
		
```{{execute}}

## 预测结果
```
score, acc = model.evaluate(Xtest, ytest, batch_size=BATCH_SIZE)
print("\nTest score: %.3f, accuracy: %.3f" % (score, acc))
print('{}   {}      {}'.format('预测','真实','句子'))
for i in range(5):
    idx = np.random.randint(len(Xtest))
    xtest = Xtest[idx].reshape(1,40)
    ylabel = ytest[idx]
    ypred = model.predict(xtest)[0][0]
    sent = " ".join([index2word[x] for x in xtest[0] if x != 0])
    print(' {}      {}     {}'.format(int(round(ypred)), int(ylabel), sent))

		
```{{execute}}