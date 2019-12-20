from typing import List

from ML_funcs import unpickle
import matplotlib.pyplot as plt
import numpy as np
from numpy.core._multiarray_umath import ndarray

result_path = 'C:/Users/Administrator/Desktop/EEGDATA/result_svm/'
path = 'C:/Users/Administrator/Desktop/EEGDATA/all_txts'
dic_path = 'C:/Users/Administrator/Desktop/EEGDATA/all_pkl/svm_result_acc_r_boot_0702.pkl'

data = unpickle(dic_path)
print(data)
mean_acc = []

for i in range(35):
    mean_acc.append(np.mean(data[:,i]))
    print(np.mean(data[:,i]))

dummy = mean_acc[:]
sort_idx =[]
print(mean_acc)
for i in range(35):
    best_acc = max(dummy)
    for k in range(35):
        if dummy[k] == best_acc and best_acc > 0:
            sort_idx.append(k)
            dummy[k] = -1
            break
print(sort_idx)
#print(mean_acc)
print(dummy)

filename = path + '/1-1_Baseline CorrectionA.txt'
dummy = open(filename, 'r')
sorted_mean = []
for line in dummy:
    ALL = line.split()
    break
all_35 = [2,3,6,7,10,11,14,15,16,18,20,21,22,23,24,25,26,27,32,33,36,37,40,41,42,43,46,47,50,51,54,55,56,57,61]
xlabels = []
for i in range(35):
    idx = sort_idx[i]
    print(ALL[all_35[idx]])
    xlabels.append(ALL[all_35[idx]])
    sorted_mean.append(mean_acc[idx])

fig = plt.gca()

x_pos = list(range(35))
plt.bar(x_pos,sorted_mean,alpha=0.5,align='center')

plt.ylabel('accuracy of svm')
plt.xticks(x_pos,xlabels)
plt.ylim([0.4,0.8])
plt.xticks(rotation=90)

plt.title('prediction acc of each elecs svm model(iter=1000,data = R condition)')
plt.savefig(result_path+'result_bar_plot of r_0702.png')

