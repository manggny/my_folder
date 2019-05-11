from PIL import Image
import os,sys
import numpy as np
import scipy.misc
from files.machine_funcs import load_datas
from two_layer_net import TwoLayerNet
import pickle as pkl

filelist = os.listdir("files/trainning/")

x_train,t_train,x_test,t_test = load_datas()
print(np.shape(x_train),np.shape(t_train))
network = TwoLayerNet(input_size=160,hidden_size=10,output_size=11)
iters_num = 10000
train_size = x_train.shape[0]
batch_size = 100
learning_rate = 0.01

train_loss_list = []
train_acc_list = []
test_acc_list = []

iter_per_epoch = 1000#max(train_size/batch_size,1)

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
#print(network.params)

output = open('weights.pkl', 'wb')
pkl.dump(network, output)
output.close()

pkl_file = open('weights.pkl', 'rb')
weights = pkl.load(pkl_file)
# for pngs in filelist:
# 	if pngs == 'test' or pngs == 'trainning':
# 		continue
# 	a = Image.open("files/trainning/"+pngs)
# 	name,_ =pngs.split(".")
# 	path = "C:/Users/manggny/PycharmProjects/my_folder/files/trainning/"
# 	w,h = a.size
# 	im = a.convert('L')
# 	data = im.getdata()
#
# 	data = np.array(data, dtype='float')
# 	new_data = np.reshape(data, (1, h*w))
# 	if np.sum(train_img) == 0:
# 		train_img = new_data
# 	else:
# 		print("!!")
# 		train_img = np.append(train_img, new_data, axis=0)

#	print(np.shape(new_data))




#print(np.reshape(train_img[1,:],(h,w)))



	#print(np.shape(new_data))
	#print(new_data[:,0:8])
	# 8 fixels for one character(width,height = 20(fixed)))
	# i should make : put the png's filename, and return the number of the png.
	# 팡이 들어오면, 넘파이 매트릭스로 만들고, 0 1 로 처리(250넘는건 다 1, 나머진 0)으로 바꿔서 계산. 저기 그림중에 절반만
	# 써서 만들어서 나머지 시험!
	# 학습 시킬 사진들을 0~9까지 나눠서, 한자리수 학습으로 우선 진행. 나중에 함수에서 쓰는걸로.
	# 0~9까지로 나뉜 사진을 학습 폴더에 넣고. 데이터 불러오는 함수 만들기! 그 함수에 100을 넣으면, 그 사진들중에 랜덤으로 100개 중복
	# 있게 뽑고, 사진 이름에 따라(사진 이름을 정답으로) 원 핫 인코딩 만들어서, 정답 레이블로 사용. 학습 정확도가 100%되면(100번 10회)
	# 테스트 진행.