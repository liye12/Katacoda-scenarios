## 主函数测试
```
if __name__ == '__main__':

    # step 1 读取停用词，构建停用词set集合
    stop_words = []
    with open('stopword.txt', encoding='utf-8') as f:  # 读取stop_words.txt，每行为一个词
        line = f.readline()  # 按行读取
        while line:
            stop_words.append(line[:-1])  # 去除每行后面的换行符并添加到stop_words中
            line = f.readline()
    stop_words = set(stop_words)  # 通过set函数去除重复词
    print('停用词读取完毕，共{n}个单词'.format(n=len(stop_words)))

    # step2 读取文本，预处理，分词，得到词典
    all_word_list = []  # 用于记录所有的词，即词典
    sentence_list = []  # 用于记录所有样本的样本list,如：[["今天","天气","不错"],["我","是","谁"],...,["","",""]]
    line_sum = 1
    with open('corpus.txt', encoding='utf-8') as f:
        line = f.readline()  # 按行读取
        while line:  # 判断有没有读取到文件末尾，没有就执行循环语句
            print("正在处理第", line_sum, "行")
            while '\n' in line:
                line = line.replace('\n', '')  # 将'\n'替换为''
            while ' ' in line:
                line = line.replace(' ', '')  # 将' '替换为''
            if len(line) > 0:  # 如果句子非空
                raw_words = list(jieba.cut(line, cut_all=False))  # 使用jieba分词
                dealed_words = []  # 用于记录去除停用词以及规定词后的词
                for word in raw_words:
                    # 如果词不属于停用词且不是['qingkan520', 'www', 'com', 'http']中的词
                    if word not in stop_words and word not in ['qingkan520', 'www', 'com', 'http']:
                        all_word_list.append(word)  # 将该词添加到样本的词list中
                        dealed_words.append(word)  # 将该词添加到处理后的词list中
                sentence_list.append(dealed_words)  # 每行为一个样本，并将处理过的词list添加到样本list
            line = f.readline()  # 读取下一行
            line_sum += 1
    word_count = collections.Counter(all_word_list)  # 计数器，返回dict类型，{"单词1":15,"单词2":5,"单词3":2}
    # 表示单词1出现了15次，单词2出现了5次，单词3出现了2次，依次类推
    print('文本中总共有{n1}个单词,不重复单词数{n2},选取前30000个单词进入词典'
          .format(n1=len(all_word_list), n2=len(word_count)))
    word_count = word_count.most_common(30000)  # 返回一个TopN列表，如：[("单词1",15),("单词2",5),("单词3",2)]
    word_list = [x[0] for x in word_count]  # 取出TopN列表中的单词，放到word_list中，构成["单词1","单词2","单词3"]
    print(word_list[:100])
    # 创建模型，训练
    w2v = word2vec(vocab_list=word_list,  # 词典集
                   embedding_size=200,  # 词向量的维度
                   win_len=2,  # 窗口大小
                   learning_rate=1,  # 学习率
                   num_sampled=100,  # 负采样个数
                   logdir='/tmp/280')  # tensorboard记录地址

    num_steps = 10000  # 训练次数
    for i in range(num_steps):
        # print (i%len(sentence_list))
        sent = sentence_list[i % len(sentence_list)]
        # 如果len(sentence_list) <  num_steps,会有重复训练的行，如num_steps=20，len(sentence_list)=10
        # 0 % 10 = 0，1 % 10 = 1，...,10 % 10 = 0，11 % 10 = 1，12 % 10 = 2...
        # 这样有些就被训练多次了
        w2v.train_by_sentence([sent])  # 按行训练模型，我们认为一行代表一个样本
    w2v.save_model('model')  # 保存模型，加训练好的模型参数保存

    w2v.load_model('model')  # 加载模型，得到保存的模型参数

    # 测试
    test_word = ["广东省", "珠三角"]
    test_id = [word_list.index(x) for x in test_word]  # 测试单词在词典word_list中的索引，即为单词id
    test_words, near_words, sim_mean, sim_var = w2v.cal_similarity(test_id)  # 计算相似度
    print(test_words, near_words, sim_mean, sim_var)
```{{execute}}

## 点击ESC 推出vim编辑模型
保存并退出vim,输入以下命令 
:wq

## 运行python文件

`python3 word2vec`{{execute}}