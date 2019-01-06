# -*- coding: utf-8 -*-
import sys,os
import jieba
import matplotlib.pyplot as plt

## name_lists

wk_list = ['孙悟空','孙行者','美猴王','齐天大圣','斗战胜佛']
ts_list = ['江流','唐三藏','陈玄奘','金蝉子','旃檀功德佛','唐僧']
zbj_list = ['猪悟能','猪刚鬣','猪八戒','天蓬元帅','净坛使者']
swz_list = ['沙悟净','沙僧','沙和尚','卷帘大将','金身罗汉']
all_list = ['孙悟空','唐僧','猪八戒','沙悟净']
whole_list =wk_list+ts_list+zbj_list+swz_list

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

for i in wk_list:
	jieba.add_word(i)
for i in ts_list:
	jieba.add_word(i)
for i in zbj_list:
	jieba.add_word(i)
for i in swz_list:
	jieba.add_word(i)
content1_words = list(jieba.cut(content1))#jieba分词
content2_words = list(jieba.cut(content2))
#print(content1_words)

dic1 = {}
dic2 = {}
for i in all_list:
	dic1[i] = dic1.get(i, 0)
	dic2[i] = dic2.get(i, 0)


for i in content1_words:
	if i in wk_list:
		dic1['孙悟空'] = dic1.get('孙悟空', 0) + 1
	elif i in ts_list:
		dic1['唐僧'] = dic1.get('唐僧', 0) + 1
	elif i in zbj_list:
		dic1['猪八戒'] = dic1.get('猪八戒', 0) + 1
	elif i in swz_list:
		dic1['沙悟净'] = dic1.get('沙悟净', 0) + 1

for i in content2_words:
	if i in wk_list:
	#	print("!!!")
		dic2['孙悟空'] = dic2.get('孙悟空', 0) + 1
	elif i in ts_list:
		dic2['唐僧'] = dic2.get('唐僧', 0) + 1
	elif i in zbj_list:
		dic2['猪八戒'] = dic2.get('猪八戒', 0) + 1
	elif i in swz_list:
		dic2['沙悟净'] = dic2.get('沙悟净', 0) + 1
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
plt.plot(x1,y1,'r',label = 'name')
plt.title("name frequancy of yukongchuan")
plt.xlabel('name')
plt.ylabel('frequancy')
plt.savefig("name frequancy of yukongchuan.png")
plt.close()

x2 = []
y2 = []
for i in wc2:
	x2.append(i[0])
	y2.append(i[1])

print(x2)
plt.plot(x2,y2,'r',label = 'name')
plt.title("name frequancy of xiyouji")
plt.xlabel('name')
plt.ylabel('frequancy')
plt.savefig("name frequancy of xiyouji.png")
plt.close()
