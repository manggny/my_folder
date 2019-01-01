from nptdms import TdmsFile
import numpy as np
import pickle as pkl
import sys, os
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list_record
from go.funcs import div_by_laser,make_gonogolick_ordor,div_by_odor_record


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
	cue1_cal = np.zeros((int(cue1_trialnum),1000))
	cue2_cal = np.zeros((int(cue2_trialnum), 1000))
	now_cue1 = 0
	now_cue2 = 0
	cue_ordor = []
	while i < np.alen(change_cue1):
		if change_cue1[i] == 1:
			trial_start = round(i/20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k])<=t and np.sum(cal_time[0:k+1])>t:
					cue1_cal[now_cue1,0:200] = cal_data[k-200:k]
					cue1_cal[now_cue1,200:1000] = cal_data[k:k+800]
			now_cue1 += 1
			cue_ordor.append(1)
			#print('1!')

		elif change_cue2[i] == 1:
			trial_start = round(i / 20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k]) <= t and np.sum(cal_time[0:k + 1]) > t:
					cue2_cal[now_cue2, 0:200] = cal_data[k - 200:k]
					cue2_cal[now_cue2, 200:1000] = cal_data[k:k + 800]
			now_cue2 += 1
			cue_ordor.append(2)
			#print('2!')

		t += cue_interval
		i += 1
	#print(cue1_cal,np.mean(cue1_cal))
	#print(cue2_cal,np.mean(cue2_cal))
	return cue1_cal,cue2_cal,cue_ordor




if __name__=="__main__":
	path = 'F:/ACC-Camk2/GCAMP6/record_pkls/'
	beha_path = 'F:/ACC-Camk2/GCAMP6/uncertainty/'
	cuename = path + '#g3_uncertainty_record_odor1_1228-Event.pkl'
	calname = path + '#g3_uncertainty_record_odor1_1228.pkl'
	behavname = beha_path + '#g3_uncertainrecord_d1_odor1_2.lvm'
	cue,cal = load_tdms(cuename,calname)
	cue1_cal,cue2_cal,trial_ordor = div_by_cue(cal[0],cal[2],cue[1],cue[2],1000)
	odor1, odor2, lick, pump, action, airpuff = make_list_record(behavname)
	odor1_lick,odor2_lick,behav_ordor = make_gonogolick_ordor(odor1,odor2,lick)
	odor1_action, odor1_airpuff, odor1_pump, odor2_action, odor2_airpuff, odor2_pump = div_by_odor_record(odor1,odor2,action,airpuff,pump)
	#이제 시간 굳이 합칠 필요 없이, behav에서 hit 하면 hit 으로, pump하면 pump으로 하면 됨!


	#print(len(trial_ordor),len(behav_ordor))
	#for i in range(len(trial_ordor)):
	#	if trial_ordor[i] == behav_ordor[i]:
	#		print('ok')
	#	else:
	#		print(trial_ordor,behav_ordor)



	#print(np.mean(cue[0]),np.mean(cue[1]),np.mean(cue[2]),np.mean(cue[3]))
	#print(type(cal[0]),np.mean(cal[1]),np.mean(cal[2]),np.mean(cal[3]),np.mean(cal[4]),np.mean(cal[5]))
	#print(np.mean(cal[3]))