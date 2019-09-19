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
	print(sum(cue2))

	change_cue1 = np.diff(cue1)

	cue1_trialnum = np.sum(np.abs(change_cue1)/2)
	#print(int(cue1_trialnum))
	change_cue2 = np.diff(cue2)
	print(sum(change_cue2))
	cue2_trialnum = np.sum(np.abs(change_cue2) / 2)

	print("tn",cue1_trialnum,cue2_trialnum)
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
	#beha_path = 'F:/ACC-Camk2/GCAMP6/record_gonogo/'
	cue_file = '#f3_gonogo50record__r(red)_left(blue,weak)_190704-Event.pkl'
	cal_file = '#f3_gonogo50record__r(red)_left(blue,weak)_190704.pkl'
	cuename = path + cue_file
	calname = path + cal_file
	#behavname = beha_path + '#5_gca_ai+accgonogorecord_0120_odor1_4.lvm'
	result_path = 'figures/record_results/'
	f_name,_ = cal_file.split('.')
	f_name = result_path + f_name

	##### basic processing for raw data
	cue,cal = load_tdms(cuename,calname)
	cue1_cal,cue2_cal,trial_ordor = div_by_cue(cal[0],cal[3],cue[1],cue[2],1000)
	print('!!!',sum(cue[1]),sum(cue[2]))
	#print('!!!', sum(cal[1]), sum(cue[2]), sum(cue[3]))

	dif_cue1 = np.abs(np.diff(cue[1]))
	dif_cue2 = np.abs(np.diff(cue[2]))

	for k in range(np.alen(cue1_cal)):
		cue1_cal[k,:] = z_score(cue1_cal[k,0:100],cue1_cal[k,:])
	for k in range(np.alen(cue2_cal)):
		cue2_cal[k,:] = z_score(cue2_cal[k,0:100],cue2_cal[k,:])


	trial_time = 600
	cue1_mean_cal = np.zeros(trial_time)
	cue1_error_cal = np.zeros(trial_time)
	cue2_mean_cal = np.zeros(trial_time)
	cue2_error_cal = np.zeros(trial_time)

	tr1, *_ = np.shape(cue1_cal)
	tr2, *_ = np.shape(cue2_cal)

	x1 = np.linspace(-2, 3, trial_time)
	for k in range(trial_time):
		cue1_mean_cal[k] = np.mean(cue1_cal[:,k])
		cue1_error_cal[k] = np.std(cue1_cal[:,k]) / np.sqrt(tr1)
		cue2_mean_cal[k] = np.mean(cue2_cal[:, k])
		cue2_error_cal[k] = np.std(cue2_cal[:, k]) / np.sqrt(tr2)

	plt.plot(x1, cue1_mean_cal, 'r', label='odor1')
	plt.fill_between(x1, cue1_mean_cal - cue1_error_cal, cue1_mean_cal + cue1_error_cal, alpha=0.3,
						 color='r')
	plt.plot(x1, cue2_mean_cal, 'b', label='odor2')
	plt.fill_between(x1, cue2_mean_cal - cue2_error_cal, cue2_mean_cal + cue2_error_cal, alpha=0.3,
					 color='b')

	plt.title(f_name+"_")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(f_name + "left.png")
	plt.close()
	#plt.savefig(f_name+"_odor1.png")
	#plt.close()

