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

def finding_idx(air):
	idx = -1

	d_air = np.diff(air)
	for i in range(np.alen(air)):
		if d_air[i] == 1:
			idx = np.floor(i/2)
			break

	return int(idx)

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

	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/after_optimize/after_cleaning/after_delete/gonogo50/good/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)
	odor1_k = 0
	odor1_mk = 0
	odor2_k = 0
	odor2_mk = 0
	odor1_noact_k = 0



	for file in filelist:
		k = 0
		if file == '11':
			continue
		name,s = file.split('.')
		if s != 'pkl':
			continue
		print(file)

		data = unpickle(pkls_path + file)

		lick = data['lick']
		pump = data['pump']
		odor_list = data['odor_order']
		airpuff = data['air']
		cal = data['cal_data']
		print(cal.shape)




		odor2_air_mean = np.zeros(300)
		for i in range(len(odor_list)):

			if odor_list[i] == 2 and np.sum(airpuff[i,:]) > 10:
				idx = finding_idx(airpuff[i,:])
				#print(cal[i, (idx - 100):(idx + 200)])
				if k == 0:
					odor2_air = cal[i,idx-100:idx+200]
				else:
					odor2_air=np.vstack((odor2_air, cal[i,idx-100:idx+200]))
				k += 1
				#print(idx)

		tr,*ti = np.shape(odor2_air)

		if np.alen(odor2_air) > 0 and np.alen(odor2_air) < 700:
			for i in range(300):
				odor2_air_mean[i] = np.mean(odor2_air[:,i])
			x1 = np.linspace(-2, 4, 300)
			plt.plot(x1, odor2_air_mean, 'r', label='odor2_air')
			plt.show()
		else:
			continue




		#
		# plt.plot(x1, odor1_hit_mean[0:300], 'r', label='odor1_hit')
		# # plt.fill_between(x1, all_odor1_hit_mean, all_odor1_hit_mean + all_odor1_hit_error, alpha=0.3,
		# # 				 color='r')
		# plt.plot(x1, odor1_m_mean[0:300], 'b', label='odor1_miss')
		# # plt.fill_between(x1, all_odor1_m_mean - all_odor1_m_error, all_odor1_m_mean + all_odor1_m_error, alpha=0.3,
		# # 				 color='b')
		# plt.plot(x1, odor2_cr_mean[0:300], 'y', label='odor2_cr')
		# # plt.fill_between(x1, all_odor2_cr_mean - all_odor2_cr_error, all_odor2_cr_mean + all_odor2_cr_error, alpha=0.3,
		# # 				 color='y')
		# plt.plot(x1, odor2_hit_mean[0:300], 'g', label='odor2_fa') #[0:125]
		# # plt.fill_between(x1, all_odor2_hit_mean - all_odor2_hit_error, all_odor2_hit_mean + all_odor2_hit_error, alpha=0.3,
		# # 				 color='g')
		# #plt.plot(x1, all_odor1_noact_mean[0:125], 'p', label='odor1_noact')
		#
		# plt.xlabel('Time(s)')
		# plt.ylabel('z-score')
		# plt.legend(loc='upper right')
		# plt.show()
		# # print(np.shape(all_odor2_cr),np.shape(all_odor2_hit))
		# 	#plt.savefig(f_name + "left.png")
		# 	#plt.close()
		#
