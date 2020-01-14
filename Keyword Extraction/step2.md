## 打开vim

`vim Keyword_Extraction`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 导入库

```
import math
import jieba
import jieba.posseg as psg
from gensim import corpora,models
from jieba import analyse
import functools
```{{execute}}


## 加载停用词表


```
def get_stopword_list():
    stop_word_path='./stopword.txt'    #停用词所在的路径
    stopword_list=[sw.replace('\n','') for sw in open(stop_word_path,encoding='utf8').readlines()]  #获取其中的停用词
    return stopword_list
```{{execute}}

## 定义分词方法
pos为是否只保留名词的依据

```
def get_stopword_list():
    stop_word_path='./stopword.txt'    #停用词所在的路径
    stopword_list=[sw.replace('\n','') for sw in open(stop_word_path,encoding='utf8').readlines()]  #获取其中的停用词
    return stopword_list
```{{execute}}

## 定义干扰词过滤方法
```
def word_filter(seg_list,pos=False):
    stopword_list=get_stopword_list()    #获得停用词
    filter_list=[]    #存储过滤后的词
    
    #根据pos确定是否进行此行过滤
    ####不进行此行过滤则都标记为n并保留
    for seg in seg_list:
        if not pos:
            word=seg
            flag='n'
        else:
            word=seg.word
            flag=seg.flag
        if not flag.startswith('n'):
            continue
        #过滤停用词中词以及长度<2的
        if  not word in stopword_list and len(word)>1:
            filter_list.append(word)
    
    return filter_list
```{{execute}}

## 加载数据集
```
def load_data(pos=False,corpus_path='./corpus.txt'):
    #对数据进行预处理
    doc_list=[]
    for line in open(corpus_path,'r',encoding='utf8'):
        content=line.strip()
        seg_list=seg_to_list(content,pos)      #对句子进行分词
        filter_list=word_filter(seg_list,pos)  #对分词结果过滤干扰词
        doc_list.append(filter_list)
    return doc_list
```{{execute}}


## TopK关键词
```
def cmp(e1,e2):
    import numpy as np
    res=np.sign(e1[1]-e2[1])
    if res!=0:
        return res
    else:
        a=e1[0]+e2[0]
        b=e2[0]+e1[0]
        if a>b:
            return 1
        elif a==b:
            return 0
        else:
            return -1
```{{execute}}

## idf统计方法

```
def train_idf(doc_list):
    idf_dic={}
    #文档总数
    tt_count=len(doc_list)
    #每个词出现的文档数
    for doc in doc_list:
        for word in set(doc):
            idf_dic[word]=idf_dic.get(word,0.0)+1.0
    
    #按工时转化为idf值，分母加1进行平滑处理
    for k,v in idf_dic.items():
        idf_dic[k]=math.log(tt_count/(1.0+v))
        
    #对没有出现的次，默认出现1次
    default_idf=math.log(tt_count/(1.0))
    return idf_dic,default_idf
```{{execute}}

## 定义TF-IDF类

```
class TfIdf(object):
    ###参数为：训练好的idf字典，默认的idf值，处理后的待提取样本，关键词数量
    def __init__(self,idf_dic,default_idf,word_list,keyword_num):
        self.word_list=word_list
        self.idf_dic,self.default_idf=idf_dic,default_idf
        self.tf_dic=self.get_tf_dic()   #TF数据
        self.keyword_num=keyword_num
    
    #统计tf值
    def get_tf_dic(self):
        tf_dic={}
        for word in self.word_list:
            tf_dic[word]=tf_dic.get(word,0.0)+1.0
            
        tt_count=len(self.word_list)
        for k,v in tf_dic.items():
            tf_dic[k]=float(v)/tt_count
            
        return tf_dic
    
    #计算tf-idf
    def get_tfidf(self):
        tfidf_dic={}
        for word in self.word_list:
            idf=self.idf_dic.get(word,self.default_idf)
            tf=self.tf_dic.get(word,0)
            
            tfidf=tf*idf
            tfidf_dic[word]=tfidf
        
        #根据tf-idf的排序，取前keyword_num个作为关键词
        for k,v in sorted(tfidf_dic.items(),key=functools.cmp_to_key(cmp),reverse=True)[:self.keyword_num]:
            print(k+"/",end='')
        print()
```{{execute}}

## 主题模型的类


```

class TopicModel(object):
    ###参数：处理后的数据集、关键词数量、具体模型（LSI、LDA）、主题数量
    def __init__(self,doc_list,keyword_num,model='LSI',num_topics=4):
        #使用gensim接口将文本转化为向量表示
        ##构建词空间
        self.dictionary=corpora.Dictionary(doc_list)
        ##使用BOW模型向量化
        corpus=[self.dictionary.doc2bow(doc) for doc in doc_list]
        ##对每个词根据tf-idf进行加权
        self.tfidf_model=models.TfidfModel(corpus)
        self.corpus_tfidf=self.tfidf_model[corpus]
        
        self.keyword_num=keyword_num
        self.num_topics=num_topics
        
        #选择加载的模型
        if model=='LSI':
            self.model=self.train_lsi()
        else:
            self.model=self.train_lda()
        
        #得到数据集的主题--词分布
        word_dic=self.word_dictionary(doc_list)
        self.wordtopic_dic=self.get_wordtopic(word_dic)
    
    ###训练LSI
    def train_lsi(self):
        lsi=models.LsiModel(self.corpus_tfidf,id2word=self.dictionary,num_topics=self.num_topics)
        return lsi
    
    ###训练LDA
    def train_lda(self):
        lda=models.LdaModel(self.corpus_tfidf,id2word=self.dictionary,num_topics=self.num_topics)
        return lda
    
    def get_wordtopic(self,word_dic):
        wordtopic_dic={}
        
        for word in word_dic:
            single_list=[word]
            wordcorpus=self.tfidf_model[self.dictionary.doc2bow(single_list)]
            wordtopic=self.model[wordcorpus]
            wordtopic_dic[word]=wordtopic
        return wordtopic_dic
    
    #计算词的分布与文本的相似度，取最高的几个作为关键词
    def get_simword(self,word_list):
        sentcorpus=self.tfidf_model[self.dictionary.doc2bow(word_list)]
        senttopic=self.model[sentcorpus]
        ##余弦相似度计算
        def calsim(l1,l2):
            a,b,c=0.0,0.0,0.0
            for t1,t2 in zip(l1,l2):
                x1=t1[1]
                x2=t2[1]
                a+=x1*x1
                b+=x1*x1
                c+=x2*x2
            sim=a/math.sqrt(b*c) if not (b*c)==0.0 else 0.0
            return sim
        
        # 计算输入文本和每个词的主题分布相似度
        sim_dic = {}
        for k, v in self.wordtopic_dic.items():
            if k not in word_list:
                continue
            sim = calsim(v, senttopic)
            sim_dic[k] = sim

        for k, v in sorted(sim_dic.items(), key=functools.cmp_to_key(cmp), reverse=True)[:self.keyword_num]:
            print(k + "/ ", end='')
        print()

    # 词空间构建方法和向量化方法，在没有gensim接口时的一般处理方法
    def word_dictionary(self, doc_list):
        dictionary = []
        for doc in doc_list:
            dictionary.extend(doc)

        dictionary = list(set(dictionary))

        return dictionary

    def doc2bowvec(self, word_list):
        vec_list = [1 if word in word_list else 0 for word in self.dictionary]
        return vec_list

```{{execute}}

## 调用各提取模型

```
def tfidf_extract(word_list, pos=False, keyword_num=10):
    doc_list = load_data(pos)
    idf_dic, default_idf = train_idf(doc_list)
    tfidf_model = TfIdf(idf_dic, default_idf, word_list, keyword_num)
    tfidf_model.get_tfidf()


def textrank_extract(text, pos=False, keyword_num=10):
    textrank = analyse.textrank
    keywords = textrank(text, keyword_num)
    # 输出抽取出的关键词
    for keyword in keywords:
        print(keyword + "/ ", end='')
    print()


def topic_extract(word_list, model, pos=False, keyword_num=10):
    doc_list = load_data(pos)
    topic_model = TopicModel(doc_list, keyword_num, model=model)
    topic_model.get_simword(word_list)
```{{execute}}



