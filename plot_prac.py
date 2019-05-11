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
	path = "C:/Users/manggny/Desktop/expdata/laser"
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
		go_lick = np.zeros((go_trial+1,1500))
		for k in odor2_changed:
			if k == 1:
				trials += 1
				ng_trial += 1
		nogo_lick = np.zeros((ng_trial+1,1500))
		k = 0
		trials_times = []
		trial_time = -1
		licked = np.zeros(trials+1)
		trials = -1
		go_trial = 0
		ng_trial = 0
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
						go_die[time] += lick_changed[now_posit]
						go_lick[go_trial-1][time] += lick_changed[now_posit]
					else:
						nogo_die[time] += lick_changed[now_posit]
						nogo_lick[ng_trial - 1][time] += lick_changed[now_posit]
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

		bins_golick = np.zeros(15)
		bins_nogolick = np.zeros(15)
		bins_nogolick_range = np.zeros((ng_trial+1,15))
		bins_golick_range = np.zeros((go_trial + 1, 15))
		j = 0
		for i in range(len(diejia_trials)):
			bins_golick[int(np.floor(i/100))] += go_die[i]
			bins_nogolick[int(np.floor(i / 100))] += nogo_die[i]

		if go_trial>10:
			for j in range(go_trial+1):
				for i in range(len(go_lick[1][:])):
					bins_golick_range[j,int(np.floor(i / 100))] += go_lick[j][i]
		if ng_trial > 10:
			for j in range(ng_trial+1):
				for i in range(len(nogo_lick[1][:])):
					bins_nogolick_range[j,int(np.floor(i / 100))] += nogo_lick[j][i]

		aver_golick = np.array((bins_golick/(go_trial+1	)))
		if ng_trial > 2:
			aver_nogolick = np.array((bins_nogolick / (ng_trial + 1)))
		go_error = []
		nogo_error = []
		for i in range(15):
			go_error.append(np.std(bins_golick_range[:,i])/np.sqrt(go_trial))
			if ng_trial>2:
				nogo_error.append(np.std(bins_nogolick_range[:,i]) / np.sqrt(ng_trial))

		#print(go_error)
		#print(nogo_error)

		x = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5]
		x1 = np.array(x)
		xx = np.linspace(x1.min(),x1.max(),300)
		#print(nogo_error)
		gofunc = interp1d(x1,aver_golick,kind='cubic')
		func_goerror = interp1d(x1, go_error, kind='cubic')
		gonew = gofunc(xx)
		go_errornew = func_goerror(xx)
		if ng_trial>2:
			nogofunc = interp1d(x1, aver_nogolick, kind='cubic')
			func_ngerror = interp1d(x1, nogo_error, kind='cubic')
			nogonew = nogofunc(xx)
			nogo_errornew = func_ngerror(xx)

		for i in range(len(gonew)):
			if gonew[i] <0:
				gonew[i] = np.min(np.abs(gonew))
		if ng_trial > 2:
			for i in range(len(nogonew)):
				if nogonew[i] <0:
					nogonew[i] = np.min(np.abs(nogonew))

	#	print(xx)
	#	print(aver_nogolick)
		#print(len(gonew),np.shape(gonew))
		plt.plot(xx,gonew,'r',label='Odor1')
		plt.fill_between(xx, gonew - go_errornew, gonew + go_errornew, alpha=0.3, color = 'r')
		if ng_trial>2:
			plt.plot(xx, nogonew, 'b', label='Odor2')
			plt.fill_between(xx, nogonew - nogo_errornew, nogonew + nogo_errornew, alpha=0.3, color = 'b')



		plt.xlabel('Time(s)')
		plt.ylabel('Lickrate(s)')
		plt.title("Lickrate_Time_plot_of_" + number + "_" + jieduan + "_" + day)
		plt.legend(loc='upper left')
		#plt.show()
		plt.savefig("averplot_of_"+name+".png")
		plt.close()


		print("===================================== end =======================================")
