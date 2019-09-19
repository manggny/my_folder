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
		#print(whole_std)
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

			now_cue2 += 1
			cue_ordor.append(2)
			#print('2!')

		t += cue_interval
		i += 1
	#print(cue1_cal,np.mean(cue1_cal))
	#print(cue2_cal,np.mean(cue2_cal))
	return cue1_cal,cue2_cal,cue_ordor

def pre_odor(cue1_idx,cue2_idx):
	cue1_preodor = np.zeros(len(cue1_idx))
	cue2_preodor = np.zeros(len(cue2_idx))

	for i in range(len(cue1_idx)):
		if i == 0:
			cue1_preodor[i] = cue1_idx[i]
		else:
			cue1_preodor[i] = cue1_idx[i] - cue1_idx[i-1] -1

	for i in range(len(cue2_idx)):
		if i == 0:
			cue2_preodor[i] = cue2_idx[i]
		else:
			cue2_preodor[i] = cue2_idx[i] - cue2_idx[i-1] -1

	return cue1_preodor,cue2_preodor

if __name__=="__main__":
	#### select data and basic setting for results####
	path = 'F:/Insula-Gcamp6/record/result_pkl/'
	beha_path = 'F:/Insula-Gcamp6/behav/before 04/gonogo-record/'
	cue_file = '#3_gonogoodor3_left(blue)_190504-Event.pkl'
	cal_file = '#3_gonogoodor3_left(blue)_190504.pkl'
	cuename = path + cue_file
	calname = path + cal_file
	behavname = beha_path + '#3_3odorrecordafter_d1_odor1_3.lvm'
	cal_channal = 3
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_50%/'
	f_name,_ = cal_file.split('.')
	f_name = result_path + f_name

	result_dic = {'odor1':[],'odor2':[],'odor1_lick':[],'odor2_lick':[],'odor1_pre':[],'odor2_pre':[]}

	##### basic processing for raw data
	cue,cal = load_tdms(cuename,calname)
	cue1_cal,cue2_cal,trial_ordor = div_by_cue(cal[0],cal[cal_channal],cue[1],cue[2],1000)
	print(trial_ordor)
	idx_cue1 = []
	idx_cue2 = []
	for idx in range(len(trial_ordor)):
		if trial_ordor[idx] == 1:
			idx_cue1.append(idx)
		else:
			idx_cue2.append(idx)
	print('idx_lists',len(idx_cue1),len(idx_cue2))
	print('cue_lists', len(cue1_cal[:,1]), len(cue2_cal[:,1]))
	cue1_preodor,cue2_preodor = pre_odor(idx_cue1,idx_cue2)
	#print(cue[1])
	dif_cue1 = np.abs(np.diff(cue[1]))
	dif_cue2 = np.abs(np.diff(cue[2]))
	odor1, odor2, lick, pump, action, airpuff,laser = make_list(behavname)
	odor1_lick,odor2_lick,behav_ordor = make_gonogolick_ordor(odor1,odor2,lick,delay=200)
	odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
		odor1, odor2, action, airpuff, pump, laser, delay=200)
	#raster(odor1_pump, odor2_airpuff, ' ', "Go_trials_lick", "No-Go_trials_lick")
	#trial_time = 200  # now the basic time for one trial is 14 second(700*0.02)
	odor1_pump_trials = np.array([])# 0 for no-react, 1 for hit in odor1/2 trials
	odor1_pump_licks = np.array([])
	odor1_pump_pre = []
	odor1_nopump_trials = np.array([]) # or airpuff
	odor1_nopump_licks = np.array([])
	odor1_nopump_pre = []
	odor1_miss_trials = np.array([]) # trials no-react at all
	odor1_miss_licks = np.array([])
	odor1_miss_pre = []
	odor2_pump_trials = np.array([])  # 0 for no-react, 1 for hit in odor2 trials
	odor2_pump_licks = np.array([])
	odor2_pump_pre =[]
	odor2_nopump_trials = np.array([])  # or airpuff
	odor2_nopump_licks = np.array([])
	odor2_nopump_pre =[]
	odor2_miss_trials = np.array([])  # trials no-react at all
	odor2_miss_licks = np.array([])
	odor2_miss_pre =[]
	act_start = -1
	act_end = -1
	print(np.alen(cue1_cal),np.alen(cue2_cal),np.sum(dif_cue1),np.sum(dif_cue2))
	for k in range(np.alen(cue1_cal)):
		cue1_cal[k,:] = z_score(cue1_cal[k,0:100],cue1_cal[k,:])
	for k in range(np.alen(cue2_cal)):
		cue2_cal[k,:] = z_score(cue2_cal[k,0:100],cue2_cal[k,:])

	for i in range(np.alen(cue1_cal[:,1])):
		# ac = np.diff(odor1_action[i,:])
		# for j in range(np.alen(ac)):
		# 	if ac[j] == 1:
		# 		act_start = j
		# 	elif ac[j] == -1:
		# 		act_end = j

		if np.sum(odor1_lick[i,:])>0 and (np.sum(odor1_pump[i,:]) + np.sum(odor1_airpuff[i,:])) > 40:
			if np.alen(odor1_pump_trials) ==0:
				odor1_pump_trials = cue1_cal[i,:]
				odor1_pump_licks = odor1_lick[i,:]
				odor1_pump_pre.append(cue1_preodor[i])
			else:
				odor1_pump_trials = np.vstack((odor1_pump_trials,cue1_cal[i,:]))
				odor1_pump_licks = np.vstack((odor1_pump_licks, odor1_lick[i, :]))
				odor1_pump_pre.append(cue1_preodor[i])

		elif np.sum(odor1_lick[i,:]) == 0:
			if np.alen(odor1_miss_trials) == 0:
				odor1_miss_trials = cue1_cal[i, :]
				odor1_miss_licks = odor1_lick[i,:]
				odor1_miss_pre.append(cue1_preodor[i])
			else:
				odor1_miss_trials = np.vstack((odor1_miss_trials, cue1_cal[i, :]))
				odor1_miss_licks = np.vstack((odor1_miss_licks, odor1_lick[i, :]))
				odor1_miss_pre.append(cue1_preodor[i])

		else:
			if np.alen(odor1_nopump_trials) == 0:
				odor1_nopump_trials = cue1_cal[i, :]
				odor1_nopump_licks = odor1_lick[i,:]
				odor1_nopump_pre.append(cue1_preodor[i])
			else:
				odor1_nopump_trials = np.vstack((odor1_nopump_trials, cue1_cal[i, :]))
				odor1_nopump_licks = np.vstack((odor1_nopump_licks, odor1_lick[i, :]))
				odor1_nopump_pre.append(cue1_preodor[i])
	#print(np.alen(odor2_pump[:,1]))
	for i in range(np.alen(cue2_cal[:,1])):
		# ac = np.diff(odor2_action[i, :])
		# for j in range(np.alen(ac)):
		# 	if ac[j] == 1:
		# 		act_start = j
		# 	elif ac[j] == -1:
		# 		act_end = j
		if np.sum(odor2_lick[i,:])>0 and (np.sum(odor2_pump[i,:]) + np.sum(odor2_airpuff[i,:])) > 40:
			# for q in range(np.alen(odor2_pump[i,:])):
			# 	if q >0 :
			# 		print(q)

			if np.alen(odor2_pump_trials) ==0:
				odor2_pump_trials = cue2_cal[i,:]
				odor2_pump_licks = odor2_lick[i,:]
				odor2_pump_pre.append(cue2_preodor[i])
			else:
				#print(np.sum(odor2_pump[i,:]))
				odor2_pump_trials = np.vstack((odor2_pump_trials,cue2_cal[i,:]))
				odor2_pump_licks = np.vstack((odor2_pump_licks, odor2_lick[i, :]))
				odor2_pump_pre.append(cue2_preodor[i])
				#print(i)

		elif np.sum(odor2_lick[i,:]) == 0:
			if np.alen(odor2_miss_trials) == 0:
				odor2_miss_trials = cue2_cal[i, :]
				odor2_miss_licks = odor2_lick[i,:]
				odor2_miss_pre.append(cue2_preodor[i])
			else:
				odor2_miss_trials = np.vstack((odor2_miss_trials, cue2_cal[i, :]))
				odor2_miss_licks = np.vstack((odor2_miss_licks, odor2_lick[i, :]))
				odor2_miss_pre.append(cue2_preodor[i])

		else:
			if np.alen(odor2_nopump_trials) == 0:
				odor2_nopump_trials = cue2_cal[i, :]
				odor2_nopump_licks = odor2_lick[i,:]
				odor2_nopump_pre.append(cue2_preodor[i])
			else:
				odor2_nopump_trials = np.vstack((odor2_nopump_trials, cue2_cal[i, :]))
				odor2_nopump_licks = np.vstack((odor2_nopump_licks, odor2_lick[i, :]))
				odor2_nopump_pre.append(cue2_preodor[i])

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

	filename,_ = cal_file.split('.')
	if cal_channal ==2:
		filename = filename+'_r.pkl'
	elif cal_channal == 3:
		filename = filename + '_l.pkl'
	output = open(result_path+filename, 'wb')
	pkl.dump(result_dic, output)
	output.close()




