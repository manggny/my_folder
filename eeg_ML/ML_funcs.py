#from keras.models import Sequential
#from keras.layers import Dense,Dropout,LSTM,CuDNNLSTM,BatchNormalization
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import mne
from sklearn.preprocessing import MinMaxScaler

def create_model(input_shape,num_classes=4): # tuple for input_shape
	model = Sequential()
	model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())

	model.add(LSTM(128, input_shape=input_shape))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(Dense(32, activation='relu'))
	model.add(Dropout(0.2))

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
		('Theta', 4, 7),
		('Alpha', 8, 12),
		('Beta', 13, 25),
	]
	#raw = raw_all[:,0]
	# set epoching parameters
	tmin, tmax = -0.2, 1.
	baseline = None
	#raw = mne.io.read_raw_fif(raw_fname, preload=False)
	frequency_map = list()

	for band,fmin,fmax in iter_freqs:
		# (re)load the data to save memory
		#raw = mne.io.read_raw_fif(raw_fname, preload=True)
		#raw.pick_types(meg='grad', eog=True)  # we just look at gradiometers
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


if __name__=="__main__":
	a = np.loadtxt('F:/data_eeg/all_txts/15-1_Baseline CorrectionB.txt', skiprows=1, dtype=float)
	data = get_hzs_wave(a[:,0])
	#print(data[0][1])
	k_data = data[0][1][0:600]
	m_data = mean_range(k_data,25,24)
	print(m_data)
	print(m_data.shape)
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




