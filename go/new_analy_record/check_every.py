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

def finding_idx(cal,air):
	idx = -1
	behav_fre = 100
	cal_fre = 20
	d_air = np.diff(air)
	for i in range(air):
		if d_air[i] == 1:
			idx = np.floor(i/5)
			break

	return idx

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

	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_clean_no_nom/80/after_delete/goods/after_div/merged/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)


	k = 0

	for file in filelist:
		if file == '11':
			continue
		name,s = file.split('.')
		if s != 'pkl':
			continue
		print(name)
		data = unpickle(pkls_path + file)

		odor1_hit = data['odor1'][0]
		odor1_m = data['odor1'][1]
		odor2_fa = data['odor2'][0]
		odor2_cr = data['odor2'][1]
		#print(np.isnan(np.mean(odor1_hit,axis=0)))

		if np.alen(np.isnan(np.mean(odor1_hit,axis=0)))<100 and np.isnan(np.mean(odor1_hit,axis=0)):
			odor1_hit_mean = np.zeros(700)
		else:
			odor1_hit_mean = np.mean(odor1_hit,axis=0)

		if np.alen(np.isnan(np.mean(odor1_m,axis=0)))<100 and np.isnan(np.mean(odor1_m,axis=0)):
			odor1_m_mean = np.zeros(700)
		else:
			odor1_m_mean = np.mean(odor1_m,axis=0)

		if np.alen(np.isnan(np.mean(odor2_cr,axis=0)))<100 and np.isnan(np.mean(odor2_cr,axis=0)):
			odor2_cr_mean = np.zeros(700)
		else:
			odor2_cr_mean = np.mean(odor2_cr,axis=0)

		if np.alen(np.isnan(np.mean(odor2_fa,axis=0)))<100 and np.isnan(np.mean(odor2_fa,axis=0)):
			odor2_fa_mean = np.zeros(700)
		else:
			odor2_fa_mean = np.mean(odor2_fa,axis=0)

		print('odor2 fa', np.shape(odor2_fa))
		print('odor2 cr', np.shape(odor2_cr))
		print('odor1 miss', np.shape(odor1_m))
		print('odor1 hit', np.shape(odor1_hit))

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
		plt.plot(x1, odor2_fa_mean[0:300], 'g', label='odor2_fa') #[0:125]
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

