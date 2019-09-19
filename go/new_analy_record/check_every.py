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

def normalizing(trial_data):
	f0 = np.median(trial_data)
	result = np.zeros(len(trial_data))
	for i in range(len(trial_data)):
		result[i] = (trial_data[i]-f0)/trial_data[i]
	return result

def normalizing_p(trial_data,part):
	f0 = np.median(part)
	result = np.zeros(len(trial_data))
	for i in range(len(trial_data)):
		result[i] = (trial_data[i]-f0)/trial_data[i]
	return result


if __name__=="__main__":
	test = np.zeros(700)

	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/after_optimize/after_cleaning/after_delete/gonogo20/after_behav/goods/merged/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)
	odor1_k = 0
	odor1_mk = 0
	odor2_k = 0
	odor2_mk = 0
	odor1_noact_k = 0
	all_odor1_hit_mean = np.zeros(700)
	all_odor1_hit_error = np.zeros(700)
	odor1_hit_error = np.zeros(700)
	all_odor1_m_mean = np.zeros(700)
	all_odor1_m_error = np.zeros(700)
	odor1_m_error = np.zeros(700)
	all_odor2_cr_mean = np.zeros(700)
	all_odor2_cr_error = np.zeros(700)
	odor2_cr_error = np.zeros(700)
	all_odor2_hit_mean = np.zeros(700)
	all_odor2_hit_error = np.zeros(700)
	odor2_hit_error = np.zeros(700)
	all_odor1_noact_mean = np.zeros(700)
	k = 0

	for file in filelist:
		if file == '11':
			continue
		name,s = file.split('.')
		if s != 'pkl':
			continue

		data = unpickle(pkls_path + file)

		odor1_hit = data['odor1'][0]
		odor1_hit_mean=np.zeros(700)
		odor2_hit_mean = np.zeros(700)
		odor2_noact_mean = np.zeros(700)
		odor2_miss_mean = np.zeros(700)
		odor1_noact_mean = np.zeros(700)

		tr,ti = odor1_hit.shape

		odor1_miss = data['odor1'][1]
		#odor1_noact = data['odor1'][2]
		odor2_hit = data['odor2'][0]
		odor2_miss = data['odor2'][1]
		#odor2_noact = data['odor2'][2]
		#tr2,*_ = odor2_noact.shape
		tr3,*_ = odor2_miss.shape

		# if tr2 == 0:
		odor2_cr = odor2_miss
		# elif tr3 == 0:
		# 	odor2_cr = odor2_noact
		# else:
		# 	odor2_cr = np.vstack((odor2_miss,odor2_noact))



		#odor1_m = np.zeros(700)
		# tr2, *_ = odor1_noact.shape
		tr3, *_ = odor1_miss.shape
		odor1_m = odor1_miss
		# if np.ndim(odor1_noact)>1 and np.ndim(odor1_miss) > 1:
		# 	tr2, ti2 = odor1_noact.shape
		# 	tr3, ti3 = odor1_miss.shape
		# 	if tr2 == 0 or ti2 == 0:
		# 		odor1_m = odor1_miss
		# 	elif tr3 ==0 or ti3 == 0:
		# 		odor1_m = odor1_noact
		# 	else:
		# 		odor1_m = np.vstack((odor1_miss, odor1_noact))


		# elif np.ndim(odor1_noact)<2:
		# 	odor1_m = odor1_miss
		# elif  np.ndim(odor1_miss)<2:
		# 	odor1_m = odor1_noact

		odor2_cr_mean = np.zeros(700)
		odor1_m_mean = np.zeros(700)
		odor1_miss_mean = np.zeros(700)
		tr,*_ = np.shape(odor1_miss)
		ntr,*_ = np.shape(odor2_hit)
		print(file)
		# for i in range(ntr):
		# 	print(odor1_m[i,100:110])
		for i in range(np.alen(odor1_hit)):
			odor1_hit[i,:] = normalizing_p(odor1_hit[i,:],odor1_hit[i,0:100])
		for i in range(np.alen(odor1_m)):
			odor1_m[i, :] = normalizing_p(odor1_m[i,:],odor1_m[i, 0:100])
		for i in range(np.alen(odor2_cr)):
			odor2_cr[i, :] = normalizing_p(odor2_cr[i,:],odor2_cr[i, 0:100])

		t,*q = np.shape(odor2_hit)
		print(odor2_hit.shape)
		if t == 700:
			odor2_hit[:] = normalizing_p(odor2_hit[:], odor2_hit[0:100])
		else:
			for i in range(t):
				odor2_hit[i, :] = normalizing_p(odor2_hit[i,:],odor2_hit[i, 0:100])
		print('odor2 fa', np.shape(odor2_hit))
		print('odor2 cr', np.shape(odor2_cr))
		print('odor1 miss', np.shape(odor1_m))
		print('odor1 hit', np.shape(odor1_hit))

		if tr3 != 0 and np.alen(odor1_miss) < 100:
			#print(odor1_noact.shape)
			odor1_noact_k += 1
			for i in range(ti):
				odor1_noact_mean[i] = np.mean(odor1_miss[:, i])

		for i in range(ti):

			odor1_hit_mean[i] = np.mean(odor1_hit[:,i])
						#print(odor1_m.shape)
			if np.alen(odor1_m) == 0:
				odor1_m_mean = np.array([])
			else:
				odor1_m_mean[i] = np.mean(odor1_m[:, i])

			# if tr > 0 and tr < 200:
			# 	odor1_miss_mean[i] = np.mean(odor1_miss[:, i])
			if t == 700:
				odor2_hit_mean[i] = odor2_hit[i]
			else:
				odor2_hit_mean[i] = np.mean(odor2_hit[:,i])

			odor2_cr_mean[i] = np.mean(odor2_cr[:,i])

		if np.alen(odor1_m) > 0:
			odor1_mk += 1
		odor2_k += 1
		odor2_mk += 1
		odor1_k += 1
			# odor2_noact_mean[i] = np.mean(odor2_noact[:, i])
			# odor2_miss_mean[i] = np.mean(odor2_miss[:, i])

		x1 = np.linspace(-2, 4, 300)

		plt.plot(x1, odor1_hit_mean[0:300], 'r', label='odor1_hit')
		# plt.fill_between(x1, all_odor1_hit_mean, all_odor1_hit_mean + all_odor1_hit_error, alpha=0.3,
		# 				 color='r')
		plt.plot(x1, odor1_m_mean[0:300], 'b', label='odor1_miss')
		# plt.fill_between(x1, all_odor1_m_mean - all_odor1_m_error, all_odor1_m_mean + all_odor1_m_error, alpha=0.3,
		# 				 color='b')
		plt.plot(x1, odor2_cr_mean[0:300], 'y', label='odor2_cr')
		# plt.fill_between(x1, all_odor2_cr_mean - all_odor2_cr_error, all_odor2_cr_mean + all_odor2_cr_error, alpha=0.3,
		# 				 color='y')
		plt.plot(x1, odor2_hit_mean[0:300], 'g', label='odor2_fa') #[0:125]
		# plt.fill_between(x1, all_odor2_hit_mean - all_odor2_hit_error, all_odor2_hit_mean + all_odor2_hit_error, alpha=0.3,
		# 				 color='g')
		#plt.plot(x1, all_odor1_noact_mean[0:125], 'p', label='odor1_noact')

		plt.xlabel('Time(s)')
		plt.ylabel('z-score')
		plt.legend(loc='upper right')
		plt.show()
		# print(np.shape(all_odor2_cr),np.shape(all_odor2_hit))
			#plt.savefig(f_name + "left.png")
			#plt.close()

