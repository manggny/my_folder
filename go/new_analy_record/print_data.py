from xlutils.copy import copy
import xlwt, xlrd,os
import numpy as np
def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

def normalizing_p(trial_data,part):
	f0 = np.mean(part)
	result = np.zeros(len(trial_data))
	for i in range(len(trial_data)):
		result[i] = (trial_data[i]-f0)/trial_data[i]
	return result

if __name__=="__main__":
	test = np.zeros(700)

	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/after_optimize/after_cleaning/after_delete/gonogo20/after_behav/goods/merged/'

	filelist = os.listdir(pkls_path)
	k = 0

	for file in filelist:
		name,s = file.split('.')
		if s != 'pkl':
			continue

		print(file,'start!!')

		data = unpickle(pkls_path + file)

		odor1_hit = data['odor1'][0]
		odor1_hit_mean=np.zeros(700)
		odor2_hit_mean = np.zeros(700)
		odor2_noact_mean = np.zeros(700)
		odor2_miss_mean = np.zeros(700)
		tr,ti = odor1_hit.shape

		odor1_miss = data['odor1'][1]
		#odor1_noact = data['odor1'][2]
		odor2_hit = data['odor2'][0]
		odor2_miss = data['odor2'][1]
		#odor2_noact = data['odor2'][2]
		odor2_cr = odor2_miss
		odor1_m = odor1_miss
		#
		# tr2,*_ = odor2_noact.shape
		# tr3,*_ = odor2_miss.shape
		# if tr2 == 0:
		# 	odor2_cr = odor2_miss
		# elif tr3 == 0:
		# 	odor2_cr = odor2_noact
		# else:
		# 	odor2_cr = np.vstack((odor2_miss,odor2_noact))
		#
		# #odor1_m = np.zeros(700)
		# tr2, *_ = odor1_noact.shape
		# tr3, *_ = odor1_miss.shape
		# if np.ndim(odor1_noact)>1 and np.ndim(odor1_miss) > 1:
		# 	tr2, ti2 = odor1_noact.shape
		# 	tr3, ti3 = odor1_miss.shape
		# 	if tr2 == 0 or ti2 == 0:
		# 		odor1_m = odor1_miss
		# 		#odor1_m_pre = odor1_miss_pre
		# 	elif tr3 ==0 or ti3 == 0:
		# 		odor1_m = odor1_noact
		# 		#odor1_m_pre = odor1_noact_pre
		# 	else:
		# 		odor1_m = np.vstack((odor1_miss, odor1_noact))
		#
		# elif np.ndim(odor1_noact)<2:
		# 	odor1_m = odor1_miss
		# 	#odor1_m_pre = odor1_miss_pre
		# elif  np.ndim(odor1_miss)<2:
		# 	odor1_m = odor1_noact
		# 	#odor1_m_pre = odor1_noact_pre
		print('!!!!!', odor1_m.shape)
		print('odor2 fa', np.shape(odor2_hit))
		print('odor1 miss', np.shape(odor1_miss))
		# print('odor1 noact', np.shape(odor1_noact))
		print('odor1 hit', np.shape(odor1_hit))
		print('odor2 cr', np.shape(odor2_cr))

		for i in range(np.alen(odor1_hit)):
			odor1_hit[i,:] = normalizing_p(odor1_hit[i,:],odor1_hit[i,0:100])

		if np.alen(odor1_m)> 0 and np.alen(odor1_m) < 700:
			for i in range(np.alen(odor1_m)):
				odor1_m[i, :] = normalizing_p(odor1_m[i,:],odor1_m[i, 0:100])
		elif np.alen(odor1_m) == 700 or np.alen(odor1_m) == 1:
			odor1_m[:] = normalizing_p(odor1_m[:], odor1_m[0:100])
		else:
			odor1_m = np.array([])

		print(odor2_cr.shape)
		for i in range(np.alen(odor2_cr)):
			odor2_cr[i, :] = normalizing_p(odor2_cr[i,:],odor2_cr[i, 0:100])


		if np.alen(odor2_hit)> 0 and np.alen(odor2_hit) < 700:
			for i in range(np.alen(odor2_hit)):
				odor2_hit[i, :] = normalizing_p(odor2_hit[i,:],odor2_hit[i, 0:100])
		elif np.alen(odor2_hit) == 700 or np.alen(odor2_hit) == 1:
			odor2_hit[:] = normalizing_p(odor2_hit[:], odor2_hit[0:100])
		else:
			odor2_hit = np.array([])

		odor2_cr_mean = np.zeros(700)
		odor1_m_mean = np.zeros(700)
		odor1_miss_mean = np.zeros(700)
		tr,*_ = np.shape(odor1_miss)
		ntr,*_ = np.shape(odor2_hit)
		print(file)
		# for i in range(ntr):
		# 	print(odor1_m[i,100:110])

		for i in range(ti):
			odor1_hit_mean[i] = np.mean(odor1_hit[:,i])
			if np.alen(odor1_m) > 0:
				if np.alen(odor1_m) == 700:
					odor1_m_mean = odor1_m
				else:
					odor1_m_mean[i] = np.mean(odor1_m[:, i])

			if np.alen(odor2_hit) > 0:
				if np.alen(odor2_hit) == 700:
					odor2_hit_mean = odor2_hit
				else:
					odor2_hit_mean[i] = np.mean(odor2_hit[:, i])


			#odor2_hit_mean[i] = np.mean(odor2_hit[:,i])
			odor2_cr_mean[i] = np.mean(odor2_cr[:,i])
			# odor2_noact_mean[i] = np.mean(odor2_noact[:, i])
			# odor2_miss_mean[i] = np.mean(odor2_miss[:, i])


		print('odor2 fa', np.shape(odor2_hit))
		print('odor1 miss', np.shape(odor1_miss))
		# print('odor1 noact', np.shape(odor1_noact))
		oldwb = xlrd.open_workbook('result_20.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		sheet.write(0, k, file)
		if k == 0:
			test = odor2_hit
		else:
			test = np.vstack((test, odor2_hit))

#		for i in range(0,100):

		sheet.write(1, k, np.mean(odor1_hit_mean[100:115]))
		sheet.write(1 , k + 20, np.mean(odor1_m_mean[100:115]))
		sheet.write(5, k, np.mean(odor2_cr_mean[100:115]))
		sheet.write(5, k + 20, np.mean(odor2_hit_mean[100:115]))
		print(odor2_hit_mean[i])
		k += 1
		os.remove('result_20.xls')
		newwb.save('result_20.xls')

	t_mean = np.zeros(700)

	for i in range(700):
		t_mean[i] = np.mean(test[:,i])
	#print(np.shape(test))
	#print(t_mean[100:110])