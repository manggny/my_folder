# load the original pkl file(not dived), and save it after optimizing.


from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from scipy import log
import os

def load_tdms(cal_pkl_name):

	cal_pkl_file = open(cal_pkl_name, 'rb')
	cal = pkl.load(cal_pkl_file)

	cal_group = cal.groups()
	cal_channels = cal.group_channels(cal_group[0])
	cal_channels_data = []
	for i in cal_channels:
		c = i
		c = c.path.split('/')
		c = c[2].replace("'", "")
		cal_channels_data.append(cal.channel_data(cal_group[0], c))
	return cal_channels_data

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

def func(x, a, b, c):
	return a * np.exp(-b * x) + c

def func2(x, a, b):
	return a * log(x) + b

def normalizing_z(cal):
	f0 = np.mean(cal)
	q = np.std(cal)
	result = []
	for i in range(len(cal)):
		result.append((cal[i]-f0)/q)
	return result

if __name__=="__main__":
	pkl_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/after_optimize/gonogo20/'

	### setting###
	filename = '#5_Lacc(r,2)+rai(b,3)_0120_gonogotest_opt_r.pkl'

	name,_ = filename.split('.')
	cal = unpickle(pkl_path+filename)

	xdata = np.linspace(0, round(len(cal[0])/50), len(cal[0]))

	y = cal[1]
	plt.plot(xdata, y, 'b-')

	print(np.median(y))
	y2 = normalizing_z(y)
	for i in range(len(y2)):
		y2[i] = y2[i] + 3
	plt.plot(xdata, y2, 'r--')

	plt.show()


