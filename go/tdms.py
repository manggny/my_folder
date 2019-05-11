from nptdms import TdmsFile
import numpy as np
import pickle as pkl
import sys, os
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list_record,make_list,raster
from go.funcs import div_by_laser,make_gonogolick_ordor,div_by_odor_record,div_by_odor
import matplotlib.pyplot as plt

def z_score(whole,score):  #홀 은 전체 분포를 만들 데이터, 넘파이 like; score는 변환할 구체적 score들 넘파이 like
	whole_std = np.std(whole)
	whole_mean = np.mean(whole)
	z = np.zeros(np.alen(score))
	for i in range(np.alen(score)):
		print(whole_std)
		z[i] = (score[i]-whole_mean)/whole_std
	return z

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

def div_by_cue(cal_time,cal_data,cue1,cue2,cue_hz):
	cue_interval = 1/cue_hz
	i = 0
	t = 0
	trial_start = 0
	change_cue1 = np.diff(cue1)
	cue1_trialnum = np.sum(np.abs(change_cue1)/2)
	#print(int(cue1_trialnum))
	change_cue2 = np.diff(cue2)
	cue2_trialnum = np.sum(np.abs(change_cue2) / 2)
	print("tn",cue1_trialnum,cue2_trialnum)
	cue1_cal = np.zeros((int(cue1_trialnum),700))
	cue2_cal = np.zeros((int(cue2_trialnum), 700))
	now_cue1 = 0
	now_cue2 = 0
	cue_ordor = []
	while i < np.alen(change_cue1):
		if change_cue1[i] == 1:
			trial_start = round(i/20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k])<=t and np.sum(cal_time[0:k+1])>t:
					cue1_cal[now_cue1,0:100] = cal_data[k-100:k]
					try:
						cue1_cal[now_cue1,100:700] = cal_data[k:k+600]
					except:
						continue
			now_cue1 += 1
			cue_ordor.append(1)
			#print('1!')

		elif change_cue2[i] == 1:
			trial_start = round(i / 20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k]) <= t and np.sum(cal_time[0:k + 1]) > t:
					cue2_cal[now_cue2, 0:100] = cal_data[k - 100:k]
					try:
						cue2_cal[now_cue2, 100:700] = cal_data[k:k + 600]
					except:
						continue

			now_cue2 += 1
			cue_ordor.append(2)
			#print('2!')

		t += cue_interval
		i += 1
	#print(cue1_cal,np.mean(cue1_cal))
	#print(cue2_cal,np.mean(cue2_cal))
	return cue1_cal,cue2_cal,cue_ordor




if __name__=="__main__":
	#### select data and basic setting for results####
	path = 'F:/Insula-Gcamp6/record/result_pkl/'
	beha_path = 'F:/Insula-Gcamp6/behav/gonogo-record/'
	cue_file = '#3_odor3_left(blue)_190504-Event.pkl'
	cal_file = '#3_odor3_left(blue)_190504.pkl'
	cuename = path + cue_file
	calname = path + cal_file
	behavname = beha_path + '#3_3odorrecordafter_d1_odor1_3.lvm'
	result_path = 'figures/record_results/'
	f_name,_ = cal_file.split('.')
	f_name = result_path + f_name

	##### basic processing for raw data
	cue,cal = load_tdms(cuename,calname)
	cue1_cal,cue2_cal,trial_ordor = div_by_cue(cal[0],cal[3],cue[1],cue[2],1000)
	print('!!!',sum(cue[1]),sum(cue[2]))
	print("@@@",sum(cal[3]))
	#print(cue[1])
	dif_cue1 = np.abs(np.diff(cue[1]))
	dif_cue2 = np.abs(np.diff(cue[2]))
	odor1, odor2, lick, pump, action, airpuff,laser = make_list(behavname)
	odor1_lick,odor2_lick,behav_ordor = make_gonogolick_ordor(odor1,odor2,lick,delay=200)
	odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
		odor1, odor2, action, airpuff, pump, laser, delay=200)
	raster(odor1_pump, odor2_airpuff, ' ', "Go_trials_lick", "No-Go_trials_lick")
	trial_time = 700  # now the basic time for one trial is 14 second(700*0.02)
	odor1_pump_trials = np.array([])# 0 for no-react, 1 for hit in odor1/2 trials
	odor1_nopump_trials = np.array([]) # or airpuff
	odor1_miss_trials = np.array([]) # trials no-react at all
	odor2_pump_trials = np.array([])  # 0 for no-react, 1 for hit in odor2 trials
	odor2_nopump_trials = np.array([])  # or airpuff
	odor2_miss_trials = np.array([])  # trials no-react at all
	act_start = -1
	act_end = -1
	print(np.alen(cue1_cal),np.alen(cue2_cal),np.sum(dif_cue1),np.sum(dif_cue2))
	for k in range(np.alen(cue1_cal)):
		cue1_cal[k,:] = z_score(cue1_cal[k,0:100],cue1_cal[k,:])
	for k in range(np.alen(cue2_cal)):
		cue2_cal[k,:] = z_score(cue2_cal[k,0:100],cue2_cal[k,:])

	for i in range(np.alen(odor1_pump[:,1])):
		ac = np.diff(odor1_action[i,:])
		for j in range(np.alen(ac)):
			if ac[j] == 1:
				act_start = j
			elif ac[j] == -1:
				act_end = j

		if np.sum(odor1_lick[i,:])>0 and (np.sum(odor1_pump[i,:]) + np.sum(odor1_airpuff[i,:])) > 40:
			if np.alen(odor1_pump_trials) ==0:
				odor1_pump_trials = cue1_cal[i,:]
			else:
				odor1_pump_trials = np.vstack((odor1_pump_trials,cue1_cal[i,:]))

		elif np.sum(odor1_lick[i,:]) == 0:
			if np.alen(odor1_miss_trials) == 0:
				odor1_miss_trials = cue1_cal[i, :]
			else:
				odor1_miss_trials = np.vstack((odor1_miss_trials, cue1_cal[i, :]))

		else:
			if np.alen(odor1_nopump_trials) == 0:
				odor1_nopump_trials = cue1_cal[i, :]
			else:
				odor1_nopump_trials = np.vstack((odor1_nopump_trials, cue1_cal[i, :]))
	#print(np.alen(odor2_pump[:,1]))
	for i in range(np.alen(odor2_pump[:,1])):
		ac = np.diff(odor2_action[i, :])
		for j in range(np.alen(ac)):
			if ac[j] == 1:
				act_start = j
			elif ac[j] == -1:
				act_end = j
		if np.sum(odor2_lick[i,:])>0 and (np.sum(odor2_pump[i,:]) + np.sum(odor2_airpuff[i,:])) > 40:
			# for q in range(np.alen(odor2_pump[i,:])):
			# 	if q >0 :
			# 		print(q)

			if np.alen(odor2_pump_trials) ==0:
				odor2_pump_trials = cue2_cal[i,:]
			else:
				#print(np.sum(odor2_pump[i,:]))
				odor2_pump_trials = np.vstack((odor2_pump_trials,cue2_cal[i,:]))
				#print(i)

		elif np.sum(odor2_lick[i,:]) == 0:
			if np.alen(odor2_miss_trials) == 0:
				odor2_miss_trials = cue2_cal[i, :]
			else:
				odor2_miss_trials = np.vstack((odor2_miss_trials, cue2_cal[i, :]))

		else:
			if np.alen(odor2_nopump_trials) == 0:
				odor2_nopump_trials = cue2_cal[i, :]
			else:
				odor2_nopump_trials = np.vstack((odor2_nopump_trials, cue2_cal[i, :]))

	if np.ndim(odor1_pump_trials) > 1:
		ptr1,*_ = np.shape(odor1_pump_trials)
	else:
		ptr1 = 1
	if np.ndim(odor1_nopump_trials) > 1:
		nptr1,*_ = np.shape(odor1_nopump_trials)
	else:
		nptr1 = 1
	if np.ndim(odor1_miss_trials) > 1:
		mtr1,*_ = np.shape(odor1_miss_trials)
	else:
		mtr1 = 1

	if np.ndim(odor2_pump_trials) > 1:
		ptr2,*_ = np.shape(odor2_pump_trials)
	else:
		ptr2 = 1
	if np.ndim(odor2_nopump_trials) > 1:
		nptr2,*_ = np.shape(odor2_nopump_trials)
	else:
		nptr2 = 1
	if np.ndim(odor2_miss_trials) > 1:
		mtr2,*_ = np.shape(odor2_miss_trials)
	else:
		mtr2 = 1

	## plotting
	odor1_pump_mean = np.zeros(trial_time)
	odor1_nopump_mean = np.zeros(trial_time)
	odor1_miss_mean = np.zeros(trial_time)
	odor2_pump_mean = np.zeros(trial_time)
	odor2_nopump_mean = np.zeros(trial_time)
	odor2_miss_mean = np.zeros(trial_time)

	odor1_pump_error = np.zeros(trial_time)
	odor1_nopump_error = np.zeros(trial_time)
	odor1_miss_error = np.zeros(trial_time)
	odor2_pump_error = np.zeros(trial_time)
	odor2_nopump_error = np.zeros(trial_time)
	odor2_miss_error = np.zeros(trial_time)

	cue1_mean_cal = np.zeros(trial_time)
	cue2_mean_cal = np.zeros(trial_time)

	x1 = np.linspace(-2, 12, np.alen(cue1_mean_cal))
	for k in range(trial_time):
		cue1_mean_cal[k] = np.mean(cue1_cal[:,k])
		cue2_mean_cal[k] = np.mean(cue2_cal[:, k])
	if np.alen(odor1_pump_trials) > 5:
		if np.ndim(odor1_pump_trials) is not 1:
			for k in range(trial_time):
				odor1_pump_mean[k] = np.mean(odor1_pump_trials[:,k])
				odor1_pump_error[k] = np.std(odor1_pump_trials[:,k]) / np.sqrt(ptr1)

			plt.plot(x1, odor1_pump_mean, 'r', label='odor1_hit')
			plt.fill_between(x1, odor1_pump_mean - odor1_pump_error, odor1_pump_mean + odor1_pump_error, alpha=0.3,
						 color='r')
	if np.alen(odor1_nopump_trials) > 5:
		if np.ndim(odor1_nopump_trials) is not 1:
			for k in range(trial_time):
				odor1_nopump_mean[k] = np.mean(odor1_nopump_trials[:, k])
				odor1_nopump_error[k] = np.std(odor1_nopump_trials[:, k]) / np.sqrt(nptr1)
			plt.plot(x1, odor1_nopump_mean, 'b', label='odor1_nopump')
			plt.fill_between(x1, odor1_nopump_mean - odor1_nopump_error, odor1_nopump_mean + odor1_nopump_error, alpha=0.3,
						 color='b')
	if np.alen(odor1_miss_trials) > 5:

		if np.ndim(odor1_miss_trials) is not 1:
			print(np.alen(odor1_miss_trials))
			for k in range(trial_time):
				odor1_miss_mean[k] = np.mean(odor1_miss_trials[:, k])
				odor1_miss_error[k] = np.std(odor1_miss_trials[:, k]) / np.sqrt(mtr1)
			plt.plot(x1, odor1_miss_mean, 'g', label='odor1_miss')
			plt.fill_between(x1, odor1_miss_mean - odor1_miss_error, odor1_miss_mean + odor1_miss_error, alpha=0.3, color='g')
	plt.title(f_name+"_odor1")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(f_name+"_odor1.png")
	plt.close()
	if np.alen(odor2_pump_trials) > 5:
		if np.ndim(odor2_pump_trials) is not 1:
			for k in range(trial_time):
				odor2_pump_mean[k] = np.mean(odor2_pump_trials[:, k])
				odor2_pump_error[k] = np.std(odor2_pump_trials[:, k]) / np.sqrt(ptr2)
			plt.plot(x1, odor2_pump_mean, 'r', label='odor2_hit')
			plt.fill_between(x1, odor2_pump_mean - odor2_pump_error, odor2_pump_mean + odor2_pump_error, alpha=0.3,
						 color='r')
	if np.alen(odor2_nopump_trials) > 5:
		if np.ndim(odor2_nopump_trials) is not 1:
			for k in range(trial_time):
				odor2_nopump_mean[k] = np.mean(odor2_nopump_trials[:, k])
				odor2_nopump_error[k] = np.std(odor2_nopump_trials[:, k]) / np.sqrt(nptr2)
			plt.plot(x1, odor2_nopump_mean, 'b', label='odor2_nopump')
			plt.fill_between(x1, odor2_nopump_mean - odor2_nopump_error, odor2_nopump_mean + odor2_nopump_error, alpha=0.3,
						 color='b')
	if np.alen(odor2_miss_trials) > 5:
		if np.ndim(odor2_miss_trials) is not 1:
		#	print(np.alen(odor2_miss_trials))
			for k in range(trial_time):
				odor2_miss_mean[k] = np.mean(odor2_miss_trials[:, k])
				odor2_miss_error[k] = np.std(odor2_miss_trials[:, k]) / np.sqrt(mtr2)
			plt.plot(x1, odor2_miss_mean, 'g', label='odor2_miss')
			plt.fill_between(x1, odor2_miss_mean - odor2_miss_error, odor2_miss_mean + odor2_miss_error, alpha=0.3,
						 color='g')
	plt.title(f_name+"_odor2")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(f_name+"_odor2.png")
	print('!!!')

	plt.close()
	# fig = plt.figure()
	# ax1 = fig.add_subplot(121)
	# # print('odor2miss'+str(np.alen(odor2_pump_trials)))
	# #
	# # im = ax1.imshow(np.uint8(odor1_pump_trials), aspect='auto',cmap=plt.cm.hot_r)
	# # plt.colorbar(im)
	# # plt.show()

	#raster(x1, odor1_pump_trials,'heat','x','y')




	#print(np.alen(cue1_cal[1,:]))


	#print(len(trial_ordor),len(behav_ordor))
	#for i in range(len(trial_ordor)):
	#	if trial_ordor[i] == behav_ordor[i]:
	#		print('ok')
	#	else:
	#		print(trial_ordor,behav_ordor)


