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
	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/pkls_licks/confilct/befor/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_20%/'

	#result_name = result_path + 'all(5)_AI_50%_-0.2-0.2_record_mean_result'
	file1='#f3_gonogo80record__r(red)_left(blue)_190708_l.pkl'
	file2 = '#f3_gonogo80record__r(red)_left(blue)_190706_l.pkl'
	file3 = '#f3_gonogo80record__r(red)_left(blue)_190707_l.pkl'
	pkl1 = unpickle(pkls_path + file1)
	pkl2 = unpickle(pkls_path + file2)
	pkl3 = unpickle(pkls_path + file3)

	result_dic = {'odor1': [], 'odor2': [], 'odor1_lick': [], 'odor2_lick': [], 'odor1_pre': [], 'odor2_pre': []}
	print(np.shape(pkl1['odor1_pre'][2]),np.shape(pkl2['odor1_pre'][2]),np.shape(pkl3['odor1_pre'][2]))
	odor1_pump_trials = np.vstack((pkl1['odor1'][0], pkl2['odor1'][0], pkl3['odor1'][0]))  # 0 for no-react, 1 for hit in odor1/2 trials
	odor1_pump_licks = np.vstack((pkl1['odor1_lick'][0], pkl2['odor1_lick'][0], pkl3['odor1_lick'][0]))
	pkl1['odor1_pre'][0].extend(pkl2['odor1_pre'][0])
	pkl1['odor1_pre'][0].extend(pkl3['odor1_pre'][0])
	odor1_pump_pre = pkl1['odor1_pre'][0]
	print(odor1_pump_trials.shape,len(odor1_pump_pre),odor1_pump_licks.shape)

	odor1_nopump_trials = np.vstack((pkl1['odor1'][1], pkl2['odor1'][1], pkl3['odor1'][1]))  # or airpuff
	odor1_nopump_licks = np.vstack((pkl1['odor1_lick'][1], pkl2['odor1_lick'][1], pkl3['odor1_lick'][1]))
	pkl1['odor1_pre'][1].extend(pkl2['odor1_pre'][1])
	pkl1['odor1_pre'][1].extend(pkl3['odor1_pre'][1])
	odor1_nopump_pre = pkl1['odor1_pre'][1]

	odor1_miss_trials = pkl2['odor1'][2]
	#odor1_miss_trials = np.vstack((pkl1['odor1'][2], pkl2['odor1'][2],pkl3['odor1'][2])) # trials no-react at all
	odor1_miss_licks = pkl2['odor1_lick'][2]
	#odor1_miss_licks = np.vstack((pkl1['odor1_lick'][2], pkl2['odor1_lick'][2],pkl3['odor1_lick'][2]))
	pkl1['odor1_pre'][2].extend(pkl2['odor1_pre'][2])
	pkl1['odor1_pre'][2].extend(pkl3['odor1_pre'][2])
	odor1_miss_pre = pkl1['odor1_pre'][2]
	#odor1_miss_pre = np.hstack((pkl1['odor1_pre'][2], pkl2['odor1_pre'][2],pkl3['odor1_pre'][2]))

	odor2_pump_trials = np.vstack(
		(pkl1['odor2'][0], pkl2['odor2'][0], pkl3['odor2'][0]))  # 0 for no-react, 1 for hit in odor1/2 trials
	odor2_pump_licks = np.vstack((pkl1['odor2_lick'][0], pkl2['odor2_lick'][0],pkl3['odor2_lick'][0]))
	pkl1['odor2_pre'][0].extend(pkl2['odor2_pre'][0])
	pkl1['odor2_pre'][0].extend(pkl3['odor2_pre'][0])
	odor2_pump_pre = pkl1['odor2_pre'][0]

	odor2_nopump_trials = np.vstack((pkl1['odor2'][1], pkl2['odor2'][1], pkl3['odor2'][1]))  # or airpuff
	odor2_nopump_licks = np.vstack((pkl1['odor2_lick'][1], pkl2['odor2_lick'][1], pkl3['odor2_lick'][1]))
	pkl1['odor2_pre'][1].extend(pkl2['odor2_pre'][1])
	pkl1['odor2_pre'][1].extend(pkl3['odor2_pre'][1])
	odor2_nopump_pre = pkl1['odor2_pre'][1]

	odor2_miss_trials = np.vstack((pkl1['odor2'][2], pkl2['odor2'][2], pkl3['odor2'][2]))  # trials no-react at all
	odor2_miss_licks = np.vstack((pkl1['odor2_lick'][2], pkl2['odor2_lick'][2], pkl3['odor2_lick'][2]))
	pkl1['odor2_pre'][2].extend(pkl2['odor2_pre'][2])
	pkl1['odor2_pre'][2].extend(pkl3['odor2_pre'][2])
	odor2_miss_pre = pkl1['odor2_pre'][2]

	result_dic['odor1'].append(odor1_pump_trials)
	result_dic['odor1'].append(odor1_nopump_trials)
	result_dic['odor1'].append(odor1_miss_trials)
	result_dic['odor1_lick'].append(odor1_pump_licks)
	result_dic['odor1_lick'].append(odor1_nopump_licks)
	result_dic['odor1_lick'].append(odor1_miss_licks)
	result_dic['odor1_pre'].append(odor1_pump_pre)
	result_dic['odor1_pre'].append(odor1_nopump_pre)
	result_dic['odor1_pre'].append(odor1_miss_pre)
	result_dic['odor2'].append(odor2_pump_trials)
	result_dic['odor2'].append(odor2_nopump_trials)
	result_dic['odor2'].append(odor2_miss_trials)
	result_dic['odor2_lick'].append(odor2_pump_licks)
	result_dic['odor2_lick'].append(odor2_nopump_licks)
	result_dic['odor2_lick'].append(odor2_miss_licks)
	result_dic['odor2_pre'].append(odor2_pump_pre)
	result_dic['odor2_pre'].append(odor2_nopump_pre)
	result_dic['odor2_pre'].append(odor2_miss_pre)

	filename, _ =file1.split('.')

	output = open(result_path + filename + '.pkl', 'wb')
	pkl.dump(result_dic, output)
	output.close()
