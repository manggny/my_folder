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

if __name__=="__main__":
	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_50%/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'


	result_name = result_path + 'all(5)_AI_50%_-0.2-0.2_record_mean_result'

	all_result = {'odor1':[],'odor2':[]}

	filelist = os.listdir(pkls_path)
	num_files = 0
	odor1_hit = []
	odor1_miss = []
	odor1_noact = []
	odor2_hit = []
	odor2_miss = []
	odor2_noact = []
	for files in filelist:
		odor1_trials = 0
		odor2_trials = 0
		print(files)
		name,s = files.split('.')
		print(s)
		if s != 'pkl':
			print(11)
			continue

		data = unpickle(pkls_path+files)
		num_files += 1
		print(type(data['odor1'][0]))
		tr0,tr1,tr2 = 0,0,0
		if np.ndim(data['odor1'][0]) > 1:
			tr0,*_ = np.shape(data['odor1'][0])
			#print(type(np.ndim(data['odor1'][0])))
		if np.ndim(data['odor1'][1])>1:
			tr1, *_ = np.shape(data['odor1'][1])
			#print(np.ndim(data['odor1'][1]))
		if np.ndim(data['odor1'][2])>1:
			tr2, *_ = np.shape(data['odor1'][2])
			#print(np.ndim(data['odor1'][2]))
		odor1_trials = tr0 + tr1 + tr2

		tr0, tr1, tr2 = 0, 0, 0
		if np.ndim(data['odor2'][0])>1:
			tr0,*_ = np.shape(data['odor2'][0])
		if np.ndim(data['odor2'][1])>1:
			tr1, *_ = np.shape(data['odor2'][1])
		if np.ndim(data['odor2'][2])>1:
			tr2, *_ = np.shape(data['odor2'][2])
		odor2_trials = tr0 + tr1 + tr2

		print('odor1 trials of'+files+' is', odor1_trials)
		print('odor2 trials of' + files + ' is', odor2_trials)



		for i in range(3):
			if len(data['odor1'][i]) == 0:
				print(data['odor1'][i])
				print('odor1, data length is ', len(data['odor1'][i]), i)
				#all_result['odor1'].append(np.array([]))
				continue
			else:
				if i == 0:
					odor1_hit.append(data['odor1'][i])
				elif i == 1:
					odor1_miss.append(data['odor1'][i])
				elif i == 2:
					odor1_miss.append(data['odor1'][i])
					#odor1_noact.append(data['odor1'][i])

		for i in range(3):
			if len(data['odor2'][i]) == 0:
				print('odor2, data length is ', len(data['odor2'][i]), i)
				#all_result['odor1'].append(np.array([]))
				continue
			else:
				if i == 0:
					odor2_hit.append(data['odor2'][i])
				elif i == 1:
					odor2_miss.append(data['odor2'][i])
				elif i == 2:
					odor2_miss.append(data['odor2'][i])
					#odor2_noact.append(data['odor2'][i])

	for i in range(len(odor1_hit)):
		if i == 0:
			all_result['odor1'].append(odor1_hit[i])
		else:
			all_result['odor1'][0] = np.vstack((all_result['odor1'][0], odor1_hit[i]))

	for i in range(len(odor1_miss)):
		if i == 0:
			all_result['odor1'].append(odor1_miss[i])
		else:
			all_result['odor1'][1] = np.vstack((all_result['odor1'][1], odor1_miss[i]))

	# for i in range(len(odor1_noact)):
	# 	if i == 0:
	# 		all_result['odor1'].append(odor1_noact[i])
	# 	else:
	# 		all_result['odor1'][2] = np.vstack((all_result['odor1'][2], odor1_noact[i]))

	for i in range(len(odor2_hit)):
		if i == 0:
			all_result['odor2'].append(odor2_hit[i])
		else:
			all_result['odor2'][0] = np.vstack((all_result['odor2'][0], odor2_hit[i]))

	for i in range(len(odor2_miss)):
		if i == 0:
			all_result['odor2'].append(odor2_miss[i])
		else:
			all_result['odor2'][1] = np.vstack((all_result['odor2'][1], odor2_miss[i]))

	# for i in range(len(odor2_noact)):
	# 	if i == 0:
	# 		all_result['odor2'].append(odor2_noact[i])
	# 	else:
	# 		all_result['odor2'][2] = np.vstack((all_result['odor2'][2], odor2_noact[i]))



	print(all_result['odor1'][0].shape)
	print(all_result['odor2'][0].shape)
	print(all_result['odor1'][1].shape)
	print(all_result['odor2'][1].shape)
	# print(all_result['odor1'][2].shape)
	# print(all_result['odor2'][2].shape)
	print(len(all_result['odor2']))

	print('file nums ',num_files)

	trial_start = 90
	trial_end = 110
	trial_time = trial_end-trial_start
	odor1_hit_mean = np.zeros(trial_time)
	odor1_miss_behav_mean = np.zeros(trial_time)
	odor1_noact_mean = np.zeros(trial_time)
	odor2_hit_mean = np.zeros(trial_time)
	odor2_miss_behav_mean = np.zeros(trial_time)
	odor2_noact_mean = np.zeros(trial_time)
	x1 = np.linspace(-0.2,0.2, trial_time)
	odor1_hit_error = np.zeros(trial_time)
	odor1_miss_error = np.zeros(trial_time)
	odor2_hit_error = np.zeros(trial_time)
	odor2_miss_error = np.zeros(trial_time)

	#go_error.append(np.std(bins_golick_range[:, i]) / np.sqrt(tr))
	tr1,*_ = np.shape(all_result['odor1'][0])
	mtr1, *_ = np.shape(all_result['odor1'][1])
	tr2, *_ = np.shape(all_result['odor2'][0])
	mtr2, *_ = np.shape(all_result['odor2'][1])

	for k in range(trial_time):
		odor1_hit_mean[k] = np.mean(all_result['odor1'][0][:,trial_start+k])
		odor1_hit_error[k] = np.std(all_result['odor1'][0][:, trial_start+k]) / np.sqrt(tr1)
		odor1_miss_behav_mean[k] = np.mean(all_result['odor1'][1][:,trial_start+k])
		odor1_miss_error[k] = np.std(all_result['odor1'][1][:, trial_start + k]) / np.sqrt(mtr1)
		# odor1_noact_mean[k] = np.mean(all_result['odor1'][2][:,trial_start+k])
		odor2_hit_mean[k] = np.mean(all_result['odor2'][0][:,trial_start+k])
		odor2_hit_error[k] = np.std(all_result['odor2'][0][:, trial_start + k]) / np.sqrt(tr2)
		odor2_miss_behav_mean[k] = np.mean(all_result['odor2'][1][:,trial_start+k])
		odor2_miss_error[k] = np.std(all_result['odor2'][1][:, trial_start + k]) / np.sqrt(mtr2)
		# odor2_noact_mean[k] = np.mean(all_result['odor2'][2][:,trial_start+k])
	# print(odor2_hit.shape)
	# print(odor2_miss.shape)
	# print(odor2_noact.shape)


	plt.plot(x1, odor1_hit_mean, 'r', label='odor1_hit')
	plt.fill_between(x1, odor1_hit_mean - odor1_hit_error, odor1_hit_mean + odor1_hit_error, alpha=0.3, color='r')
	plt.plot(x1, odor1_miss_behav_mean, 'b', label='odor1_miss_act')
	plt.fill_between(x1, odor1_miss_behav_mean - odor1_miss_error, odor1_miss_behav_mean + odor1_miss_error, alpha=0.3, color='b')
	# plt.plot(x1, odor1_noact_mean, 'g', label='odor1_noact')
	plt.plot([0, 0], [0, np.max(odor1_hit_mean)], 'k--', linewidth=1, color='red')

	
	plt.title("_")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(result_name + "_odor1.png")
	plt.close()

	plt.plot(x1, odor2_hit_mean, 'r', label='odor2_fa')
	plt.fill_between(x1, odor2_hit_mean - odor2_hit_error, odor2_hit_mean + odor2_hit_error, alpha=0.3, color='r')
	plt.plot(x1, odor2_miss_behav_mean, 'b', label='odor2_cr_act')
	plt.fill_between(x1, odor2_miss_behav_mean - odor2_miss_error, odor2_miss_behav_mean + odor2_miss_error, alpha=0.3, color='b')
	# plt.plot(x1, odor2_noact_mean, 'g', label='odor2_cr_noact')
	plt.plot([0, 0], [0, np.max(odor2_hit_mean)], 'k--', linewidth=1, color='red')

	plt.title("_")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(result_name + "_odor2.png")
	plt.close()



