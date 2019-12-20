from keras.models import Sequential
from keras.layers import Dense,Dropout,LSTM,BatchNormalization, Conv2D, Conv1D,AveragePooling1D,MaxPooling2D,Flatten, MaxPooling1D,GlobalMaxPooling2D,Reshape
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import mne,random
from sklearn.preprocessing import MinMaxScaler



def minmax(data):
	mm = MinMaxScaler((-1,1))
	data = mm.fit_transform(data)

	return data

def create_model2(input_shape,num_classes=4): # tuple for input_shape

	model = Sequential()
	model.add(Conv2D(32, (5, 6), padding='same', activation='relu', input_shape=input_shape))
	#model.add(Conv2D(32, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))  #, input_shape=input_shape))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())
	print(model.summary())
	model.add(Reshape((72, 64)))

	#model.add(GlobalMaxPooling1D())



	model.add(LSTM(48))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	# model.add(LSTM(128, input_shape=(32,1), return_sequences=True))
	# model.add(Dropout(0.1))
	# model.add(BatchNormalization())

	# model.add(LSTM(48))
	# model.add(Dropout(0.2))
	# model.add(BatchNormalization())


	model.add(Dense(48))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())
	model.add(Dense(num_classes, activation='softmax'))
	print(model.summary())
	return model

def create_model3(input_shape,num_classes=4): # tuple for input_shape

	model = Sequential()
	model.add(Conv1D(12, padding="same", activation="relu", input_shape=input_shape, kernel_size=2))
	#model.add(Conv232, (3, 3), activation='relu'))
	model.add(MaxPooling1D(pool_size=2,data_format='channels_last'))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())
	#
	# model.add(Conv1D(32, padding="same", activation="relu", kernel_size=3))  #, input_shape=input_shape))
	# # model.add(Conv2D(64, (3, 3), activation='relu'))
	# model.add(MaxPooling1D(pool_size=2,data_format='channels_last'))
	# model.add(Dropout(0.1))
	# model.add(BatchNormalization())

	# model.add(Conv1D(32, padding="same", activation="relu", kernel_size=3)) #, input_shape=input_shape))
	# # #model.add(Conv2D(32, (3, 3), activation='relu'))
	# model.add(MaxPooling1D(pool_size=3,data_format='channels_last'))
	# model.add(Dropout(0.2))
	# model.add(BatchNormalization())
	print(model.summary())
	#model.add(GlobalMaxPooling1D())

	# model.add(LSTM(20)) #)))
	# model.add(Dropout(0.2))
	# # model.add(BatchNormalization())

	model.add(LSTM(6))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())

	# model.add(LSTM(48))
	# model.add(Dropout(0.2))
	# model.add(BatchNormalization())

	model.add(Dense(16, activation='relu'))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())
	model.add(Dense(8, activation='relu'))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())
	model.add(Dense(num_classes, activation='softmax'))
	print(model.summary())
	return model

def create_model(input_shape,num_classes=4): # tuple for input_shape
	model = Sequential()
	model.add(LSTM(24, input_shape=input_shape, return_sequences=True))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	# model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
	# model.add(Dropout(0.1))
	# model.add(BatchNormalization())

	model.add(LSTM(12, input_shape=input_shape))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(Dense(24, activation='relu'))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())
	model.add(Dense(num_classes, activation='softmax'))

	return model

def create_DNN(input_shape,num_classes=4): # tuple for input_shape
	model = Sequential()
	model.add(Flatten())
	model.add(Dense(32, activation='relu'))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())
	# model.add(Dense(128, activation='relu'))
	# model.add(Dense(128, activation='relu'))
	model.add(Dense(32, activation='relu'))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())
	model.add(Dense(num_classes, activation='softmax'))
	return model

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data


def merge(dic1, dic2):
	result = {'data': [], 'labels': []}
	result['data'] = dic1['data'] + dic2['data']
	result['labels'] = dic1['labels'] + dic2['labels']
	print((result['data'][0].shape))
	# result['filenames']  = dic1['filenames'] + dic2['filenames']

	return result


def get_hzs_wave(raw):
	#raw_all = np.loadtxt(filename, skiprows=1, dtype=float)
	#data_path = ''
	#raw_fname = data_path + 'sef_raw_sss.fif'
	iter_freqs = [
		('Theta', 4, 8),
		('Alpha', 8, 12),
		('Beta', 12, 30),
	]
	#raw = raw_all[:,0]
	# set epoching parameters
	# tmin, tmax = -0.2, 1.
	# baseline = None
	#raw = mne.io.read_raw_fif(raw_fname, preload=False)
	frequency_map = list()

	for band,fmin,fmax in iter_freqs:
		# (re)load the data to save memory
		#raw = mne.io.read_raw_fif(raw_fname, preload=True)
		#raw.pick_types(meg='grad', eog=True)  # we just look at grsadiometers
		fre = np.arange(fmin,fmax+0.1,0.1)
		#print(fre)

		# centfrq('cmor25-1', 15)*500./Alpha
		for z in range(len(raw)):
			raw[z] = raw[z] - np.mean(raw)
		#print((raw-np.mean(raw).shape))
		#data = pywt.cwt(raw, 500./fre, 'cmor25-1')
		#data = np.array(data)
		# print(data[1].shape,data[0].shape)
		# print(data[0])
		data = mne.filter.filter_data(raw,500,fmin,fmax,l_trans_bandwidth=1,h_trans_bandwidth=1)
		# bandpass filter and compute Hilbert
		# raw.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
		# 		   l_trans_bandwidth=1,  # make sure filter params are the same
		# 		   h_trans_bandwidth=1,  # in each band and skip "auto" option.
		# 		   fir_design='firwin')
		# raw.apply_hilbert(n_jobs=1, envelope=False)
		frequency_map.append(((band, fmin, fmax), data))

	return frequency_map

def mean_range(data,binrange=25,binnum=24):
	result = np.zeros(binnum)
	for i in range(binnum):
		#print('i :',i)
		for j in range(binrange):
			inx = (i*binrange)+j
		#	print('inx :', inx)
			result[i] += data[inx]
		#print(result[i])
		result[i] = result[i]/binrange
		#print('after mean:', result[i])
	return result

def boostrap_RNN(data,stepwise=100,num=30000,length=600):

	output = []
	list_idx = []

	for i in range(len(data)):
		list_idx.append(i)
	for i in range(num):
		samples = np.zeros(length)
		dummy = random.sample(list_idx, stepwise)
		# print(type(dummy))
		# print(type(dummy[1]))
		for j in dummy:
			samples += data[j]
		samples = samples/stepwise
		output.append(samples)

	return output

def boostrap_3d(data,stepwise=100,num=30000,shape=(35,36)):

	output = []
	list_idx = []

	for i in range(len(data)):
		list_idx.append(i)
	for i in range(num):
		samples = np.zeros(shape)
		dummy = random.sample(list_idx, stepwise)
		# print(type(dummy))
		# print(type(dummy[1]))
		for j in dummy:
			samples += data[j]
		samples = samples/stepwise
		output.append(samples)

	return output


def peak_range(data,binrange=25,binnum=24):
	result = np.zeros(binnum)
	for i in range(binnum):
		#print('i :',i)
		for j in range(binrange):
			inx = (i*binrange)+j
		#	print('inx :', inx)
			if abs(data[inx]) > abs(result[i]):
				result[i] = data[inx]
		#print(result[i])
		#result[i] = result[i]/binrange
		#print('after mean:', result[i])
	return result


if __name__=="__main__":
	a = np.loadtxt('C:/Users/Administrator/Desktop/EEGDATA/all_txts/15-1_Baseline CorrectionB.txt', skiprows=1, dtype=float)
	#data = get_hzs_wave(a[:,0])
	#print(data[0][1])
	k_data = a[:,1]
	k_data = minmax(k_data)
	print(min(k_data),max(k_data))
	# m_data = mean_range(k_data,25,24)
	# print(m_data)
	# print(m_data.shape)
	#
	# print(type(data))
	#
	# print(data[0][1])
	# print(min(data[0][1]),max(data[0][1]))
	# #k_data = preprocessing.scale(data[0][1])
	# mm = MinMaxScaler()
	# mm_data = mm.fit_transform(data[0][1])
	#
	# print(min(mm_data), max(mm_data))
	# print(len(mm_data))




