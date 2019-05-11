import os,sys,shutil

path = 'F:/zhaopian/fa'
#result = 'F:/zhaopian/all'
filelist = os.listdir(path)

mubiao = ['_45_','_90_','_135_','_180_','_225_','_270_','_315_']

for file in filelist:
	*_,s = file.split('.')
	filen = path + '/' + file
	if s == 'gif':
		os.remove(filen)
		print(file + " was removed!")
		continue
	for i in range(len(mubiao)):
		if mubiao[i] in file:
			os.remove(filen)
			print(file + " was removed!")
			break
