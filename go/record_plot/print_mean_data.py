from xlutils.copy import copy
import xlwt, xlrd,os
import numpy as np
import matplotlib.pyplot as plt
import sklearn.preprocessing
def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

if __name__=="__main__":
	test = np.zeros(700)

	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_20%/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)
	k = 0
	all_odor1_hit_mean = np.zeros(700)
	all_odor1_m_mean = np.zeros(700)
	all_odor2_cr_mean = np.zeros(700)
	all_odor2_hit_mean = np.zeros(700)

	for file in filelist:
		name,s = file.split('.')
		if s != 'pkl':
			continue

		data = unpickle(pkls_path + file)

		odor1_hit = data['odor1'][0]
		odor1_hit_mean=np.zeros(700)
		odor2_hit_mean = np.zeros(700)
		odor2_noact_mean = np.zeros(700)
		odor2_miss_mean = np.zeros(700)

		tr,ti = odor1_hit.shape

		odor1_miss = data['odor1'][1]
		odor1_noact = data['odor1'][2]
		odor2_hit = data['odor2'][0]
		odor2_miss = data['odor2'][1]
		odor2_noact = data['odor2'][2]
		tr2,*_ = odor2_noact.shape
		tr3,*_ = odor2_miss.shape
		if tr2 == 0:
			odor2_cr = odor2_miss
		elif tr3 == 0:
			odor2_cr = odor2_noact
		else:
			odor2_cr = np.vstack((odor2_miss,odor2_noact))



		#odor1_m = np.zeros(700)
		tr2, *_ = odor1_noact.shape
		tr3, *_ = odor1_miss.shape
		if np.ndim(odor1_noact)>1 and np.ndim(odor1_miss) > 1:
			tr2, ti2 = odor1_noact.shape
			tr3, ti3 = odor1_miss.shape
			if tr2 == 0 or ti2 == 0:
				odor1_m = odor1_miss
			elif tr3 ==0 or ti3 == 0:
				odor1_m = odor1_noact
			else:
				odor1_m = np.vstack((odor1_miss, odor1_noact))

		elif np.ndim(odor1_noact)<2:
			odor1_m = odor1_miss
		elif  np.ndim(odor1_miss)<2:
			odor1_m = odor1_noact

		odor2_cr_mean = np.zeros(700)
		odor1_m_mean = np.zeros(700)
		odor1_miss_mean = np.zeros(700)
		tr,*_ = np.shape(odor1_miss)
		ntr,*_ = np.shape(odor2_hit)
		print(file)
		# for i in range(ntr):
		# 	print(odor1_m[i,100:110])\
		# for i in range(np.alen(odor1_hit)):
		# 	odor1_hit[i,:] = sklearn.preprocessing.scale(odor1_hit[i,:])#,feature_range=(-1,1))
		# for i in range(np.alen(odor1_m)):
		# 	odor1_m[i,:] = sklearn.preprocessing.scale(odor1_m[i,:])#,feature_range=(-1,1))
		# for i in range(np.alen(odor2_cr)):
		# 	odor2_cr[i,:] = sklearn.preprocessing.scale(odor2_cr[i,:])#,feature_range=(-1,1))
		# for i in range(np.alen(odor2_hit)):
		# 	odor2_hit[i,:] = sklearn.preprocessing.scale(odor2_hit[i,:])#,feature_range=(-1,1))

		for i in range(ti):
			odor1_hit_mean[i] = np.mean(odor1_hit[:,i])
			odor1_m_mean[i] = np.mean(odor1_m[:, i])
			# if tr > 0 and tr < 200:
			# 	odor1_miss_mean[i] = np.mean(odor1_miss[:, i])
			odor2_hit_mean[i] = np.mean(odor2_hit[:,i])
			odor2_cr_mean[i] = np.mean(odor2_cr[:,i])
			# odor2_noact_mean[i] = np.mean(odor2_noact[:, i])
			# odor2_miss_mean[i] = np.mean(odor2_miss[:, i])
		print('odor2 fa', np.shape(odor2_hit))
		print('odor2 cr', np.shape(odor2_cr))
		print('odor1 miss', np.shape(odor1_m))
		print('odor1 hit', np.shape(odor1_hit))

		#
		oldwb = xlrd.open_workbook('result_20.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)

		for i in range(100,125):

			sheet.write(i-89, k, str(odor1_hit_mean[i]))
			sheet.write(i - 89, k + 15, str(odor1_m_mean[i]))
			sheet.write(i-50, k, str(odor2_cr_mean[i]))
			sheet.write(i - 50, k + 15, str(odor2_hit_mean[i]))
		sheet.write(0, k, file)
		# x1 = np.linspace(-2, 12, 700)
		# plt.plot(x1, odor1_hit_mean, 'r', label='odor1_hit')
		# plt.plot(x1, odor1_m_mean, 'b', label='odor1_miss')
		# plt.plot(x1, odor2_cr_mean, 'y', label='odor2_cr')
		# plt.plot(x1, odor2_hit_mean, 'g', label='odor2_fa')
		# plt.show()

		k += 1
		os.remove('result_20.xls')
		newwb.save('result_20.xls')
		all_odor1_hit_mean += odor1_hit_mean
		all_odor1_m_mean += odor1_m_mean
		all_odor2_cr_mean += odor2_cr_mean
		all_odor2_hit_mean += odor2_hit_mean

	all_odor1_hit_mean/= k
	all_odor1_m_mean /= k
	all_odor2_cr_mean /= k
	all_odor2_hit_mean /= k
	x1 = np.linspace(-2, 12, 700)

	plt.plot(x1, all_odor1_hit_mean, 'r', label='odor1_hit')
	plt.plot(x1, all_odor1_m_mean, 'b', label='odor1_miss')
	plt.plot(x1, all_odor2_cr_mean, 'y', label='odor2_cr')
	plt.plot(x1, all_odor2_hit_mean, 'g', label='odor2_fa')

	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.show()
		#plt.savefig(f_name + "left.png")
		#plt.close()

