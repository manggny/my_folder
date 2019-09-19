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


def load_tdms(cue_pkl_name,cal_pkl_name):
	cue_pkl_file = open(cue_pkl_name, 'rb')
	event = pkl.load(cue_pkl_file)
	cal_pkl_file = open(cal_pkl_name, 'rb')
	cal = pkl.load(cal_pkl_file)
	cue_group = event.groups()
	cue_channels = event.group_channels(cue_group[0])
	cue_channels_data = []
	for i in cue_channels:
		c = i
		c = c.path.split('/')
		c= c[2].replace("'","")
		cue_channels_data.append(event.channel_data(cue_group[0],c))


	cal_group = cal.groups()
	cal_channels = cal.group_channels(cal_group[0])
	cal_channels_data = []
	for i in cal_channels:
		c = i
		c = c.path.split('/')
		c = c[2].replace("'", "")
		cal_channels_data.append(cal.channel_data(cal_group[0], c))


	return cue_channels_data,cal_channels_data


if __name__=="__main__":
	pkls_path = 'F:/Insula-Gcamp6/record/result_pkl/20_gonogo/'
	result_path = 'F:/Insula-Gcamp6/record/result_pkl/20_gonogo/after_ex/'

	cue_file = '#f1_gonogo80record__r(red)_left(blue,weak)_190705-Event.pkl'
	cal_file = '#f1_gonogo80record__r(red)_left(blue,weak)_190705.pkl'

	cuename = pkls_path+cue_file
	calname = pkls_path+cal_file

	cue, cal = load_tdms(cuename, calname)
	cue1_cal_l, cue2_cal_l, cue3_cal_l, trial_ordor_l = div_by_cue(cal[0], cal[3], cue[1], cue[2], cue[3], 1000)
	cue1_cal_r, cue2_cal_r, cue3_cal_r, trial_ordor_r = div_by_cue(cal[0], cal[2], cue[1], cue[2], cue[3], 1000)

	all_result_l = {'odor1': cue1_cal_l, 'odor2': cue2_cal_l, 'odor3': cue3_cal_l}
	all_result_r = {'odor1': cue1_cal_r, 'odor2': cue2_cal_r, 'odor3': cue3_cal_r}
	namel = result_path+'l_'+cal_file
	namer =result_path+'r_'+cal_file

	output = open(namel, 'wb')
	pkl.dump(all_result_l, output)
	output.close()

	output = open(namer, 'wb')
	pkl.dump(all_result_r, output)
	output.close()
