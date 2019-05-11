import os,sys,shutil

path = 'F:/zhaopian/positive/male'
result = 'F:/zhaopian/all'
filelist = os.listdir(path)


for file in filelist:
	name,s = file.split('.')
	print(s)
	if s != 'gif':
		continue

	print('1')
	filename = path + '/' + file
	dummy_name = 'pos_m_'+file
	new_name = result+'/'+dummy_name
	shutil.copyfile(filename, new_name)