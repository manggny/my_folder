# -*- coding: utf-8 -*-
import sys,os
import jieba
import matplotlib.pyplot as plt

## 打开语气词 词表，保存在yuqi_list里
f_yuqi = open('biyuci.txt','r')
yuqi_list = []

for line in f_yuqi:
	a,*_ = line.split('、')
	yuqi_list.append(a)

#print(yuqi_list)

## 打开两篇小说，并对特殊词进行清理处理
raw_content1 = open('yukongchuan.txt',"r",encoding="utf-8").read()    #打开并读取文件，返回字符串
punc1 = list("。，！”“：‘’……?《》——？")     #建立包含中文符号的列表
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
for i in yuqi_list:
	dic1[i] = dic1.get(i, 0)
	dic2[i] = dic2.get(i, 0)

for i in content1_words:
	for j in yuqi_list:
		if i.encode('utf-8') == j.encode('utf-8'):
			#print("!!!")
			dic1[i] = dic1.get(i, 0) + 1
			break
for i in content2_words:
	for j in yuqi_list:
		if i.encode('utf-8') == j.encode('utf-8'):
			#print("!!!")
			dic2[i] = dic2.get(i, 0) + 1
			break

wc1 = list(dic1.items())
wc1.sort(key=lambda x: x[1], reverse=True)#以出现次数为标准排列，从大到小排序
wc2 = list(dic2.items())
wc2.sort(key=lambda x: x[1], reverse=True)#以出现次数为标准排列，从大到小排序
x1 = []
y1 = []
for i in wc1:
	x1.append(i[0])
	y1.append(i[1])

print(x1)
plt.plot(x1,y1,'r',label = 'biyuci')
plt.title("biyuci frequancy of yukongchuan")
plt.xlabel('biyucis')
plt.ylabel('frequancy')
plt.savefig("biyuci frequancy of yukongchuan.png")
plt.close()

x2 = []
y2 = []
for i in wc2:
	x2.append(i[0])
	y2.append(i[1])

print(x2)
plt.plot(x2,y2,'r',label = 'biyuci')
plt.title("biyuci frequancy of xiyouji")
plt.xlabel('biyucis')
plt.ylabel('frequancy')
plt.savefig("biyuci frequancy of xiyouji.png")
plt.close()
