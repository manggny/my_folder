from sklearn.decomposition import PCA
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans


from matplotlib import style
style.use('ggplot')

from ML_funcs import unpickle

dic_name = 'C:/Users/Administrator/Desktop/EEGDATA/result_sub_features_4labels.pkl'

data = unpickle(dic_name)

print(np.array(data['data']).shape)

result_dic = {'data':[],'labels':data['labels']}
data = np.array(data['data'])

tr,ti,elec = np.shape(data)
result = np.zeros((tr,7,elec))

for i in range(elec):
    data_dummy = data[:,:,i]
    scal = StandardScaler()
    scal.fit(data_dummy)
    s_data = scal.transform(data_dummy)
    p = PCA(n_components = 7)
    p.fit(s_data)
    data_new = p.transform(s_data)
    print(data_new.shape)
    result[:,:,i] = data_new

for i in range(tr):
    result_dic['data'].append(result[i,:,:])
 #   print(result_dic['data'][i].shape)

print(len(result_dic['data']))

output = open('C:/Users/Administrator/Desktop/EEGDATA/result_feature_pca_4labels.pkl', 'wb')
pkl.dump(result_dic, output)
output.close()
#
print('result_feature_pca_4labels.pkl was saved!')
#

# kmeans = MiniBatchKMeans()
# kmeans.fit(data_new)
# centroids = kmeans.cluster_centers_
# labels = kmeans.labels_
#
# print(centroids)
# print(labels)
#
# print(max(labels))
#
# colors = 10*['g.','r.','b.','y.']
# for i in range(len(data_new)):
#     #print('coordinate : ',data_new[i],'label:',labels[i])
#     plt.plot(data_new[i,0],data_new[i,1],colors[labels[i]],markersize=10)
#
# plt.scatter(centroids[:,0],centroids[:,1],marker='x',s=150,linewidths=5,zorder=10)
# plt.show()


