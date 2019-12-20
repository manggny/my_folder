import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from ML_funcs import unpickle,minmax
import matplotlib.pyplot as plt
import random
import keras
import pickle as pkl
MODEL_DIR = "C:/Users/Administrator/Desktop/EEGDATA/result_feature_2labels_dnn"
dic_file = 'C:/Users/Administrator/Desktop/EEGDATA/preprocessed_result_boot_r_0702.pkl'
BATCH_SIZE = 128
EPOCHS = 20
num_Classes = 2
best_acc = 0
best_elec = 0
#checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),save_best_only=True)
all_data = unpickle(dic_file)
accs = np.zeros((10,35))
for re in range(10):
    for elec in range(35):
        data = []
        label = []
        for i in range(len(all_data['data'])):
            if all_data['labels'][i] == 1 or all_data['labels'][i] == 0:
                data.append(all_data['data'][i][:,elec])
                label.append(all_data['labels'][i])
            else:
                continue

        train_data, test_data, train_labels_one_hot, test_labels_one_hot = train_test_split(data, label)
        train_data = np.array(train_data)
        test_data = np.array(test_data)
        print(train_data.shape,test_data.shape)
        print(f'train label 1:{train_labels_one_hot.count(0)}',f'train label 2:{train_labels_one_hot.count(1)}',f'train label 3:{train_labels_one_hot.count(2)}')
        #min_num_train = min(train_labels_one_hot.count(0),train_labels_one_hot.count(1),train_labels_one_hot.count(2))
        #train_data = train_data[0:min_num_train]


        print(f'test label 1:{test_labels_one_hot.count(0)}',f'test label 2:{test_labels_one_hot.count(1)}',f'test label 3:{test_labels_one_hot.count(2)}')

        #
        # train_labels_one_hot = keras.utils.to_categorical(train_labels_one_hot, num_Classes)
        # test_labels_one_hot = keras.utils.to_categorical(test_labels_one_hot, num_Classes)

        # train_data = np.reshape(train_data, (train_data.shape[0], 42, 1))
        # test_data = np.reshape(test_data, (test_data.shape[0], 42, 1))

        # print(train_data.shape,test_data.shape)
        # for p in range(len(train_data[:,1])):
        #     train_data[p,:] = minmax(train_data[p,:])
        # for p in range(len(test_data[:,1])):
        #     #for q in range(len(test_data[1,1,1,:])):
        #     test_data[p,:] = minmax(test_data[p,:])

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
       # print('!!!start!!', elec)
        for i in range(len(pre)):

            if pre[i] == test_labels_one_hot[i]:
                acc+=1
       # print('!!!end!!')
        #print(acc)
        acc = acc/len(test_labels_one_hot)
        accs[re,elec] = acc
        print(re, ' th was finished!')

        #print(test_labels_one_hot)

print(accs)

output = open('C:/Users/Administrator/Desktop/EEGDATA/all_pkl/svm_result_acc_r_boot_0702.pkl', 'wb')
pkl.dump(accs, output)
output.close()