import pickle as pkl
from PIL import Image
import numpy as np
from files.machine_funcs import analy_pngs
import os,sys

pkl_file = open('weights_final.pkl', 'rb')
weights = pkl.load(pkl_file)
for key in ('W1', 'b1', 'W2', 'b2'):
	print(type(weights))
files = os.listdir("files/test/ans/")
path = "files/test/ans/"
j = 0
for file in files:

	a = Image.open(path+file)#"files/test/real_test/109.png")#"C:/Users/manggny/PycharmProjects/my_folder/files/trainning/0.png")#)"files/test/real_test/109.png")
# w, h = a.size
# im = a.convert('L')
# data = im.getdata()
# data = np.array(data, dtype='float')
# new_data = np.reshape(data, (1, h * w))
	y = analy_pngs(a)
	try:
		os.rename(path+file,path+str(y)+".png")
	except:
		os.rename(path + file, path + str(y) + str(j)+".png")
		j += 1
