import numpy as np
import pickle as pkl
import sys, os

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
import matplotlib.pyplot as plt


def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data


if __name__ == "__main__":
	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_clean_no_nom/80/after_div/'
	result_path = pkls_path + '/merged/'

	#result_name = result_path + 'all(5)_AI_50%_-0.2-0.2_record_mean_result'
	file1='#gcam8_gonogo80record_d1_r(red)_left(blue)_190827_cleaned_r_behav.pkl'
	file2 = '#gcam8_gonogo80record_d2_r(red)_left(blue)_190828_cleaned_r_behav.pkl'
	#file3 = '#f2_gonogo80record__r(red)_left(blue)_190707_cleaned_r_behav.pkl'
	files = [file1,file2]#,file3]
	#file3 = '#f3_gonogo80record__r(red)_left(blue)_190708_opt_r_behav.pkl'
	pkls = []
	result_dic = {'odor1':[],'odor2':[]}

	for i in range(len(files)):
		data = unpickle(pkls_path + files[i])
		if i == 0:
			odor1_pump_trials = data['odor1'][0]
			odor1_nopump_trials = data['odor1'][1]
			#odor1_miss_trials = data['odor1'][2]
			odor2_pump_trials = data['odor2'][0]
			odor2_nopump_trials = data['odor2'][1]
			#odor2_miss_trials = data['odor2'][2]
			continue
		else:
			odor1_pump_trials = np.vstack((odor1_pump_trials,data['odor1'][0]))
			if np.alen(data['odor1'][1]) > 0:
				if np.alen(data['odor1'][1]) == 700:
					odor1_nopump_trials = np.vstack((odor1_nopump_trials,data['odor1'][1].reshape((1,700))))#odor1_nopump_trials.reshape(1,700)
				elif np.alen(odor1_nopump_trials) == 0:
					odor1_nopump_trials = data['odor1'][1]
				else:
					print(data['odor1'][1].shape,odor1_nopump_trials.shape)
					odor1_nopump_trials = np.vstack((odor1_nopump_trials,data['odor1'][1]))

			# if np.alen(data['odor1'][2]) > 0:
			# 	if np.alen(data['odor1'][2]) == 700:
			# 		odor1_miss_trials = np.vstack((odor1_miss_trials,data['odor1'][2].reshape((1,700))))#odor1_nopump_trials.reshape(1,700)
			# 	else:
			# 		odor1_miss_trials = np.vstack((odor1_miss_trials,data['odor1'][2]))

			if np.alen(data['odor2'][0]) > 0:
				odor2_pump_trials = np.vstack((odor2_pump_trials,data['odor2'][0]))
			if np.alen(data['odor2'][1]) > 0:
				odor2_nopump_trials = np.vstack((odor2_nopump_trials, data['odor2'][1]))
			#print(odor2_miss_trials.shape,data['odor2'][0].shape)
			# if np.alen(data['odor2'][2]) > 0:
			# 	odor2_miss_trials = np.vstack((odor2_miss_trials, data['odor2'][2]))


	#pkl3 = unpickle(pkls_path + file3)


	result_dic['odor1'].append(odor1_pump_trials)
	result_dic['odor1'].append(odor1_nopump_trials)
	# result_dic['odor1'].append(odor1_miss_trials)

	result_dic['odor2'].append(odor2_pump_trials)
	result_dic['odor2'].append(odor2_nopump_trials)
	# result_dic['odor2'].append(odor2_miss_trials)

	print('odor2 fa', np.shape(odor2_pump_trials))
	# print('odor1 noact', np.shape(odor1_miss_trials))
	print('odor1 nopump', np.shape(odor1_nopump_trials))
	print('odor1 hit', np.shape(odor1_pump_trials))
	print('odor2 cr', np.shape(odor2_nopump_trials))
	# print('odor2 cr2', np.shape(odor2_miss_trials))

	filename, _ =file1.split('.')

	output = open(result_path + filename + '_merged.pkl', 'wb')
	pkl.dump(result_dic, output)
	output.close()
