import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from ML_funcs import unpickle,minmax
from sklearn.decomposition import PCA
import sklearn.preprocessing
import matplotlib.pyplot as plt
import random
import keras
import pickle as pkl
dic_file_fa = 'F:/Insula-Gcamp6/record/record_split_by_behav/50%_nogo_hit_trials.pkl'
dic_file_cr = 'F:/Insula-Gcamp6/record/record_split_by_behav/50%_nogo_miss_trials.pkl'

result_path= 'C:/Users/manggny/Desktop/record_all/'

num_Classes = 2

#checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),save_best_only=True)
data_fa = unpickle(dic_file_fa)
data_cr = unpickle(dic_file_cr)
ticks = 28
start = 0
time_acc = np.zeros(ticks) # 1 for 0.2s, all 3s (-2s~1s)
loop_time = 1000
time_step = 25

lower = min(np.alen(data_fa),np.alen(data_cr))
# for i in range(np.alen(data_fa)):
# 	data_fa[i,:] = sklearn.preprocessing.scale(data_fa[i,:],axis=0) #,feature_range=(-1,1)
# for i in range(np.alen(data_cr)):
# 	data_cr[i, :] = sklearn.preprocessing.scale(data_cr[i, :], axis=0) #,feature_range=(-1,1)




for loop in range(loop_time):
	idx_data_fa = list(range(np.alen(data_fa)))
	idx_data_cr = list(range(np.alen(data_cr)))
	idx_data_fa = random.sample(idx_data_fa,lower)
	idx_data_cr = random.sample(idx_data_cr,lower)
	print('Now start ',loop,'th loop!')
	for time in range(ticks):
		data = []
		labels = []
		for i in idx_data_cr:
			data.append(data_cr[i,start + time*time_step:start + time_step+time*time_step])
			labels.append(1)
		for i in idx_data_fa:
			data.append(data_fa[i,start + time*time_step:start + time_step+time*time_step])
			labels.append(0)

		train_data, test_data, train_labels_one_hot, test_labels_one_hot = train_test_split(data, labels)
		train_data = np.array(train_data)
		test_data = np.array(test_data)
		print(train_data.shape,test_data.shape)
		print(f'train label 1:{train_labels_one_hot.count(0)}',f'train label 2:{train_labels_one_hot.count(1)}',f'train label 3:{train_labels_one_hot.count(2)}')
		print(f'test label 1:{test_labels_one_hot.count(0)}',f'test label 2:{test_labels_one_hot.count(1)}',f'test label 3:{test_labels_one_hot.count(2)}')

		train_data = train_data.astype('float32')
		test_data = test_data.astype('float32')
		#test_data = minmax(test_data)
		print(11111)

		print(train_data.shape, len(train_labels_one_hot))
		#print(train_labels_one_hot.shape, test_labels_one_hot.shape)

		print('1111',train_data.shape[1:])
		print(train_data[1:].shape)
		# print(train_labels_one_hot[1].shape)

		clf = svm.SVC(gamma=0.001,C=100)

		clf.fit(train_data,train_labels_one_hot)
		#print()
		pre = clf.predict(test_data)
		acc = 0
		for i in range(len(pre)):
			if pre[i] == test_labels_one_hot[i]:
				acc += 1

		time_acc[time] += acc/len(test_labels_one_hot)

for i in range(ticks):
	time_acc[i] = time_acc[i]/loop_time

print("all accs is! : " )
print(time_acc)

x_pos = list(range(ticks))
plt.bar(x_pos,time_acc,alpha=0.5,align='center')

plt.ylabel('no-go svm accuracy of each time(-2s~1s)')
plt.xlabel('Time(-2s~1s,0.5s for each ticks)')
plt.xticks(x_pos)
plt.ylim([0.4,0.8])

plt.title('no-go fa-cr svm accuracy of each time(0.5s)')
plt.savefig(result_path+'alltime_result_acc_plot of fa-cr_svm_0723 20%.png')