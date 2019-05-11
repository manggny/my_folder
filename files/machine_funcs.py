from PIL import Image
import os,sys
import numpy as np
from two_layer_net import TwoLayerNet
import pickle as pkl

#(x_train,t_train),(x_test,t_test) = load_mnist(normalize=True,one_hot_label=True)

def load_datas(normalize=True):
	filelist = os.listdir("files/trainning/")
	train_img = np.zeros(5)
	labels = np.zeros((11,11))
	q = 0

	for pngs in filelist:

		a = Image.open("files/trainning/" + pngs)
		num,_ = pngs.split(".")
		num = int(num)
		labels[q,num] = 1
		q += 1
		w, h = a.size
		im = a.convert('L')
		#data = im.getdata()
		data = np.asarray(im, dtype='float')
		print(data)
		new_data = np.reshape(data, (1, h * w))
		for i in range(len(new_data[0,:])):
			if new_data[0,i] < 250:
				new_data[0,i] = 0
			else:
				new_data[0,i] = 1
		#print(new_data)

		if np.sum(train_img) == 0:
			train_img = new_data
		else:
			#print("!!")
			train_img = np.append(train_img, new_data, axis=0)

	for i in range(12):
		train_img = np.append(train_img, train_img, axis=0)
		labels = np.append(labels,labels,axis=0)
	print(np.shape(train_img),np.shape(labels))
	dataset = {'train_img':train_img,'train_label':labels,'test_img':train_img,'test_label':labels}

	return dataset['train_img'],dataset['train_label'],dataset['test_img'],dataset['test_label']

def classify_pngs(ndarray_pngs,weights):

	y = weights.predict(ndarray_pngs)
	return np.argmax(y, axis=1)

def analy_pngs(pngs):
	pkl_file = open('weights_final.pkl', 'rb')
	weights = pkl.load(pkl_file)
	pkl_file.close()
	w, h = pngs.size
	cha_num = int(w/8)
	im = pngs.convert('L')
	#data = im.getdata()
	#print(data)
	data = np.asarray(im, dtype='float')
	#data = data[:,:,0]
	#print(np.shape(data))
	raw = []
	result = 0
	for i in range(cha_num):
		dummy = data[:,(i*8):((i+1)*8)]
		print(dummy)
		new_data = np.reshape(dummy, (1, h * 8))
		y = classify_pngs(new_data,weights)
		#print(y)
		if y <10:
			raw.append(y)

	j = len(raw)
	for i in raw:
		if i >9 :
			continue
		else:
			result += i * (10 ** (j - 1))
			j = j-1
	return int(result)


def _change_one_hot_label(X):
	T = np.zeros((X.size, 10))
	for idx, row in enumerate(T):
		row[X[idx]] = 1
	return T