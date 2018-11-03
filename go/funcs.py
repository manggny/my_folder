import sys,os
import numpy as np
from xlutils.copy import copy
import xlwt,xlrd
import matplotlib.pyplot as plt
from scipy.interpolate import *


def diff(x):
	y = []
	for i in range(len(x)):
		if i == 0:
			y.append(0)
		else:
			y.append(x[i]-x[i-1])
	return y

def make_list(filename):
	file = open(filename)
	odor1, odor2, lick, pump, action, airpuff, laser = [], [], [], [], [], [], []

	for line in file:
		odor1d, odor2d, lickd, pumpd, actiond, airpuffd, laserd = line.split()
		odor1.append(float(odor1d))
		odor2.append(float(odor2d))
		lick.append(float(lickd))
		pump.append(float(pumpd))
		action.append(float(actiond))
		airpuff.append(float(airpuffd))
		laser.append(float(laserd))
	# odor1_clean = clean_results(odor1)
	# odor2_clean = clean_results(odor2)
	# lick_clean = clean_results(lick)
	# pump_clean = clean_results(pump)
	# action_clean = clean_results(action)
	# airpuff_clean = clean_results(airpuff)
	# laser_clean = clean_results(laser)

	return odor1,odor2,lick,pump,action,airpuff,laser#odor1_clean,odor2_clean,lick_clean,pump_clean,action_clean,airpuff_clean,laser_clean



def clean_results(r_list):
	# delete some of 1s in list, for cleaning some wrong records. r_list should be a list with int or floats

	for i in range(len(r_list)-1):
		if r_list[i] == 1:
			if sum(r_list[i:i+10]) < 2:
				r_list[i] = 0
	return r_list


def cut(min,max):
	from_tri = input("You want to cut trials from?")
	to_tri = input("to?")
	if from_tri =='':
		from_tri = min
	else:
		if int(from_tri) is None:
			print("Must input int!")
			from_tri = min
		else:
			from_tri = int(from_tri)
			if from_tri<min:
				from_tri = min
	if to_tri =='':
		to_tri = max
	else:
		if int(to_tri) is None:
			print("Must input int!")
			to_tri = max
		else:
			to_tri = int(to_tri)

	return from_tri,to_tri

def raster(go_lick,nogo_lick,title,first_subname,secon_subname):
#	print("================================================ start =======================================")
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	i = 0
	tr,ti = np.shape(go_lick)
	ntr, nti = np.shape(nogo_lick)
	ax1.imshow(np.uint8(go_lick),cmap=plt.get_cmap('gray_r'),aspect='auto')
	ax1.set_xlabel('Time(S)')
	ax1.set_ylabel('Trials')
	ax1.set_title(first_subname)
	#print(go_trial)
	ax1.plot([200,200],[0,tr],'k--',linewidth=1,color = 'red')
	ax1.plot([300, 300], [0, tr], 'k--', linewidth=1,color = 'blue')
	ax1.plot([500, 500], [0, tr], 'k--', linewidth=1, color='green')

	fig.suptitle("Raster_of_"+title)
	xxx = [0,500,1000,1500]
	plt.xticks(xxx,np.array([0,5,10,15]),rotation=0)
	ax2 = fig.add_subplot(122)
	ax2.set_title(secon_subname)
	ax2.imshow(np.uint8(nogo_lick), cmap=plt.get_cmap('gray_r'),aspect='auto',interpolation=None,vmax=1,vmin=0,norm=None)
	ax2.set_xlabel('Time(S)')
	ax2.plot([200,200],[0,ntr],'k--',linewidth=1,color = 'red')
	ax2.plot([300, 300], [0, ntr], 'k--', linewidth=1,color = 'blue')
	ax2.plot([500, 500], [0, ntr], 'k--', linewidth=1, color='green')
	plt.xticks(xxx, np.array([0, 5, 10, 15]), rotation=0)
	#plt.show()
	plt.savefig("figures/raster/Raster_of_"+title+".png")
	plt.close()
	print("===================="+"Raster_of_"+title+".png"+" was successfully created!"+" ======================")
	#print("================================================ end =======================================")
	return

def raster_laser(go_lick,nogo_lick,title,delay = 0):
#	print("================================================ start =======================================")
	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	i = 0
	tr,ti = np.shape(go_lick)
	ntr, nti = np.shape(nogo_lick)
	ax1.imshow(np.uint8(go_lick),cmap=plt.get_cmap('gray_r'),aspect='auto')
	ax1.set_xlabel('Time(S)')
	ax1.set_ylabel('Trials')
	ax1.set_title('lick in laser_trials')
	#print(go_trial)
	ax1.plot([delay,delay],[0,tr],'k--',linewidth=1,color = 'red')
	ax1.plot([delay+100,delay+100], [0, tr], 'k--', linewidth=1,color = 'blue')
	ax1.plot([delay+300, delay+300], [0, tr], 'k--', linewidth=1, color='green')

	fig.suptitle("Raster_of_"+title)
	xxx = [0,500,1000,1500]
	plt.xticks(xxx,np.array([0,5,10,15]),rotation=0)
	ax2 = fig.add_subplot(122)
	ax2.set_title('lick in no-laser trials')
	ax2.imshow(np.uint8(nogo_lick), cmap=plt.get_cmap('gray_r'),aspect='auto',interpolation=None,vmax=1,vmin=0,norm=None)
	ax2.set_xlabel('Time(S)')
	ax2.plot([delay,delay],[0,ntr],'k--',linewidth=1,color = 'red')
	ax2.plot([delay+100, delay+100], [0, ntr], 'k--', linewidth=1,color = 'blue')
	ax2.plot([delay+300, delay+300], [0, ntr], 'k--', linewidth=1, color='green')
	plt.xticks(xxx, np.array([0, 5, 10, 15]), rotation=0)
	#plt.show()
	plt.savefig("figures/raster/Raster_of_"+title+".png")
	plt.close()
	print("===================="+"Raster_of_"+title+".png"+" was successfully created!"+" ======================")
	#print("================================================ end =======================================")
	return
def first_lick_plot(go_lick,nogo_lick,title,delay = 0):
	tr, ti = np.shape(go_lick)
	ntr, nti = np.shape(nogo_lick)
	secondtime = int(np.ceil(ti/100))
	emptys1=0
	emptys2 = 0
	suc1 = 0
	suc2 = 0
	bins_firstgolick = np.zeros(int(ti/10))
	bins_firstnogolick = np.zeros(int(ti/10))
	go_firstlick = 0
	nogo_firstlick = 0
	for i in range(tr):
		if np.sum(go_lick[i,:]) == 0:
			emptys1 += 1
		for j in range(int(delay),501):
			if go_lick[i,j] == 1:
				bins_firstgolick[int(np.floor(j / 10))] += go_lick[i,j]
				go_firstlick += j
				suc1 += 1
				break

	for i in range(len(nogo_lick[:, 1])):
		if np.sum(nogo_lick[i,:]) == 0:
			emptys2 += 1
		for j in range(int(delay),501):
			if nogo_lick[i,j] == 1:
				bins_firstnogolick[int(np.floor(j / 10))] += nogo_lick[i,j]
				nogo_firstlick += j
				suc2 += 1
				break
	bins_firstgolick = bins_firstgolick[int(delay/10):int(30+(delay/10))]
	bins_firstnogolick = bins_firstnogolick[int(delay/10):int(30+(delay/10))]
	x1 = np.linspace(0, 3, int(30+delay/10)-int(delay/10))
	xx = np.linspace(x1.min(), x1.max(), 300)
	aver_golick = np.array((bins_firstgolick / tr))

	if suc1 > 0:
		aver_gofirst = go_firstlick/suc1
	else:
		aver_gofirst = 0
	if suc2 >0:
		aver_nogofirst = nogo_firstlick / suc2
	else:
		aver_nogofirst = 0
	print(aver_gofirst,aver_nogofirst)


	if ntr > 2:
		aver_nogolick = np.array((bins_firstnogolick / ntr))
	gofunc = interp1d(x1, aver_golick, kind='cubic')
	#func_goerror = interp1d(x1, go_error, kind='cubic')
	#go_errornew = func_goerror(xx)
	# func_goerror = interp1d(x1, go_error, kind='cubic')
	gonew = gofunc(xx)
	# go_errornew = func_goerror(xx)
	if ntr > 2:
		nogofunc = interp1d(x1, aver_nogolick, kind='cubic')

		nogonew = nogofunc(xx)


	# for i in range(len(gonew)):
	# 	if gonew[i] < 0:
	# 		gonew[i] = np.min(np.abs(gonew))
	# if ntr > 2:
	# 	for i in range(len(nogonew)):
	# 		if nogonew[i] < 0:
	# 			nogonew[i] = np.min(np.abs(nogonew))

	plt.plot(xx, gonew, 'r', label='odor1')
	plt.plot([1, 1], [0, max(gonew)], 'k--', linewidth=1, color='red')
	plt.plot([3, 3], [0, max(gonew)], 'k--', linewidth=1, color='green')
	if ntr > 2:
		plt.plot(xx, nogonew, 'b', label='odor2')

	plt.xlabel('Time(s)')
	plt.ylabel('Lickrate(s)')
	plt.title("firstlick_Time_plot_of_" + title + "_laser")
	plt.legend(loc='upper left')
	#plt.show()
	plt.savefig("figures/firstlick/firstlick_of_" + title + ".png")
	plt.close()
	print(
		"====================" + "firstlick_of_" + title + ".png" + " was successfully created!" + " ======================")
	# print("========================================`======== end =======================================")
	return



def averplot(go_lick,nogo_lick,title):

	tr,ti = np.shape(go_lick)
	ntr,nti = np.shape(nogo_lick)
	print("ti,ti/100")
	print(ti,ti/100)
	secondtime = int(np.ceil(ti / 100))
	bins_golick = np.zeros(secondtime*10)
	bins_nogolick = np.zeros(secondtime*10)
	bins_nogolick_range = np.zeros((ntr, secondtime*10))
	bins_golick_range = np.zeros((tr, secondtime*10))


	for i in range(len(go_lick[:,1])):
		for j in range(len(go_lick[0,:])):
			bins_golick[int(np.floor(j / 10))] += go_lick[i,j]
			bins_golick_range[i,int(np.floor(j / 10))] += go_lick[i, j]

	for i in range(len(nogo_lick[:, 1])):
		for j in range(len(nogo_lick[0, :])):
			bins_nogolick[int(np.floor(j / 10))] += nogo_lick[i,j]
			bins_nogolick_range[i, int(np.floor(j / 10))] += nogo_lick[i, j]


	aver_golick = np.array((bins_golick / tr))
	if ntr > 2:
		aver_nogolick = np.array((bins_nogolick / ntr))


	x1 = np.linspace(0,secondtime, secondtime*10)
	print(len(x1),x1.max())
	xx = np.linspace(x1.min(), x1.max(), 300)

	go_error = []
	nogo_error = []
	for i in range(int(ti/10)):
		go_error.append(np.std(bins_golick_range[:, i]) / np.sqrt(tr))
		if ntr > 2:
			nogo_error.append(np.std(bins_nogolick_range[:, i]) / np.sqrt(ntr))
	gofunc = interp1d(x1, aver_golick, kind='cubic')
	func_goerror = interp1d(x1, go_error, kind='cubic')
	go_errornew = func_goerror(xx)
#func_goerror = interp1d(x1, go_error, kind='cubic')
	gonew = gofunc(xx)
#go_errornew = func_goerror(xx)
	if ntr > 2:
		nogofunc = interp1d(x1, aver_nogolick, kind='cubic')
		func_ngerror = interp1d(x1, nogo_error, kind='cubic')
		nogonew = nogofunc(xx)
		nogo_errornew = func_ngerror(xx)


	for i in range(len(gonew)):
		if gonew[i] < 0:
			gonew[i] = np.min(np.abs(gonew))
	if ntr > 2:
		for i in range(len(nogonew)):
			if nogonew[i] < 0:
				nogonew[i] = np.min(np.abs(nogonew))


	plt.plot(xx, gonew, 'r', label='odor1')
	plt.fill_between(xx, gonew - go_errornew, gonew + go_errornew, alpha=0.3, color = 'r')
	if ntr>2:
		plt.plot(xx, nogonew, 'b', label='odor2')
		plt.fill_between(xx, nogonew - nogo_errornew, nogonew + nogo_errornew, alpha=0.3, color = 'b')
	plt.plot([1, 1], [0, max(gonew)], 'k--', linewidth=1, color='red')
	plt.plot([3, 3], [0, max(gonew)], 'k--', linewidth=1, color='green')
	plt.xlabel('Time(s)')
	plt.ylabel('Lickrate(s)')
	plt.title("Lickrate_Time_plot_of_" + title+"_laser")
	plt.legend(loc='upper left')

	plt.savefig("figures/averplots/averplot_of_" + title + ".png")
	plt.close()
	print("===================="+"averplot_of_" + title + ".png"+" was successfully created!"+" ======================")
	#print("================================================ end =======================================")
	return

def analy_behavior(odor,lick,action,pumporair): #put odor, lick ,action and pump(if the odor is godor) or airpuff(ngodor)
	odor_changed = diff(odor)
	lick_changed = diff(lick)
	time = -1
	trials = 0
	for k in odor_changed:
		if k == 1:
			trials += 1

	trial_lick = np.zeros((trials+1,1900))
	now_trial = 0
	lickintime = 0
	lickiniti = 0
	hit = 0
	miss = 0

def make_gonogolick(odor1,odor2,lick,delay=0):
	odor1_changed = diff(odor1)
	odor2_changed = diff(odor2)
	lick_changed = diff(lick)
	odor1_trial = 0
	odor2_trial = 0
	trials = 0
	time = -1
	maxtime = 0
	trial_start =0
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 50] == 1)):
			trials += 1
			odor1_trial += 1
			if time > maxtime:
				maxtime = time
			time = 0

		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 50] == 1)):
			trials += 1
			odor2_trial += 1
			if time > maxtime:
				maxtime = time
			time = 0
		if time is not -1:
			time += 1
	maxtime = int(np.ceil((maxtime/100)))

	odor1_licks = np.zeros((odor1_trial, maxtime*100))
	odor2_licks = np.zeros((odor2_trial, maxtime*100))
	now1_trial = -1
	now2_trial = -1
	now_trial = 0
	i=0
	time = -500
	stop =0
	while now_trial >= 0 and now_trial < trials:

		while i + time < len(odor1_changed):
			if now_trial >= trials:
				break
			if time == -500:
				now_posit = i
			else:
				now_posit = i + time

			if (odor1_changed[now_posit] == 1 and trial_start == 0):
				trial_start = 1
				licked = 0
				i = now_posit
				stop = 1
				now_trial += 1

				now1_trial += 1
				if now1_trial > 0:
					for q in range(delay):
						odor1_licks[now1_trial-1][-q] = 0
				time = -delay
				first = 0

				odor = 1
				continue
			elif (odor2_changed[now_posit] == 1 and trial_start ==0):
				trial_start = 1
				licked = 0
				i = now_posit
				stop = 1
				now_trial += 1
				now2_trial += 1
				if now2_trial > 0:
					for q in range(delay):
						odor2_licks[now2_trial-1][-q] = 0
				time = -delay
				first = 0
				ndid = 0
				odor = 2
				continue
			if (time < 1000) and (time > -500):
				if odor == 1:


					if lick_changed[now_posit] == 1:
						licked = 1
						odor1_licks[now1_trial][delay+time] = lick_changed[now_posit]

				else:
					if lick_changed[now_posit] == 1:

						odor2_licks[now2_trial][delay+time] = lick_changed[now_posit]

			#
			if time > -400:
				time += 1
			if (stop == 0):
				i += 1
			if (odor1_changed[now_posit] == -1) or (odor2_changed[now_posit] == -1):
				trial_start = 0


	#print(maxtime)
	return odor1_licks,odor2_licks

def div_by_laser(numpied_ori,numpied_laser):
	tr,ti = np.shape(numpied_ori)
	laser_ori = np.arange(0)
	nolaser_ori = np.arange(0)
	for i in range(tr):
		if (np.sum(numpied_laser[i,0:100]) > 10):
			if (np.shape(laser_ori)[0] == 0):
				laser_ori = numpied_ori[i, :].reshape(1, ti)
				continue
			else:
				laser_ori = np.r_[laser_ori, numpied_ori[i, :].reshape(1, ti)]
		else:
			if (np.shape(nolaser_ori)[0] == 0):
				nolaser_ori = numpied_ori[i, :].reshape(1, ti)
				continue
			else:
				nolaser_ori = np.r_[nolaser_ori, numpied_ori[i, :].reshape(1, ti)]

	return laser_ori,nolaser_ori

def div_by_odor(odor1,odor2,action,air,pump,laser,delay=0):
	odor1_changed = diff(odor1)
	odor2_changed = diff(odor2)
	trial_start = 0
	odor1_trial = 0
	odor2_trial = 0
	trials = 0
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 50] == 1)):
			trials += 1
			odor1_trial += 1

		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 50] == 1)):
			trials += 1
			odor2_trial += 1
#action,air,pump,laser
	odor1_action = np.zeros((odor1_trial, 1900))
	odor2_action = np.zeros((odor2_trial, 1900))
	odor1_airpuff = np.zeros((odor1_trial, 1900))
	odor2_airpuff = np.zeros((odor2_trial, 1900))
	odor1_pump = np.zeros((odor1_trial, 1900))
	odor2_pump = np.zeros((odor2_trial, 1900))
	odor1_laser = np.zeros((odor1_trial, 1900))
	odor2_laser = np.zeros((odor2_trial, 1900))

	now1_trial = -1
	now2_trial = -1
	now_trial = 0
	i=0
	time = -500
	stop =0
	while now_trial >= 0 and now_trial < trials:

		while i + time < len(odor1_changed):
			if now_trial >= trials:
				break
			if time == -500:
				now_posit = i
			else:
				now_posit = i + time
			if time == -500:
				now_posit = i
			else:
				now_posit = i + time

			if (odor1_changed[now_posit] == 1) and (trial_start == 0):
				trial_start = 1
				licked = 0
				i = now_posit
				stop = 1
				now_trial += 1

				now1_trial += 1
				# if now1_trial > 0:
				# 	for q in range(1,delay):
				# 		odor1_action[now1_trial-1, -q] = 0
				# 		odor1_airpuff[now1_trial-1, -q] = 0
				# 		odor1_pump[now1_trial-1, -q] = 0
				# 		odor1_laser[now1_trial-1, -q] = 0
				time = -delay
				first = 0

				odor = 1
				continue
			elif (odor2_changed[now_posit] == 1) and (trial_start == 0):
				trial_start =1
				licked = 0
				i = now_posit
				stop = 1
				now_trial += 1
				now2_trial += 1
				# if now2_trial > 0:
				# 	for q in range(1,delay):
				# 		#odor2_action = np.delete(odor2_action,-q,)[now2_trial-1, -q] = 0
				# 		odor2_airpuff[now2_trial-1, -q] = 0
				# 		odor2_pump[now2_trial-1, -q] = 0
				# 		odor2_laser[now2_trial-1, -q] = 0
				time = -delay
				first = 0
				ndid = 0
				odor = 2
				continue

			if (time != -500) and (time < 1000):
				if odor == 1:
					odor1_action[now1_trial,delay+time] = action[now_posit]
					odor1_airpuff[now1_trial,delay+time] = air[now_posit]
					odor1_pump[now1_trial,delay+time] = pump[now_posit]
					odor1_laser[now1_trial,delay+time] = laser[now_posit]
				elif odor == 2:
					odor2_action[now2_trial,delay+time] = action[now_posit]
					odor2_airpuff[now2_trial,delay+time] = air[now_posit]
					odor2_pump[now2_trial,delay+time] = pump[now_posit]
					odor2_laser[now2_trial,delay+time] = laser[now_posit]

			#
			if time > -400:
				time += 1
			if (stop == 0):
				i += 1
			if (odor1_changed[now_posit] == -1) or (odor2_changed[now_posit] == -1):
				trial_start = 0
	if delay > 0:
		for q in range(1,delay):
			odor1_action = np.delete(odor1_action,-q,axis=1)
			odor1_airpuff = np.delete(odor1_airpuff,-q,axis=1)
			odor1_pump = np.delete(odor1_pump,-q,axis=1)
			odor1_laser = np.delete(odor1_laser,-q,axis=1)
			odor2_action = np.delete(odor2_action,-q,axis=1)
			odor2_airpuff = np.delete(odor2_airpuff,-q,axis=1)
			odor2_pump = np.delete(odor2_pump,-q,axis=1)
			odor2_laser = np.delete(odor2_laser,-q,axis=1)


	return odor1_action,odor1_airpuff,odor1_pump,odor1_laser,odor2_action,odor2_airpuff,odor2_pump,odor2_laser

