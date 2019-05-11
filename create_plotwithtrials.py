import sys,os
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import *

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")

def diff(x):
	y = []
	for i in range(len(x)):
		if i == 0:
			y.append(0)
		else:
			y.append(x[i]-x[i-1])
	return y

if __name__ == '__main__':
	path = "C:/Users/manggny/Desktop/expdata/new"
	filelist = os.listdir(path)
	filelist_current = os.listdir()
	exist = 0
	cs = 1 # cs odor is odor 1
	for raw_file in filelist:
		if raw_file == 'go_nogo_result.xls':
			continue


		print("================================================ start =======================================")
		print(raw_file)
		filename = path+"/"+raw_file
		name,_ = raw_file.split(".")
		number,jieduan,day,*_ = raw_file.split("_")
		if jieduan == 'onlygo':
			continue
		file = open(filename)
		odor1,odor2,lick,pump,action,airpuff,laser = [],[],[],[],[],[],[]

		for line in file:
			odor1d,odor2d,lickd,pumpd,actiond,airpuffd,laserd = line.split()
			odor1.append(float(odor1d))
			odor2.append(float(odor2d))
			lick.append(float(lickd))
			pump.append(float(pumpd))
			action.append(float(actiond))
			airpuff.append(float(airpuffd))
			laser.append(laserd)
		time = -1
		lickintime =0
		lickiniti=0
		hit = 0
		miss=0
		did = -1
		i=0
		ndid = -1
		go_trial = 0
		ng_trial = 0
		cr = 0
		fa = 0
		go_die = np.zeros(1500)
		nogo_die = np.zeros(1500)

		first = 0
		trial = []
		diejia_trials = np.zeros(1500)
		trials = -1
		stop =0
		odor = 0

		trial_position = []
		first_licked = np.zeros(1500)
		odor1_changed=diff(odor1)
		odor2_changed = diff(odor2)
		lick_changed = diff(lick)
		#print(len(odor2_changed),len(odor1),len(lick_changed))
		for k in odor1_changed:
			if k == 1:
				trials += 1
				go_trial += 1
		go_lick = np.zeros((go_trial+1,1900))
		for k in odor2_changed:
			if k == 1:
				trials += 1
				ng_trial += 1
		nogo_lick = np.zeros((ng_trial+1,1900))

		go_trials = np.zeros(go_trial+1)
		nogo_trials = np.zeros(ng_trial+1)
		k = 0
		trials_times = []
		trial_time = -1
		licked = np.zeros(trials+1)
		trials = -1
		lick_changed = diff(lick)
		pump_changed = diff(pump)
		for i in range(len(odor1_changed)):
			if trial_time is not -1:
				if odor1_changed[i] == 1 or odor2_changed[i] == 1:
					trials_times.append(trial_time)
					trial_time = 0

				else:
					trial_time += 1
			else:
				if odor1_changed[i] == 1 or odor2_changed[i] == 1:
					trial_time = 0

		#print(len(trials_times))
		#print(trials)
		i = 0
		go_trial = 0
		ng_trial = 0
		while i+time < len(odor1_changed):
			if time == -1:
				now_posit = i
			else:
				now_posit = i+time
			if odor1_changed[now_posit] == 1:
			#	print(now_posit)
				#print('shangsheng:'+str(i))
				if did == 0:
					miss += 1
				i = now_posit
				stop = 1
				trial_position.append(i)
				trials+=1
				go_trial += 1
				time=0
				first = 0
				did =0
				odor = 1

			elif odor2_changed[now_posit] == 1:

				if ndid == 0:
					cr += 1
				i = now_posit
				stop = 1
				trial_position.append(i)
				trials+=1
				ng_trial += 1
				time=0
				first = 0
				#did = 0
				ndid =0
				odor = 2

			elif time<800 and (time>=0):
				if lick_changed[now_posit] == 1:
				#	print(now_posit)

					#if trials>=120:
					#	break
					licked[trials] += 1
					lickintime += 1
					#if action[i+time]
					if first == 0:# and trials>60:
						first = 1
						first_licked[time] += 1
					if (action[now_posit] == 1) and (did == 0) and (time>=300):
						trial.append(trials)
						if odor == 1:
							hit+=1
							did = 1

					elif (action[now_posit] == 1) and (ndid == 0) and (time>=300):
						if odor == 2:
						#	print(ng_trial)
							fa += 1
							ndid = 1

			elif (time>=800) and (time<1500):
				if first == 0:# and trials>60:
					first = 1
					first_licked[time] += 1
				if lick_changed[now_posit] == 1:
			#		if trials == 120:
			#			break

					licked[trials] += 1
					lickiniti += 1
			#
			if (time >=0) and (time<1500):
				if lick_changed[now_posit] == 1:
					diejia_trials[time] += lick_changed[now_posit]
					if odor == 1:
						go_trials[go_trial] += lick_changed[now_posit]
					else:
						nogo_trials[ng_trial] += lick_changed[now_posit]
			if time is not -1:
				time+=1
			if(stop == 0):
				i +=1
		if did == 0:
			miss += 1
			did =1
		if ndid == 0:
			cr += 1
			ndid = 1
		fig = plt.figure()
		go_trials = go_trials/15
		nogo_trials = nogo_trials/15
		ax1 = plt.subplot(121)
		plt.ylim(0, 4)
		ax2 = plt.subplot(122,sharey=ax1)
		if go_trial > ng_trial:
			odor1_div = 8
			odor2_div = 2
		else:
			odor1_div = 2
			odor2_div = 8
		x1 = range(0,go_trial,odor1_div)
		x2 = range(0, ng_trial,odor2_div)
	#	print((go_trial)/8)
		aver_go = np.zeros(int((go_trial)/odor1_div))
		aver_nogo = np.zeros(int((ng_trial) / odor2_div))
		for i in range(go_trial):
			aver_go[int(np.floor(i/odor1_div))] += go_trials[i]
		for i in range(ng_trial):
			aver_nogo[int(np.floor(i/odor2_div))] += nogo_trials[i]


		aver_go = aver_go/odor1_div
		aver_nogo = aver_nogo / odor2_div
		xx1 = np.linspace(0,go_trial,900)
		xx2 = np.linspace(0, ng_trial, 300)
		smooth1 = spline(x1,aver_go,xx1)
		smooth2 = spline(x2, aver_nogo, xx2)
		#new_go_t = np.array((go_trials/(go_trial+1)))
		#new_nogo_t = np.array((nogo_trials / (ng_trial + 1)))
		#gofunc = interp1d(x1,go_trials,kind='cubic')
		#nogofunc = interp1d(x2, nogo_trials, kind='cubic')
		#gonew = gofunc(xx1)
		#nogonew = nogofunc(xx2)
	# 	for i in range(len(gonew)):
	# 		if gonew[i] <0:
	# 			gonew[i] = np.min(np.abs(gonew))
	# 	for i in range(len(nogonew)):
	# 		if nogonew[i] <0:
	# 			nogonew[i] = np.min(np.abs(nogonew))
	# #	print(xx)
	#	print(aver_nogolick)
		ax1.set_xlabel('Trials')
		ax1.set_ylabel('licks in a trial(per 1 second)')
		ax1.set_title('Odor1')

		ax1.plot(xx1,smooth1,'r')


		ax2.set_xlabel('Trials')
	#	ax2.set_ylabel('licks in a trial(per 1 second)')
		ax2.set_title('Odor2')
		fig.suptitle("Lickrate_Trial_plot_of_" + number + "_" + jieduan + "_" + day)
		ax2.plot(xx2, smooth2, 'b')

		#plt.legend(loc='upper left')
		#plt.show()
		#print(go_trial)
		plt.savefig("trials_plot_of_"+name+".png")
		plt.close()
		# pl.fill_between(x, y - error, y + error,
		#				alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')

		print("===================================== end =======================================")
