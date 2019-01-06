import jieba

txt = open('西游记.txt', 'r', encoding='UTF-8').read()#打开文件西游记

for i in '，。！？：“”……（）你我他她是没有一什么这为那这':
    txt = txt.replace(i, '')
words = list(jieba.cut(txt))#jieba分词

dic = {}
for i in words:
    if len(i) == 1:
        continue
    else:
        dic[i] = dic.get(i, 0) + 1

wc = list(dic.items())
wc.sort(key=lambda x: x[1], reverse=True)#以出现次数为标准排列，从大到小排序

for i in range(20):
    print(wc[i])