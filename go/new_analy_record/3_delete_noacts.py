# load the original pkl file(not dived), and save it after optimizing.


from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from scipy import log
from go.funcs import make_list_record,raster
import os,math

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


def func(x, a, b, c):
	return a * np.exp(-b * x) + c

def func2(x, a, b):
	return a * log(x) + b

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
	all_cue_cal = np.zeros((int(cue1_trialnum+cue2_trialnum),700))
	cue1_cal = np.zeros((int(cue1_trialnum),700))
	cue2_cal = np.zeros((int(cue2_trialnum), 700))
	all_cue = 0
	now_cue1 = 0
	now_cue2 = 0
	cue_order = []
	while i < np.alen(change_cue1):
		if change_cue1[i] == 1:
			trial_start = round(i/20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k])<=t and np.sum(cal_time[0:k+1])>t:
					if len(cal_data[k:k + 600]) < 600:
						cue1_cal = np.delete(cue1_cal,now_cue1,0)
						all_cue_cal = np.delete(all_cue_cal, all_cue, 0)
						print('cue1' + str(now_cue1))
						break
					else:
						cue1_cal[now_cue1, 0:delay] = cal_data[k - delay:k]
						cue1_cal[now_cue1, delay:] = cal_data[k:k + (700-delay)]
						all_cue_cal[all_cue, :] = cue1_cal[now_cue1,:]
						cue_order.append(1)
						now_cue1 += 1
						all_cue += 1
						break

			#print('1!')

		elif change_cue2[i] == 1:
			trial_start = round(i / 20)
			for k in range(trial_start-20,trial_start+20):
				if np.sum(cal_time[0:k]) <= t and np.sum(cal_time[0:k + 1]) > t:
					if len(cal_data[k:k + 600]) < 600:
						cue2_cal = np.delete(cue2_cal,now_cue2,0)
						all_cue_cal = np.delete(all_cue_cal,all_cue,0)
						print('cue2' + str(now_cue2))
						break
					else:
						cue2_cal[now_cue2, 0:delay] = cal_data[k - delay:k]
						cue2_cal[now_cue2, delay:] = cal_data[k:k + (700-delay)]
						all_cue_cal[all_cue, :] = cue2_cal[now_cue2, :]
						cue_order.append(2)
						now_cue2 += 1
						all_cue += 1
						break

			#print('2!')

		t += cue_interval
		i += 1
	for i in range(np.alen(all_cue_cal)):
		if np.max(all_cue_cal[i,:]) == 0:
			all_cue_cal = np.delete(all_cue_cal,i,0)
			print('empty trial!', i)
			break

	print(np.shape(all_cue_cal))
	#print(cue1_cal,np.mean(cue1_cal))
	#print(cue2_cal,np.mean(cue2_cal))
	return cue1_cal,cue2_cal,all_cue_cal,cue_order

def diff(x):
	y = []
	for i in range(len(x)):
		if i == 0:
			y.append(0)
		else:
			y.append(x[i]-x[i-1])
	return y

def div_by_behav(odor1,odor2,air,pump,lick,delay=2):
	odor1_changed = np.diff(odor1)
	odor2_changed = np.diff(odor2)
	trial_start = 0
	odor1_trial = 0
	odor2_trial = 0
	trials = 0
	odor_list = []
	delay = delay*100
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 20] == 1)):
			trials += 1
			odor1_trial += 1
			odor_list.append(1)
		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 20] == 1)):
			trials += 1
			odor2_trial += 1
			odor_list.append(2)
	#print(odor1_trial)

	print(trials,'trials')
	print(max(odor_list),odor1_trial,odor2_trial)


	all_lick = np.zeros((trials, 1400))
	all_pump = np.zeros((trials, 1400))
	all_airpuff = np.zeros((trials, 1400))

	now1_trial = -1
	now2_trial = -1
	now_trial = -1
	i=0
	time = -500
	stop =0
	while now_trial+1 < trials:

		while i < len(odor1_changed):
			if now_trial > trials:
				break

			if (odor1_changed[i] == 1) and (odor1[i + 20] == 1)and (trial_start == 0):
				now_trial += 1
				now1_trial += 1
				odor = 1
				if np.alen(lick[i-delay:i+(1400-delay)]) == 1400:
					all_lick[now_trial,:] = lick[i-delay:i+(1400-delay)]
					all_pump[now_trial, :] = pump[i - delay:i + (1400 - delay)]
					all_airpuff[now_trial, :] = air[i - delay:i + (1400 - delay)]
				else:
					l = np.alen(lick[i-delay:i+(1400-delay)])
					all_lick[now_trial, 0:l] = lick[i - delay:i + (l - delay)]
					all_pump[now_trial, 0:l] = pump[i - delay:i + (l - delay)]
					all_airpuff[now_trial, 0:l] = air[i - delay:i + (l - delay)]
				if odor_list[now_trial] != odor:
					print(odor_list[now_trial],odor,' diff!!!!')
				i += 1000

				continue
			elif (odor2_changed[i] == 1) and (odor2[i + 20] == 1)and (trial_start == 0):

				now_trial += 1
				now2_trial += 1

				odor = 2
				if np.alen(lick[i-delay:i+(1400-delay)]) == 1400:
					all_lick[now_trial,:] = lick[i-delay:i+(1400-delay)]
					all_pump[now_trial, :] = pump[i - delay:i + (1400 - delay)]
					all_airpuff[now_trial, :] = air[i - delay:i + (1400 - delay)]
				else:
					l = np.alen(lick[i-delay:i+(1400-delay)])
					all_lick[now_trial, 0:l] = lick[i - delay:i + (l - delay)]
					all_pump[now_trial, 0:l] = pump[i - delay:i + (l - delay)]
					all_airpuff[now_trial, 0:l] = air[i - delay:i + (l - delay)]

				if odor_list[now_trial] != odor:
					print(odor_list[now_trial],odor,' diff!!!!')
				i += 1000
				continue
			i += 1

	return all_lick,all_pump,all_airpuff,odor_list

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

if __name__=="__main__":
	pkl_path = 'F:/Insula-Gcamp6/record/result_pkl/new_all/190925_pkls/after_obt_clean_no_nom/50/'
	result_path = pkl_path+'after_delete/'

	filelist = os.listdir(pkl_path)
	filelist_result = os.listdir(result_path)
	exist = 0

	for filename in filelist:
		### setting###
		print('###################',filename, ' start!!!########################')
		sys = 0
		name,*sys = filename.split('.')
		result_name = name + '_del.pkl'

		if result_name in filelist_result:
			print(filename,' is already exist!! skip...')
			continue

		if sys == []:
			continue

		filename = pkl_path+filename

		raw_data = unpickle(filename)

		miss_list = []

		lick = raw_data['lick']
		pump = raw_data['pump']
		odor_list = raw_data['odor_order']
		airpuff = raw_data['air']
		cal = raw_data['cal_data']

		print(cal.shape)
		tr,ti = np.shape(pump)
		win_num = math.ceil(tr/10)
		print(tr,ti,win_num)
		goacc_list = []
		for i in range(tr):
			if np.sum(pump[i,:])>30:
				goacc_list.append(1)
			else:
				goacc_list.append(0)

		good_cals = np.array([])
		good_odor = []
		good_lick = np.array([])
		good_pump = np.array([])
		good_air = np.array([])
		#
		omission_cals = np.array([])
		omission_odor = []
		omission_lick = np.array([])
		omission_pump = np.array([])
		omission_air = np.array([])

		for i in range(win_num):
			acc_gos = sum(goacc_list[i*10:(i+1)*10])
			go_nums = odor_list[i*10:(i+1)*10].count(1)
			print(go_nums)
			if acc_gos/go_nums <= 0.5:
				print('omi!',i)
				if np.alen(omission_cals) == 0:
					omission_cals = cal[i*10:(i+1)*10,:]
					omission_odor = odor_list[i*10:(i+1)*10]
					omission_lick = lick[i*10:(i+1)*10,:]
					omission_pump = pump[i*10:(i+1)*10,:]
					omission_air = airpuff[i*10:(i+1)*10,:]
				else:
					omission_cals = np.vstack((omission_cals, cal[i*10:(i+1)*10,:]))
					for k in range(len(odor_list[i*10:(i+1)*10])):
						omission_odor.append(odor_list[i*10+k])
					omission_lick = np.vstack((omission_lick, lick[i*10:(i+1)*10, :]))
					omission_pump = np.vstack((omission_pump, pump[i*10:(i+1)*10,:]))
					omission_air = np.vstack((omission_air, airpuff[i*10:(i+1)*10,:]))
			else:
				if np.alen(good_cals) == 0:
					good_cals = cal[i*10:(i+1)*10,:]
					good_odor = odor_list[i*10:(i+1)*10]
					good_lick = lick[i*10:(i+1)*10,:]
					good_pump = pump[i*10:(i+1)*10,:]
					good_air = airpuff[i*10:(i+1)*10,:]
				else:
					good_cals = np.vstack((good_cals, cal[i*10:(i+1)*10,:]))
					#print('odor',type(good_odor))
					for k in range(len(odor_list[i*10:(i+1)*10])):
						good_odor.append(odor_list[i*10+k])
					good_lick = np.vstack((good_lick, lick[i*10:(i+1)*10, :]))
					good_pump = np.vstack((good_pump, pump[i*10:(i+1)*10,:]))
					good_air = np.vstack((good_air, airpuff[i*10:(i+1)*10,:]))


		print('omissions : ',omission_air.shape,omission_pump.shape,omission_lick.shape,len(omission_odor),omission_cals.shape)
		print('goods : ', good_air.shape, good_pump.shape, good_lick.shape, len(good_odor),
			  good_cals.shape)

		result_g = {'lick':good_lick,'pump':good_pump,'air':good_air,'odor_order':good_odor,'cal_data':good_cals}
		result_b = {'lick': omission_lick, 'pump': omission_pump, 'air': omission_air, 'odor_order': omission_odor,
					'cal_data': omission_cals}


		result_name_g = result_path + name + '_deleted_good.pkl'
		result_name_b = result_path + name + '_deleted_omis.pkl'

		output = open(result_name_g, 'wb')
		pkl.dump(result_g, output)
		output.close()

		output = open(result_name_b, 'wb')
		pkl.dump(result_b, output)
		output.close()

		print(result_path+name + ' was saved!!')