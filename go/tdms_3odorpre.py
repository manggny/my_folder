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
from pyheatmap.heatmap import HeatMap as HM
from matplotlib import cm

def draw_heatmap(data, map_name, vmin, vmax):
	cmap = cm.get_cmap('rainbow', 1000)
	h, w = len(data), len(data[0])
	figure = plt.figure(figsize=(int(w*1.2/32), int(h*1.2/32)))
	plt.figure(facecolor='w',figsize=(10,10))
	ax = figure.add_subplot(111)
	#ax.axis("off")
	map = ax.imshow(data, cmap=cmap, aspect='equal')#, vmin=vmin, vmax=vmax)
	plt.show()



def z_score(whole,score):  #홀 은 전체 분포를 만들 데이터, 넘파이 like; score는 변환할 구체적 score들 넘파이 like
	whole_std = np.std(whole)
	whole_mean = np.mean(whole)
	if whole_std <=0.1:
		print(whole_std)
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




if __name__=="__main__":
	#### select data and basic setting for results####
	path = 'F:/Insula-Gcamp6/record/result_pkl/'
	beha_path = 'F:/ACC-Camk2/GCAMP6/record_gonogo/'
	cue_file = '#m3_odor3_right(red)_left(blue)_190502-Event.pkl'
	cal_file = '#m3_odor3_right(red)_left(blue)_190502.pkl'
	cuename = path + cue_file
	calname = path + cal_file
	#behavname = beha_path + '#5_gca_ai+accgonogorecord_0120_odor1_4.lvm'
	result_path = 'figures/record_results/'
	f_name,_ = cal_file.split('.')
	f_name = result_path + f_name

	##### basic processing for raw data
	cue,cal = load_tdms(cuename,calname)
	cue1_cal,cue2_cal,cue3_cal,trial_ordor = div_by_cue(cal[0],cal[3],cue[1],cue[2],cue[3],1000)
	print('!!!',sum(cue[1]),sum(cue[2]),sum(cue[3]))

	dif_cue1 = np.abs(np.diff(cue[1]))
	dif_cue2 = np.abs(np.diff(cue[2]))

	for k in range(np.alen(cue1_cal)):
		cue1_cal[k,:] = z_score(cue1_cal[k,0:100],cue1_cal[k,:])
	for k in range(np.alen(cue2_cal)):
		cue2_cal[k,:] = z_score(cue2_cal[k,0:100],cue2_cal[k,:])
	for k in range(np.alen(cue3_cal)):
		cue3_cal[k,:] = z_score(cue3_cal[k,0:100],cue3_cal[k,:])

	trial_time = 250
	cue1_mean_cal = np.zeros(250)
	cue1_error_cal = np.zeros(250)
	cue2_mean_cal = np.zeros(250)
	cue2_error_cal = np.zeros(250)
	cue3_mean_cal = np.zeros(250)
	cue3_error_cal = np.zeros(250)

	tr1, *_ = np.shape(cue1_cal)
	tr2, *_ = np.shape(cue2_cal)
	tr3, *_ = np.shape(cue3_cal)

	print(tr1,tr2,tr3)
	x1 = np.linspace(-2, 3, trial_time)
	for k in range(trial_time):
		cue1_mean_cal[k] = np.mean(cue1_cal[:,k])
		cue1_error_cal[k] = np.std(cue1_cal[:,k]) / np.sqrt(tr1)
		cue2_mean_cal[k] = np.mean(cue2_cal[:, k])
		cue2_error_cal[k] = np.std(cue2_cal[:, k]) / np.sqrt(tr2)
		cue3_mean_cal[k] = np.mean(cue3_cal[:, k])
		cue3_error_cal[k] = np.std(cue3_cal[:, k]) / np.sqrt(tr3)
	plt.plot(x1, cue1_mean_cal, 'r', label='odor1')
	plt.fill_between(x1, cue1_mean_cal - cue1_error_cal, cue1_mean_cal + cue1_error_cal, alpha=0.3,
						 color='r')
	plt.plot(x1, cue2_mean_cal, 'b', label='odor2')
	plt.fill_between(x1, cue2_mean_cal - cue2_error_cal, cue2_mean_cal + cue2_error_cal, alpha=0.3,
					 color='b')
	plt.plot(x1, cue3_mean_cal, 'g', label='odor3')
	plt.fill_between(x1, cue3_mean_cal - cue3_error_cal, cue3_mean_cal + cue3_error_cal, alpha=0.3,
					 color='g')

	plt.title(f_name+"_")
	plt.xlabel('Time(s)')
	plt.ylabel('z-score')
	plt.legend(loc='upper right')
	plt.savefig(f_name + "left.png")
	plt.close()
	#hm1 = HM(cue1_cal[:,0:250].tolist())
	#hm2 = HM(cue2_cal[:,0:250].tolist())
	#hm3 = HM(cue3_cal[:,0:250].tolist())
	# draw_heatmap(cue2_cal[:,0:250],0,0,0)
	#
	# for i in range(len(cue1_cal[:,0])):
	# 	if np.max(cue2_cal[i,0:250]) > 30 or np.min(cue2_cal[i,0:250])<-30:
	# 		print(i)
	# print(np.mean(cue2_cal[:,0:100]),np.mean(cue2_cal[0:100      ]))
	# hm1.heatmap(save_as=f_name+'_odor1_heatmap.png')
	# hm2.heatmap(save_as=f_name+'_odor2_heatmap.png')
	# hm3.heatmap(save_as=f_name+'_odor3_heatmap.png')

	#plt.savefig(f_name+"_odor1.png")
	#plt.close()

