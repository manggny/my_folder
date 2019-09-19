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

def div_by_cue(cal_time,cal_data,cue1,cue2,cue_hz,delay = 2):
	cue_interval = 1/cue_hz
	i = 0
	t = 0
	delay = delay*50
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
						cue1_cal[now_cue1, 0:delay] = cal_data[k - delay:k]
						cue1_cal[now_cue1, delay:] = cal_data[k:k + (700-delay)]
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
						cue2_cal[now_cue2, 0:delay] = cal_data[k - delay:k]
						cue2_cal[now_cue2, delay:] = cal_data[k:k + (700-delay)]

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

def normalizing_z(cal):
	f0 = np.mean(cal)
	q = np.std(cal)
	result = []
	for i in range(len(cal)):
		result.append((cal[i]-f0)/q)
	return result

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

if __name__=="__main__":
	#### select data and basic setting for results####
	pkl_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/after_optimize/after_cleaning/after_delete/gonogo50/'
	result_path = pkl_path+'/after_behav/'

	filelist = os.listdir(pkl_path)
	filelist_result = os.listdir(result_path)
	exist = 0

	for filename in filelist:

		f_name, *sys = filename.split('.')
		if len(sys) == 0:
			print('!!',filename)
			print(sys)
			continue
		result_name = f_name +'_behav.pkl'
		filename = pkl_path+filename

		if result_name in filelist_result:
			print(result_name,' already exists! skip...')
			continue
		result_name = result_path + f_name + '_behav.pkl'
		result_dic = {'odor1': [], 'odor2': [], 'odor1_lick': [], 'odor2_lick': [], 'odor1_pre': [], 'odor2_pre': []}

		##### basic processing for raw data
		raw_data = unpickle(filename)
		odor1_pump_trials = np.array([])
		odor1_miss_trials = np.array([])
		odor2_pump_trials = np.array([])
		odor2_miss_trials = np.array([])
		lick = raw_data['lick']
		pump = raw_data['pump']
		odor_list = raw_data['odor_order']
		airpuff = raw_data['air']
		cal = raw_data['cal_data']

		for i in range(np.alen(cal[:,1])):
			if odor_list[i] == 1:
				if np.sum(lick[i,:])>0 and (np.sum(pump[i,:])) > 40:
					if np.alen(odor1_pump_trials) == 0:
						odor1_pump_trials = cal[i, :]
					else:
						odor1_pump_trials = np.vstack((odor1_pump_trials, cal[i, :]))

				else:
					if np.alen(odor1_miss_trials) == 0:
						odor1_miss_trials = cal[i, :]
					else:
						odor1_miss_trials = np.vstack((odor1_miss_trials, cal[i, :]))


			elif odor_list[i] == 2:
				if np.sum(lick[i, :]) > 0 and (np.sum(airpuff[i, :])) > 40:
					if np.alen(odor2_pump_trials) == 0:
						odor2_pump_trials = cal[i, :]
					else:
						odor2_pump_trials = np.vstack((odor2_pump_trials, cal[i, :]))
				else:
					if np.alen(odor2_miss_trials) == 0:
						odor2_miss_trials = cal[i,:]
					else:
						odor2_miss_trials = np.vstack((odor2_miss_trials, cal[i, :]))

		print(odor1_pump_trials.shape)
		print(odor1_miss_trials.shape)
		print(odor2_pump_trials.shape)
		print(odor2_miss_trials.shape)


		result_dic['odor1'].append(odor1_pump_trials)
		result_dic['odor1'].append(odor1_miss_trials)
		result_dic['odor2'].append(odor2_pump_trials)
		result_dic['odor2'].append(odor2_miss_trials)

		output = open(result_name, 'wb')
		pkl.dump(result_dic, output)
		output.close()




