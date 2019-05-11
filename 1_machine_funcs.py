from PIL import Image
import os,sys
import numpy as np
from two_layer_net import TwoLayerNet

#(x_train,t_train),(x_test,t_test) = load_mnist(normalize=True,one_hot_label=True)

def aa(x_train,t_train,x_test,t_test):
	network = TwoLayerNet(input_size=160,hidden_size=50,output_size=10)

	iters_num = 10000
	train_size = x_train.shape[0]
	batch_size = 100
	learning_rate = 0.1

	train_loss_list = []
	train_acc_list = []
	test_acc_list = []

	iter_per_epoch = max(train_size/batch_size,1)

	for i in range(iters_num):
		batch_mask = np.random.choice(train_size,batch_size)
		x_batch = x_train[batch_mask]
		t_batch = t_train[batch_mask]

		grad = network.gradient(x_batch,t_batch)

		for key in ('W1','b1','W2','b2'):
			network.params[key] -= learning_rate * grad[key]

		loss = network.loss(x_batch,t_batch)
		train_loss_list.append(loss)

		if i % iter_per_epoch == 0:
			train_acc = network.accuracy(x_train,t_train)
			test_acc = network.accuracy(x_test,t_test)
			train_acc_list.append(train_acc)
			test_acc_list.append(test_acc)
			print(train_acc,test_acc)

def load_datas(normalize=True):
	filelist = os.listdir("files/trainning/")
	train_img = np.zeros(5)
	labels = np.zeros((11,11))
	q = 0
	for pngs in filelist:

		a = Image.open("files/" + pngs)
		num,_ = pngs.split(".")
		num = int(num)
		labels[q,num] = 1
		q += 1
		w, h = a.size
		im = a.convert('L')
		data = im.getdata()
		data = np.ndarray(data, dtype='float')
		new_data = np.reshape(data, (1, h * w))
		if np.sum(train_img) == 0:
			train_img = new_data
		else:
			#print("!!")
			train_img = np.append(train_img, new_data, axis=0)
	dataset = {'train_img':train_img,'train_label':labels,'test_img':train_img,'test_label':labels}

	return dataset['train_img'],dataset['train_label'],dataset['test_img'],dataset['test_label']


def _change_one_hot_label(X):
	T = np.zeros((X.size, 10))
	for idx, row in enumerate(T):
		row[X[idx]] = 1
	return T