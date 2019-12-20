from ML_funcs import unpickle, mean_range, create_model
import numpy as np
import pickle as pkl
import sklearn.preprocessing

all_data_path = 'C:/Users/Administrator/Desktop/EEGDATA/result_boot_r_0702.pkl'

data_all = unpickle(all_data_path)
print(data_all['labels'].count(0), data_all['labels'].count(1), data_all['labels'].count(2),
      data_all['labels'].count(3))

trial_num = len(data_all['data'])
datas = []
labels = []
print(data_all['data'][1].shape)
for i in range(trial_num):
    _, col = data_all['data'][i].shape
    print(data_all['data'][i].shape)
    if (data_all['labels'][i] == 1):  # or (data_all['labels'][i] == 2):
        print(data_all['labels'][i])
        for k in range(col):
            data_all['data'][i][:,k] = sklearn.preprocessing.scale(data_all['data'][i][:,k])
        datas.append(data_all['data'][i])
        labels.append(1)
    elif (data_all['labels'][i] == 0):
        print(data_all['labels'][i])
        for k in range(col):
            data_all['data'][i][:,k] = sklearn.preprocessing.scale(data_all['data'][i][:,k])
        datas.append(data_all['data'][i])
        labels.append(0)

print(len(datas), len(labels))
result = {'data': datas, 'labels': labels}
output = open('C:/Users/Administrator/Desktop/EEGDATA/preprocessed_result_boot_r_0702.pkl', 'wb')
pkl.dump(result, output)
output.close()



