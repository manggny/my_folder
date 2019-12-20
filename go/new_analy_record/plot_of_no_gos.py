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

	pkls_path_20 = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_clean_no_nom/80/after_div/merged/'
	pkls_path_50 = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_clean_no_nom/50/after_div/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'

	for i in range(2):
		if i == 0:
			file_path = pkls_path_20
			filelist = os.listdir(pkls_path_20)
		else:
			file_path = pkls_path_50
			filelist = os.listdir(pkls_path_50)
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

			data = unpickle(file_path + file)

			odor1_hit = data['odor1'][0]
			odor1_m = data['odor1'][1]
			odor2_fa = data['odor2'][0]
			odor2_cr = data['odor2'][1]
			# print(np.isnan(np.mean(odor1_hit,axis=0)))

			if np.alen(np.isnan(np.mean(odor1_hit, axis=0))) < 100 and np.isnan(np.mean(odor1_hit, axis=0)):
				odor1_hit_mean = np.zeros(700)
			elif np.alen(odor1_hit) == 700:
				odor1_hit_mean = odor1_hit
			else:
				odor1_hit_mean = np.mean(odor1_hit, axis=0)

			if np.alen(np.isnan(np.mean(odor1_m, axis=0))) < 100 and np.isnan(np.mean(odor1_m, axis=0)):
				odor1_m_mean = np.zeros(700)
			elif np.alen(odor1_m) == 700:
				odor1_m_mean = odor1_m
			else:
				odor1_m_mean = np.mean(odor1_m, axis=0)

			if np.alen(np.isnan(np.mean(odor2_cr, axis=0))) < 100 and np.isnan(np.mean(odor2_cr, axis=0)):
				odor2_cr_mean = np.zeros(700)
			elif np.alen(odor2_cr) == 700:
				odor2_cr_mean = odor2_cr
			else:
				odor2_cr_mean = np.mean(odor2_cr, axis=0)

			if np.alen(np.isnan(np.mean(odor2_fa, axis=0))) < 100 and np.isnan(np.mean(odor2_fa, axis=0)):
				odor2_fa_mean = np.zeros(700)
			elif np.alen(odor2_fa) == 700:
				odor2_fa_mean = odor2_fa
			else:
				odor2_fa_mean = np.mean(odor2_fa, axis=0)



				# odor2_noact_mean[i] = np.mean(odor2_noact[:, i])
				# odor2_miss_mean[i] = np.mean(odor2_miss[:, i])
			#

			print(np.alen(odor1_m))

			if k == 0:
				all_odor1_hit = odor1_hit_mean
				all_odor1_m = odor1_m_mean
				all_odor2_hit = odor2_fa_mean
				all_odor2_cr = odor2_cr_mean
			else:
				all_odor1_hit = np.vstack((all_odor1_hit,odor1_hit_mean))
				# print(np.shape(all_odor1_m),np.shape(odor1_m_mean))
				# print(odor1_m_mean)
				if np.max(odor1_m_mean) > 0:
					all_odor1_m = np.vstack((all_odor1_m, odor1_m_mean))
				all_odor2_hit = np.vstack((all_odor2_hit, odor2_fa_mean))
				all_odor2_cr = np.vstack((all_odor2_cr, odor2_cr_mean))

			k += 1
			print(file,np.shape(odor2_cr))


	#
	# print(np.alen(all_odor1_hit))
		for k in range(700):
			all_odor1_hit_error[k] = np.std(all_odor1_hit[:, k]) / np.sqrt(np.alen(all_odor1_hit))
			all_odor1_m_error[k] = np.std(all_odor1_m[:, k]) / np.sqrt(np.alen(all_odor1_m))
			all_odor2_cr_error[k] = np.std(all_odor2_cr[:, k]) / np.sqrt(np.alen(all_odor2_cr))
			all_odor2_hit_error[k] = np.std(all_odor2_hit[:, k]) / np.sqrt(np.alen(all_odor2_hit))
		print(np.shape(all_odor2_cr))
		all_odor1_hit_mean = np.mean(all_odor1_hit,axis=0)
		all_odor1_m_mean = np.mean(all_odor1_m,axis=0)
		print(all_odor2_cr[7,0:300])
		all_odor2_cr_mean = np.mean(all_odor2_cr,axis=0)
		all_odor2_hit_mean = np.mean(all_odor2_hit,axis=0)
		endpoint = 150
		x1 = np.linspace(-2, 2, endpoint)

	# plt.plot(x1, all_odor1_hit_mean[0:300], 'r', label='odor1_hit')
	# plt.fill_between(x1, all_odor1_hit_mean[0:300] - all_odor1_hit_error[0:300], all_odor1_hit_mean[0:300] + all_odor1_hit_error[0:300], alpha=0.3,
	# 				 color='r')
	# plt.plot(x1, all_odor1_m_mean[0:300], 'b', label='odor1_miss')
	# plt.fill_between(x1, all_odor1_m_mean[0:300] - all_odor1_m_error[0:300], all_odor1_m_mean[0:300] + all_odor1_m_error[0:300], alpha=0.3,
	# 				 color='b')

		if i == 0:
			plt.plot(x1, all_odor2_cr_mean[0:endpoint], 'r', label='20% cr')
			plt.fill_between(x1, all_odor2_cr_mean[0:endpoint] - all_odor2_cr_error[0:endpoint], all_odor2_cr_mean[0:endpoint] + all_odor2_cr_error[0:endpoint], alpha=0.3,
							 color='r')
			plt.plot(x1, all_odor2_hit_mean[0:endpoint], 'b', label='20% fa') #[0:125]
			plt.fill_between(x1, all_odor2_hit_mean[0:endpoint] - all_odor2_hit_error[0:endpoint], all_odor2_hit_mean[0:endpoint] + all_odor2_hit_error[0:endpoint], alpha=0.3,
						 color='b')
		else:
			plt.plot(x1, all_odor2_cr_mean[0:endpoint], 'y', label='50% cr')
			plt.fill_between(x1, all_odor2_cr_mean[0:endpoint] - all_odor2_cr_error[0:endpoint],
							 all_odor2_cr_mean[0:endpoint] + all_odor2_cr_error[0:endpoint], alpha=0.3,
							 color='y')
			plt.plot(x1, all_odor2_hit_mean[0:endpoint], 'g', label='50% fa')  # [0:125]
			plt.fill_between(x1, all_odor2_hit_mean[0:endpoint] - all_odor2_hit_error[0:endpoint],
							 all_odor2_hit_mean[0:endpoint] + all_odor2_hit_error[0:endpoint], alpha=0.3,
							 color='g')

	#plt.plot(x1, all_odor1_noact_mean[0:125], 'p', label='odor1_noact')

	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.show()
#	print(np.shape(all_odor2_cr),np.shape(all_odor2_hit))
		#plt.savefig(f_name + "left.png")
		#plt.close()

