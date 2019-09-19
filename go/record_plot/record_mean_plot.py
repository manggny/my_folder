from nptdms import TdmsFile
import numpy as np
import pickle as pkl
import sys, os
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list_record,make_list,raster
from go.funcs import div_by_laser,make_gonogolick_ordor,div_by_odor_record,div_by_odor
import matplotlib.pyplot as plt
from pyheatmap.heatmap import HeatMap as HM
from matplotlib import cm
import matplotlib as mpl
import matplotlib.colors as colors

def draw_heatmap(data,licks):
	h, w = data.shape
	for i in range(h):
		min = np.min(data[i,:])
		max = np.max(data[i,:])
		for j in range(w):
				data[i,j] = (data[i,j]-min)/(max-min)
	figure = plt.figure(figsize=(10, 10))
	ax1 = figure.add_subplot(121)
	#ax.axis("off")
	#cmap = mpl.cm.  # 蓝，白，红
	ax1.imshow(data, cmap='cividis')
	ax1.plot([50, 50], [0, h], 'k--', linewidth=1, color='red')
	ax1.plot([60, 60], [0, h], 'k--', linewidth=1, color='red')
	ax2 = figure.add_subplot(122)
	ax2.imshow(np.uint8(licks), cmap=plt.get_cmap('gray_r'), aspect='auto')
	ax2.plot([50, 50], [0, h], 'k--', linewidth=1, color='red')
	ax2.plot([60, 60], [0, h], 'k--', linewidth=1, color='red')

	plt.show()

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

def diff(x):
	y = []
	for i in range(len(x)):
		if i == 0:
			y.append(0)
		else:
			y.append(x[i]-x[i-1])
	return y

def prepro_licks(data):
	tr, ti = np.shape(data)
	print(ti)
	i = 0
	for j in range(tr):
		while i < ti:
			try:
				if data[j][i] == 1:
					data[j][i + 1] = 1
					# data[j][i + 2] = 1
					# data[j][i + 3] = 1
					# data[j][i + 4] = 1
					# data[j][i + 5] = 1
					# data[j][i + 6] = 1
					# data[j][i + 7] = 1
					i += 2
				# print(go_lick[j][i + 7])
				else:
					i += 1
			except:
				i += 1
		# print(go_lick[j][i + 7])
		i = 0
	return data

if __name__ == "__main__":
	test = np.zeros(700)

	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_20%/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)
	k = 0

	for file in filelist:
		name, s = file.split('.')
		if s != 'pkl':
			continue

		data = unpickle(pkls_path + file)
		if k == 0:
			odor1_hit = data['odor1'][0]
			odor1_miss = data['odor1'][1]
			odor1_noact = data['odor1'][2]
			odor1_hit_lick = data['odor1_lick'][0]
			odor1_miss_lick = data['odor1_lick'][1]
			odor1_noact_lick = data['odor1_lick'][2]
			odor2_hit = data['odor2'][0]
			odor2_miss = data['odor2'][1]
			odor2_noact = data['odor2'][2]
			odor2_hit_lick = data['odor2_lick'][0]
			odor2_miss_lick = data['odor2_lick'][1]
			odor2_noact_lick = data['odor2_lick'][2]
		else:
			odor1_hit = np.vstack((odor1_hit, data['odor1'][0]))
			odor1_hit_lick = np.vstack((odor1_hit_lick, data['odor1_lick'][0]))

			tr,*_ = odor1_miss.shape
			if tr == 0:
				odor1_miss = data['odor1'][1]
				odor1_miss_lick = data['odor1_lick'][1]
			else:
				if np.ndim(data['odor1'][1]) == 2:
					tr1,ti1 = data['odor1'][1].shape
					if tr1 != 0 and ti1 != 0: #and ti1 != 0:
						print(odor1_miss.shape,data['odor1'][1].shape)
						odor1_miss = np.vstack((odor1_miss, data['odor1'][1]))
						odor1_miss_lick = np.vstack((odor1_miss_lick, data['odor1_lick'][1]))

			tr, *_ = odor1_noact.shape
			if tr == 0:
				odor1_noact = data['odor1'][2]
				odor1_noact_lick = data['odor1_lick'][2]
			else:
				tr1, *_ = data['odor1'][2].shape
				if tr1 is not 0:

					odor1_noact = np.vstack((odor1_noact, data['odor1'][2]))
					odor1_noact_lick = np.vstack((odor1_noact_lick, data['odor1_lick'][2]))

			tr, *_ = odor2_hit.shape
			if tr == 0:
				odor2_hit = data['odor2'][0]
				odor2_hit_lick = data['odor2_lick'][0]
			else:
				tr1, *_ = data['odor2'][0].shape
				if tr1 is not 0:
					odor2_hit = np.vstack((odor2_hit, data['odor2'][0]))
					odor2_hit_lick = np.vstack((odor2_hit_lick, data['odor2_lick'][0]))

			tr, *_ = odor2_miss.shape
			if tr == 0:
				odor2_miss = data['odor2'][1]
				odor2_miss_lick = data['odor2_lick'][1]
			else:
				tr1, *_ = data['odor2'][1].shape
				if tr1 is not 0:
					odor2_miss = np.vstack((odor2_miss, data['odor2'][1]))
					odor2_miss_lick = np.vstack((odor2_miss_lick, data['odor2_lick'][1]))

			tr, *_ = odor2_noact.shape
			if tr == 0:
				odor2_noact = data['odor2'][2]
				odor2_noact_lick = data['odor2_lick'][2]
			else:
				tr1, *_ = data['odor2'][2].shape
				if tr1 is not 0:
					odor2_noact = np.vstack((odor2_noact, data['odor2'][2]))
					odor2_noact_lick = np.vstack((odor2_noact_lick, data['odor2_lick'][2]))

		k+= 1
	odor2_cr = np.vstack((odor2_noact,odor2_miss))
	odor2_cr_lick = np.vstack((odor2_noact_lick,odor2_miss_lick))
	test = np.vstack((np.zeros((50,100)), np.ones((50,100))))
	odor2_hit = np.array(odor2_hit)
	odor1_hit = np.array(odor1_hit)
	odor1_hit_lick = np.array(odor1_hit_lick)
	odor2_hit_lick = np.array(odor2_hit_lick)
	odor1_hit_lick = prepro_licks(odor1_hit_lick)
	odor2_hit_lick = prepro_licks(odor2_hit_lick)
	draw_heatmap(odor2_hit[:,50:150],odor2_hit_lick[:,200:400])
	draw_heatmap(odor2_cr[:, 50:150],odor2_cr_lick[:,200:400])

