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
	pkl_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_and_clean/80/after_div/'

	### setting###
	filename = '#f1_gonogo80record__r(red)_left(blue,weak)_190705_cleaned_l_behav.pkl'

	name,_ = filename.split('.')
	cal = unpickle(pkl_path+filename)
	# result_dic['odor1'].append(odor1_pump_trials)
	# result_dic['odor1'].append(odor1_miss_trials)
	# result_dic['odor2'].append(odor2_pump_trials)
	# result_dic['odor2'].append(odor2_miss_trials)


	y = cal['odor1'][0]
	y1 = cal['odor1'][0]
	y2 = cal['odor1'][0]
	y3 = cal['odor1'][0]
	xdata = np.linspace(0, round(len(y) / 50), len(y))
	plt.plot(xdata, y, 'b-')
	plt.plot(xdata, y1, 'r-')
	plt.plot(xdata, y2, 'y-')
	plt.plot(xdata, y3, 'g-')


	print(np.median(y))
	# y2 = normalizing_z(y)
	# for i in range(len(y2)):
	# 	y2[i] = y2[i] + 3
	# plt.plot(xdata, y2, 'r--')

	plt.show()


