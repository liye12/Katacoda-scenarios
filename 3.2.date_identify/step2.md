## 打开vim

`vim Date_Identify`{{execute}}

## 进入编辑模式

`i`{{execute}}

## 导入库

```
# -*- coding: utf-8 -*-
import re
from datetime import datetime,timedelta
from dateutil.parser import parse
import jieba.posseg as psg
```{{execute}}


## 数字unit


```
UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}
```{{execute}}

## 对句子进行解析，提取其中所有可能表示日期时间的词，并进行上下文拼接

```
def time_extract(text):
    time_res=[]
    word=''
    keyDate={'今天':0,'明天':1,'后天':2}
    for k,v in psg.cut(text):
        if k in keyDate:
            if word!='':
                time_res.append(word)
                word=(datetime.today()+timedelta(days=keyDate.get(k,0))).strftime('%Y年%m月%d日')   #对日期进行转化为年月日的形式
        elif word!='':
            if v in ['m','t']:   #如果word不为空且v为时间、数字标签
                word=word+k
            else:
                time_res.append(word)
                word=''
        elif v in ['m','t']:    #如果word为空且v为时间、数字标签
            word=k
    if word !='':
        time_res.append(word)
    result=list(filter(lambda x:x is not None, [check_time_valid(w) for w in time_res]))  #对提取出的日期进行有效性判断
    final_res=[parse_datetime(w) for w in result]   #对文本日期串进行时间转换
    return [x for x in final_res if x is not None]
```{{execute}}

## 对获得的日期进行有效性判断
```
def check_time_valid(word):
    m=re.match("%d+$",word)
    if m:
        if len(word)<=6:
            return None
    wordl=re.sub('[号|日]\d+$','日',word)
    if wordl !=word:
        return check_time_valid(wordl)
    else:
        return wordl
```{{execute}}

## 对提取的文本日期串进行时间转换
```
def parse_datetime(msg):
    if msg is None or len(msg) == 0:
        return None

    try:
        dt = parse(msg, fuzzy=True)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        m = re.match(
            r"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上中下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:\.时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?",
            msg)
        if m.group(0) is not None:
            res = {
                "year": m.group(1),
                "month": m.group(2),
                "day": m.group(3),
                "hour": m.group(5) if m.group(5) is not None else '00',
                "minute": m.group(6) if m.group(6) is not None else '00',
                "second": m.group(7) if m.group(7) is not None else '00',
            }
            params = {}

            for name in res:
                if res[name] is not None and len(res[name]) != 0:
                    tmp = None
                    if name == 'year':
                        tmp = year2dig(res[name][:-1])
                    else:
                        tmp = cn2dig(res[name][:-1])
                    if tmp is not None:
                        params[name] = int(tmp)
            target_date = datetime.today().replace(**params)
            is_pm = m.group(4)
            if is_pm is not None:
                if is_pm == u'下午' or is_pm == u'晚上' or is_pm =='中午':
                    hour = target_date.time().hour
                    if hour < 12:
                        target_date = target_date.replace(hour=hour + 12)
            return target_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None
```{{execute}}

## 文本转换数字
```
def cn2dig(src):
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return rsl
	
def year2dig(year):
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    m = re.match("\d+", res)
    if m:
        if len(m.group(0)) == 2:
            return int(datetime.datetime.today().year/100)*100 + int(m.group(0))
        else:
            return int(m.group(0))
    else:
        return None
		
```{{execute}}
