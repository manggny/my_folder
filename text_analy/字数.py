# -*- coding: utf-8 -*-


#悟空传
contents1 = open('yukongchuan.txt',"r",encoding="utf-8").read()    #打开并读取文件，返回字符串
punc1 = list("。，！”“：‘’……？《》 ")     #建立包含中文符号的列表

for i in punc1:#去除字符串中的符号和换行符
    f1 = contents1.replace(i,'')
    f1 = f1.strip()

lens1 = len(f1)
print('《悟空传》有',lens1,'个汉字')