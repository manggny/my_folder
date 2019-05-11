import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc,os,sys
from scipy import ndimage

path = 'F:/zhaopian/fa'
filelist = os.listdir(path)
mubiao = ['_45','_90','_135','_180','_225','_270','_315']


for file in filelist:
	*_,s = file.split('.')
	if s != 'jpg'and s != 'JPG':
		continue
	file = path + '/' + file
	img = plt.imread(file)
	filename,*_ = file.split('.')
	ex = 0
	for i in range(len(mubiao)):
		if mubiao[i] in filename:

			ex = 1
			break
	if ex == 1:
		print(file + " is already exist!")
		continue

	for degree in range(8):
		#plt.subplot(151+degree)
		if degree == 0:
			save_file = filename + '.jpg'
		else:
			save_file = filename + "_"+str(degree*45) + '.jpg'


		rotated_img = ndimage.rotate(img, degree * 45)
		plt.imsave(save_file,rotated_img)
	print(filename + ' finish!')
	os.remove(file)
		#plt.imshow(rotated_img,cmap=plt.cm.gray)
		#plt.axis('off')

