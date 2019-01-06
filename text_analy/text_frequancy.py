# -*- coding: utf-8 -*-
import numpy as np
import sys,os
import jieba

## 打开语气词 词表，保存在yuqi_list里
f_yuqi = open('yuqici.txt','r')
yuqi_list = []

for line in f_yuqi:
	a,*_ = line.split('、')
	yuqi_list.append(a)

#print(yuqi_list)

## 打开两篇小说，并对特殊词进行清理处理
raw_content1 = open('yukongchuan.txt',"r",encoding="utf-8").read()    #打开并读取文件，返回字符串
punc1 = list("。，！”“：‘’……?《》——？你我他她是没有一什么这为那这")     #建立包含中文符号的列表
raw_content2 = open('xiyouji.txt',"r",encoding="utf-8").read()    #打开并读取文件，返回字符串
j = 0

## 语气词


for i in punc1:#去除字符串中的符号和换行符
	#print(i)
	if j == 0 :
		content1 = raw_content1.replace(i,'')
		content2 = raw_content2.replace(i,'')
		content1 = content1.strip()
		content2 = content2.strip()
	else:
		content1 = content1.replace(i,'')
		content2 = content2.replace(i, '')
		content1 = content1.strip()
		content2 = content2.strip()
	j += 1

lens1 = len(content1) # 求小说长度
lens2 = len(content2)
print('《悟空传》有',lens1,'个汉字')
print('《西游记》有',lens2,'个汉字')

for i in yuqi_list:
	jieba.add_word(i)
content1_words = list(jieba.cut(content1))#jieba分词
content2_words = list(jieba.cut(content2))
#print(content1_words)

dic1 = {}
dic2 = {}
for i in content1_words:
	if len(i) == 1:
		continue
	else:
		dic1[i] = dic1.get(i, 0) + 1

for j in content2_words:
	if len(j) == 1:
		continue
	else:
		dic2[j] = dic2.get(j, 0) + 1

wc1 = list(dic1.items())
wc1.sort(key=lambda x: x[1], reverse=True)#以出现次数为标准排列，从大到小排序

wc2 = list(dic2.items())
wc2.sort(key=lambda x: x[1], reverse=True)#以出现次数为标准排列，从大到小排序

for i in range(10):
	print(wc1[i])
print("------------------------------------")
for i in range(10):
	print(wc2[i])

