## 测试
```
text1 = '我要住到明天下午三点'
print(text1, time_extract(text1), sep=':')

text2 = '预定25号的房间'
print(text2, time_extract(text2), sep=':')

text3 = '我要从26号下午4点住到11月2号'
print(text3, time_extract(text3), sep=':')

text4 = '我要预订今天到10的房间'
print(text4, time_extract(text4), sep=':')

text5 = '今天3号呵呵'
print(text5, time_extract(text5), sep=':')


```{{execute}}

## 点击ESC 退出vim编辑模型
保存并退出vim,输入以下命令 
`:wq`{{execute}}

## 运行代码
`python3 Date_Identify`{{execute}}