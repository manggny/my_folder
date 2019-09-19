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


def div_by_cue(cal_time,cal_data,cue1,cue2,cue3,cue_hz):
	cue_interval = 1/cue_hz
	i = 0
	t = 0
	trial_start = 0
	change_cue1 = np.diff(cue1)
	cue1_trialnum = np.sum(np.abs(change_cue1)/2)
	#print(int(cue1_trialnum))
	change_cue2 = np.diff(cue2)
	cue2_trialnum = np.sum(np.abs(change_cue2) / 2)
	change_cue3 = np.diff(cue3)
	cue3_trialnum = np.sum(np.abs(change_cue3) / 2)
	print("tn",cue1_trialnum,cue2_trialnum,cue3_trialnum)
	cue1_cal = np.zeros((int(cue1_trialnum),700))
	cue2_cal = np.zeros((int(cue2_trialnum), 700))
	cue3_cal = np.zeros((int(cue2_trialnum), 700))
	now_cue1 = 0
	now_cue2 = 0
	now_cue3 = 0
	cue_ordor = []
	while i < np.alen(change_cue1):
		if change_cue1[i] == 1:
			trial_start = round(i/20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k])<=t and np.sum(cal_time[0:k+1])>t:
					if len(cal_data[k:k + 600]) < 600:
						cue1_cal = np.delete(cue1_cal,now_cue1,0)
						print('cue1' + str(now_cue1))
					else:
						cue1_cal[now_cue1, 0:100] = cal_data[k - 100:k]
						cue1_cal[now_cue1, 100:] = cal_data[k:k + 600]

			now_cue1 += 1
			cue_ordor.append(1)
			#print('1!')

		elif change_cue2[i] == 1:
			trial_start = round(i / 20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k]) <= t and np.sum(cal_time[0:k + 1]) > t:
					if len(cal_data[k:k + 600]) < 600:
						cue2_cal = np.delete(cue2_cal,now_cue2,0)
						print('cue2' + str(now_cue2))
					else:
						cue2_cal[now_cue2, 0:100] = cal_data[k - 100:k]
						cue2_cal[now_cue2, 100:] = cal_data[k:k + 600]
					# 	tw = len(cal_data[k:k + 600])
					#
					# except:
					# 	print(len(cue2_cal[now_cue2, 100:]), len(cal_data[k:k + 600]))
					#	continue

			now_cue2 += 1
			cue_ordor.append(2)
			#print('2!')

		elif change_cue3[i] == 1:
			trial_start = round(i / 20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k]) <= t and np.sum(cal_time[0:k + 1]) > t:
					if len(cal_data[k:k + 600]) < 600:
						cue3_cal = np.delete(cue3_cal,now_cue3,0)
						print('cue3' + str(now_cue3))
					else:
						cue3_cal[now_cue3, 0:100] = cal_data[k - 100:k]
						cue3_cal[now_cue3, 100:] = cal_data[k:k + 600]

			now_cue3 += 1
			cue_ordor.append(3)
		t += cue_interval
		i += 1
	#print(cue1_cal,np.mean(cue1_cal))
	#print(cue2_cal,np.mean(cue2_cal))
	return cue1_cal,cue2_cal,cue3_cal,cue_ordor

def z_score(whole,score):  #홀 은 전체 분포를 만들 데이터, 넘파이 like; score는 변환할 구체적 score들 넘파이 like
	whole_std = np.std(whole)
	whole_mean = np.mean(whole)
	if whole_std <=0.1:
		print(whole_std)
	z = np.zeros(np.alen(score))
	for i in range(np.alen(score)):
		z[i] = (score[i]-whole_mean)/whole_std
	return z

if __name__=="__main__":
	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/20_gonogo/after_ex/'
	result_path = 'F:/Insula-Gcamp6/record/result_pkl/20_gonogo/'

	result_name = result_path + 'all_AI_gonogo_20_record_mean_result'
	i = 0
	filelist = os.listdir(pkls_path)

	for files in filelist:
		data = unpickle(pkls_path + files)
		if i == 0:
			odor1 = data['odor1']
			odor2 = data['odor2']
			odor3 = data['odor3']
			i += 1
			continue
		else:
			odor1 = np.vstack((odor1,data['odor1']))
			odor2 = np.vstack((odor2, data['odor2']))
			odor3 = np.vstack((odor3, data['odor3']))

	for k in range(np.alen(odor1)):
		odor1[k,:] = z_score(odor1[k,0:100],odor1[k,:])
	for k in range(np.alen(odor2)):
		odor2[k,:] = z_score(odor2[k,0:100],odor2[k,:])
	for k in range(np.alen(odor3)):
		odor3[k,:] = z_score(odor3[k,0:100],odor3[k,:])

	cue1_mean_cal = np.zeros(700)
	cue1_error_cal = np.zeros(700)
	cue2_mean_cal = np.zeros(700)
	cue2_error_cal = np.zeros(700)
	cue3_mean_cal = np.zeros(700)
	cue3_error_cal = np.zeros(700)

	tr1,_ = np.shape(odor1)
	tr2, _ = np.shape(odor2)
	tr3, _ = np.shape(odor3)
	for k in range(700):
		cue1_mean_cal[k] = np.mean(odor1[:, k])
		cue1_error_cal[k] = np.std(odor1[:, k]) / np.sqrt(tr1)
		cue2_mean_cal[k] = np.mean(odor2[:, k])
		cue2_error_cal[k] = np.std(odor2[:, k]) / np.sqrt(tr2)
		cue3_mean_cal[k] = np.mean(odor3[:, k])
		cue3_error_cal[k] = np.std(odor3[:, k]) / np.sqrt(tr3)
	x1 = np.linspace(-2, 12, 700)
	print(np.mean(odor1[:,k]),tr2,tr3)
	plt.plot(x1, cue1_mean_cal, 'r', label='odor1')
	plt.fill_between(x1, cue1_mean_cal - cue1_error_cal, cue1_mean_cal + cue1_error_cal, alpha=0.3,
					 color='r')
	plt.plot(x1, cue2_mean_cal, 'b', label='odor2')
	plt.fill_between(x1, cue2_mean_cal - cue2_error_cal, cue2_mean_cal + cue2_error_cal, alpha=0.3,
					 color='b')
	# plt.plot(x1, cue3_mean_cal, 'g', label='odor3')
	# plt.fill_between(x1, cue3_mean_cal - cue3_error_cal, cue3_mean_cal + cue3_error_cal, alpha=0.3,
	# 				 color='g')

	plt.title('all_AI_gonogo_20_record_mean_result')
	plt.xlabel('Time(s)')
	plt.ylabel('Activate(z-score)')
	plt.legend(loc='upper right')
	plt.savefig(result_name+".png")
	plt.close()




