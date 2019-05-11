import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os,Image,cv2

def rgb2gray(rgb):
	return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

if __name__ == '__main__':
	files = 'F:/zhaopian/objects/004_0086.jpg'
	img = mpimg.imread(files)
	img2 = rgb2gray(img)
	plt.imshow(img2, cmap='Greys_r')
	plt.show()
	print(img.shape)
	for i in range(len(img[:,1])):
		for j in range(len(img[1,:])):
			gray = 0.299*img[i,j,0]+0.587*img[i,j,1]+0.114*img[i,j,2]
			if gray <= 60:
				img2[i,j] = 255
			else:
				break
		for j in range(len(img[1,:])):
			gray = 0.299*img[i,-j,0]+0.587*img[i,-j,1]+0.114*img[i,-j,2]
			if gray <= 60:
				img2[i,-j] = 255
			else:
				break
			# if img[i,j] >= 250:
			# 	img[i, j] = 0
			# else:
			# 	break





