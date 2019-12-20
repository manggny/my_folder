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
dic_file_20 = 'F:/Insula-Gcamp6/record/record_split_by_behav/20%_nogo_fa_trials.pkl'
dic_file_50 = 'F:/Insula-Gcamp6/record/record_split_by_behav/50%_nogo_fa_trials.pkl'

result_path= 'C:/Users/manggny/Desktop/record_all/'

num_Classes = 2

#checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),save_best_only=True)
data_20 = unpickle(dic_file_20)
data_50 = unpickle(dic_file_50)
ticks = 5
start = 0
time_acc = np.zeros(ticks) # 1 for 0.2s, all 3s (-2s~1s)
loop_time = 1000
time_step = 10

lower = min(np.alen(data_20),np.alen(data_50))

# for i in range(np.alen(data_20)):
# 	data_20[i,:] = sklearn.preprocessing.minmax_scale(data_20[i,:],axis=0,feature_range=(-1,1))
# for i in range(np.alen(data_50)):
# 	data_50[i, :] = sklearn.preprocessing.minmax_scale(data_50[i, :], axis=0,feature_range=(-1,1))




for loop in range(loop_time):
	idx_data_20 = list(range(np.alen(data_20)))
	idx_data_50 = list(range(np.alen(data_50)))
	idx_data_20 = random.sample(idx_data_20,lower)
	idx_data_50 = random.sample(idx_data_50,lower)
	print('Now start ',loop,'th loop!')
	for time in range(ticks):
		data = []
		labels = []
		for i in idx_data_20:
			data.append(data_20[i,start + time*time_step:start + time_step+time*time_step])
			labels.append(1)
		for i in idx_data_50:
			data.append(data_50[i,start + time*time_step:start + time_step+time*time_step])
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

plt.ylabel('no-go svm accuracy of each time(-2s~12s)')
plt.xlabel('Time(-2s~12s,0.5s for each ticks)')
plt.xticks(x_pos)
plt.ylim([0.4,0.8])

plt.title('no-go 20%-50%(cr) svm accuracy of each time(0.2s)')
plt.savefig(result_path+'0~0.6_result_acc_plot of 20-50 cr_svm_0724.png')