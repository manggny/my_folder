import sys,os
import numpy as np
from xlutils.copy import copy
import xlwt,xlrd
import matplotlib.pyplot as plt
from scipy.interpolate import *
from scipy.stats import norm
from math import exp,sqrt
Z=norm.ppf

def dPrime(hit,miss,fa,cr):
	halfhit = 0.5/(hit+miss)
	halffa = 0.5/(fa+cr)

	hitrate = hit/(hit+miss)
	if hitrate >= (1-halfhit):
		hitrate = 1-halfhit
	if hitrate == 0:
		hitrate = halfhit

	farate = fa/(fa+cr)
	if farate >= (1-halffa):
		farate = 1-halffa
	if farate == 0:
		farate = halffa

	out = {}
	out['d'] = Z(hitrate) - Z(farate)
	out['b'] = exp((Z(farate)**2 - Z(hitrate)**2)/2)
	out['c'] = -(Z(hitrate) + Z(farate))/2
	out['Ad'] = norm.cdf(out['d']/sqrt(2))
	return out


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
		try:
			laser.append(float(laserd))
		except:
			continue



	if len(laser) > 10:
		return odor1, odor2, lick, pump, action, airpuff, laser
	else:
		return odor1, odor2, lick, pump, action, airpuff



def make_list_record(filename):
	file = open(filename)
	odor1, odor2, lick, pump, action, airpuff = [], [], [], [], [], []

	for line in file:
		odor1d, odor2d, lickd, pumpd, actiond, airpuffd = line.split()
		odor1.append(float(odor1d))
		odor2.append(float(odor2d))
		lick.append(float(lickd))
		pump.append(float(pumpd))
		action.append(float(actiond))
		airpuff.append(float(airpuffd))


	return odor1,odor2,lick,pump,action,airpuff




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

	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	i = 0
	tr,ti = np.shape(go_lick)
	ntr, nti = np.shape(nogo_lick)
	ax1.imshow(np.uint8(go_lick),cmap=plt.get_cmap('gray_r'),aspect='auto')
	ax1.set_xlabel('Time(S)')
	ax1.set_ylabel('Trials')
	ax1.set_title(first_subname)

	ax1.plot([200,200],[0,tr],'k--',linewidth=1,color = 'red')
	ax1.plot([250, 250], [0, tr], 'k--', linewidth=1, color='green')
	ax1.plot([300, 300], [0, tr], 'k--', linewidth=1,color = 'red')
	ax1.plot([450, 450], [0, tr], 'k--', linewidth=1, color='green')

	fig.suptitle("Raster_of_"+title)
	xxx = [0,500,1000,1500]
	plt.xticks(xxx,np.array([0,5,10,15]),rotation=0)
	ax2 = fig.add_subplot(122)
	ax2.set_title(secon_subname)
	ax2.imshow(np.uint8(nogo_lick), cmap=plt.get_cmap('gray_r'),aspect='auto',interpolation=None,vmax=1,vmin=0,norm=None)
	ax2.set_xlabel('Time(S)')
	ax2.plot([200,200],[0,ntr],'k--',linewidth=1,color = 'red')
	ax2.plot([250, 250], [0, ntr], 'k--', linewidth=1,color = 'green')
	ax2.plot([300, 300], [0, ntr], 'k--', linewidth=1, color='red')
	ax2.plot([450, 450], [0, ntr], 'k--', linewidth=1, color='green')
	plt.xticks(xxx, np.array([0, 5, 10, 15]), rotation=0)

	plt.savefig("figures/raster/Raster_of_"+title+".png")
	plt.close()
	print("===================="+"Raster_of_"+title+".png"+" was successfully created!"+" ======================")

	return

def raster_laser(go_lick,nogo_lick,title,delay = 0):

	fig = plt.figure()
	ax1 = fig.add_subplot(121)
	i = 0
	tr,ti = np.shape(go_lick)
	ntr, nti = np.shape(nogo_lick)
	ax1.imshow(np.uint8(go_lick),cmap=plt.get_cmap('gray_r'),aspect='auto')
	ax1.set_xlabel('Time(S)')
	ax1.set_ylabel('Trials')
	ax1.set_title('lick in laser_trials')

	ax1.plot([delay,delay],[0,tr],'k--',linewidth=1,color = 'red')
	ax1.plot([delay+100,delay+100], [0, tr], 'k--', linewidth=1,color = 'red')
	ax1.plot([delay+50, delay+50], [0, tr], 'k--', linewidth=1, color='green')
	ax1.plot([delay + 250, delay + 250], [0, tr], 'k--', linewidth=1, color='green')

	fig.suptitle("Raster_of_"+title)
	xxx = [0,500,1000,1500]
	plt.xticks(xxx,np.array([0,5,10,15]),rotation=0)
	ax2 = fig.add_subplot(122)
	ax2.set_title('lick in no-laser trials')
	ax2.imshow(np.uint8(nogo_lick), cmap=plt.get_cmap('gray_r'),aspect='auto',interpolation=None,vmax=1,vmin=0,norm=None)
	ax2.set_xlabel('Time(S)')
	ax2.plot([delay,delay],[0,tr],'k--',linewidth=1,color = 'red')
	ax2.plot([delay+100,delay+100], [0, tr], 'k--', linewidth=1,color = 'red')
	ax2.plot([delay+50, delay+50], [0, tr], 'k--', linewidth=1, color='green')
	ax2.plot([delay + 250, delay + 250], [0, tr], 'k--', linewidth=1, color='green')

	plt.xticks(xxx, np.array([0, 5, 10, 15]), rotation=0)

	plt.savefig("figures/raster/Raster_of_"+title+".png")
	plt.close()
	print("===================="+"Raster_of_"+title+".png"+" was successfully created!"+" ======================")

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
		for j in range(int(delay),500):
			if go_lick[i,j] == 1:
				bins_firstgolick[int(np.floor(j / 10))] += go_lick[i,j]
				go_firstlick += j
				suc1 += 1
				break

	for i in range(len(nogo_lick[:, 1])):
		if np.sum(nogo_lick[i,:]) == 0:
			emptys2 += 1
		for j in range(int(delay),500):
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
	#print(aver_gofirst,aver_nogofirst)


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
	return aver_gofirst*10,aver_nogofirst*10



def averplot(go_lick,nogo_lick,title):

	tr,ti = np.shape(go_lick)
	ntr,nti = np.shape(nogo_lick)
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

	gonew = gofunc(xx)

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

	return

def make_gonogolick(odor1,odor2,lick,delay=200): ## version up! make_gonogolick. 190623
	odor1_changed = diff(odor1)
	odor2_changed = diff(odor2)
	lick_changed = diff(lick)
	odor_ordor = []
	for i in range(len(lick_changed)):
		if lick_changed[i] < 0:
			lick_changed[i] = 0
	odor1_trial = 0
	odor2_trial = 0
	trials = 0
	time = -1
	maxtime = 1400
	trial_start =0
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 20] == 1)):
			trials += 1
			odor1_trial += 1

		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 20] == 1)):
			trials += 1
			odor2_trial += 1

	odor1_licks = np.zeros((odor1_trial, maxtime))
	odor2_licks = np.zeros((odor2_trial, maxtime))
	now1_trial = -1
	now2_trial = -1
	now_trial = 0
	i=0
	time = -500
	stop =0
	while now_trial >= 0 and now_trial < trials:

		while i < len(odor1_changed):
			if now_trial > trials:
				break
			now_posit = i

			if (odor1_changed[now_posit] == 1):
				i = now_posit
				now_trial += 1
				now1_trial += 1
				odor1_licks[now1_trial] = lick_changed[now_posit-delay:now_posit+1200]
				i += 500
				odor_ordor.append(1)
				continue
			elif (odor2_changed[now_posit] == 1):
				i = now_posit
				now_trial += 1
				now2_trial += 1
				odor2_licks[now2_trial] = lick_changed[now_posit - delay:now_posit + 1200]
				i += 500
				odor_ordor.append(2)
				continue

			if (stop == 0):
				i += 1

	return odor1_licks,odor2_licks,odor_ordor

def div_by_laser(numpied_ori,numpied_laser):
	tr,ti = np.shape(numpied_ori)
	laser_ori = np.arange(0)
	nolaser_ori = np.arange(0)
	for i in range(tr):
		if (np.sum(numpied_laser[i,0:200]) > 10):
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
	c = 0
	maxtime = 1400
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 10] == 1)):
			trials += 1
			odor1_trial += 1

		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 10] == 1)):
			trials += 1
			odor2_trial += 1
	#print(odor1_trial)
	odor1_action = np.zeros((odor1_trial, maxtime))
	odor2_action = np.zeros((odor2_trial, maxtime))
	odor1_airpuff = np.zeros((odor1_trial, maxtime))
	odor2_airpuff = np.zeros((odor2_trial, maxtime))
	odor1_pump = np.zeros((odor1_trial, maxtime))
	odor2_pump = np.zeros((odor2_trial, maxtime))
	odor1_laser = np.zeros((odor1_trial, maxtime))
	odor2_laser = np.zeros((odor2_trial, maxtime))

	now1_trial = -1
	now2_trial = -1
	now_trial = 0
	i=0
	time = -500
	stop =0

	while i + time < len(odor1_changed):
		#print(odor1_trial)
		if now_trial > trials:
			break

		if time == -500:
			now_posit = i
			if laser[now_posit] == 1:
				c += 1
				#print(c)
		else:
			now_posit = i + time

		if (odor1_changed[now_posit] == 1) and (trial_start == 0): #and (odor1[now_posit + 10] == 1)
			if now_trial > 0:
				preend = time
				preodor = odor
				if preodor == 1:
					for q in range(0, delay):
						odor1_action[now1_trial, -q] = 0
						odor1_airpuff[now1_trial, -q] = 0
						odor1_pump[now1_trial, -q] = 0
						odor1_laser[now1_trial, -q] = 0

				elif preodor == 2:
					for q in range(0, delay):
						odor2_action[now2_trial, -q] = 0
						odor2_airpuff[now2_trial, -q] = 0
						odor2_pump[now2_trial, -q] = 0
						odor2_laser[now2_trial, -q] = 0

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
		elif (odor2_changed[now_posit] == 1) and (trial_start == 0): #			elif (odor2_changed[now_posit] == 1) and (trial_start == 0):

			if now_trial > 0:
				preend = time
				preodor = odor
				if preodor == 1:
					for q in range(preend-delay, preend):
						if q < 1400:
							odor1_action[now1_trial, q] = 0
							odor1_airpuff[now1_trial, q] = 0
							odor1_pump[now1_trial, q] = 0
							odor1_laser[now1_trial, q] = 0
					#print(np.sum(odor1_laser[now1_trial,200:]))
				elif preodor == 2:
					for q in range(preend-delay, preend):
						if q < 1400:
							odor2_action[now2_trial, q] = 0
							odor2_airpuff[now2_trial, q] = 0
							odor2_pump[now2_trial, q] = 0
							odor2_laser[now2_trial, q] =  0
					#print(np.sum(odor2_laser[now2_trial, 200:]))
			trial_start =1
			licked = 0
			i = now_posit
			stop = 1
			now_trial += 1
			now2_trial += 1

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
				#print(now1_trial)
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
	tr,ti = np.shape(odor1_laser)
	print(tr,ti,'++')
	# if delay > 0:
	# 	a = []
	# 	for i in range(1,delay+1):
	# 		a.append(-i)
	# 	odor1_action = np.delete(odor1_action,a,axis=1)
	# 	odor1_airpuff = np.delete(odor1_airpuff,a,axis=1)
	# 	odor1_pump = np.delete(odor1_pump,a,axis=1)
	# 	odor1_laser = np.delete(odor1_laser,a,axis=1)
	# 	odor2_action = np.delete(odor2_action,a,axis=1)
	# 	odor2_airpuff = np.delete(odor2_airpuff,a,axis=1)
	# 	odor2_pump = np.delete(odor2_pump,a,axis=1)
	# 	odor2_laser = np.delete(odor2_laser,a,axis=1)

	tr, ti = np.shape(odor1_laser)
	print(tr, ti, '++')


	return odor1_action,odor1_airpuff,odor1_pump,odor1_laser,odor2_action,odor2_airpuff,odor2_pump,odor2_laser

def div_by_odor_record(odor1,odor2,action,air,pump,delay=0):
	odor1_changed = diff(odor1)
	odor2_changed = diff(odor2)
	trial_start = 0
	odor1_trial = 0
	odor2_trial = 0
	trials = 0
	for k in range(len(odor1_changed)):
		if ((odor1_changed[k] == 1) and (odor1[k + 20] == 1)):
			trials += 1
			odor1_trial += 1

		#			go_trial_position.append(k)
		elif ((odor2_changed[k] == 1) and (odor2[k + 20] == 1)):
			trials += 1
			odor2_trial += 1
	#print(odor1_trial)
	odor1_action = np.zeros((odor1_trial, 1900))
	odor2_action = np.zeros((odor2_trial, 1900))
	odor1_airpuff = np.zeros((odor1_trial, 1900))
	odor2_airpuff = np.zeros((odor2_trial, 1900))
	odor1_pump = np.zeros((odor1_trial, 1900))
	odor2_pump = np.zeros((odor2_trial, 1900))

	now1_trial = -1
	now2_trial = -1
	now_trial = 0
	i=0
	time = -500
	stop =0
	while now_trial >= 0 and now_trial < trials:

		while i + time < len(odor1_changed):
			#print(odor1_trial)
			if now_trial > trials:
				break
			if time == -500:
				now_posit = i
			else:
				now_posit = i + time
			if time == -500:
				now_posit = i
			else:
				now_posit = i + time

			if (odor1_changed[now_posit] == 1) and (odor1[now_posit + 20] == 1)and (trial_start == 0):
				if now_trial > 0:
					preend = time
					preodor = odor
					if preodor == 1:
						for q in range(preend - delay, preend):
							odor1_action[now1_trial, q] = 0
							odor1_airpuff[now1_trial, q] = 0
							odor1_pump[now1_trial, q] = 0


					elif preodor == 2:
						for q in range(preend - delay, preend):
							odor2_action[now2_trial, q] = 0
							odor2_airpuff[now2_trial, q] = 0
							odor2_pump[now2_trial, q] = 0

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
			elif (odor2_changed[now_posit] == 1) and (odor2[now_posit + 20] == 1)and (trial_start == 0):
				if now_trial > 0:
					preend = time
					preodor = odor
					if preodor == 1:
						for q in range(preend - delay, preend):
							odor1_action[now1_trial, q] = 0
							odor1_airpuff[now1_trial, q] = 0
							odor1_pump[now1_trial, q] = 0


					elif preodor == 2:
						for q in range(preend - delay, preend):
							odor2_action[now2_trial, q] = 0
							odor2_airpuff[now2_trial, q] = 0
							odor2_pump[now2_trial, q] = 0

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

			if (time != -500) and (time < 1500):
				if odor == 1:
					odor1_action[now1_trial,delay+time] = action[now_posit]
					odor1_airpuff[now1_trial,delay+time] = air[now_posit]
					odor1_pump[now1_trial,delay+time] = pump[now_posit]

				elif odor == 2:
					odor2_action[now2_trial,delay+time] = action[now_posit]
					odor2_airpuff[now2_trial,delay+time] = air[now_posit]
					odor2_pump[now2_trial,delay+time] = pump[now_posit]


			#
			if time > -400:
				time += 1
			if (stop == 0):
				i += 1
			if (odor1_changed[now_posit] == -1) or (odor2_changed[now_posit] == -1):
				trial_start = 0
	# if delay > 0:
	# 	for q in range(1,delay):
	# 		odor1_action = np.delete(odor1_action,-q,axis=1)
	# 		odor1_airpuff = np.delete(odor1_airpuff,-q,axis=1)
	# 		odor1_pump = np.delete(odor1_pump,-q,axis=1)
	#
	# 		odor2_action = np.delete(odor2_action,-q,axis=1)
	# 		odor2_airpuff = np.delete(odor2_airpuff,-q,axis=1)
	# 		odor2_pump = np.delete(odor2_pump,-q,axis=1)

	return odor1_action,odor1_airpuff,odor1_pump,odor2_action,odor2_airpuff,odor2_pump

