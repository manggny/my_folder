import sys,os
import numpy as np
from go.funcs import raster

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
	filelist_current = os.listdir()
	for raw_file in filelist:
		if raw_file == 'go_nogo_result.xls':
			continue


		print("================================================ start =======================================")
		print(raw_file)
		filename = path+"/"+raw_file
		name,_ = raw_file.split(".")
		if "Raster_of_" + name + ".png" in filelist_current:
			print("Raster_of_" + name + ".png is already exist!!")
			continue
		number,jieduan,day,godor,*_ = raw_file.split("_")
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
		first = 0
		trial = []
		diejia_trials = np.zeros(1900)
		trials = -1
		stop =0
		odor = 0

		trial_position = []
		first_licked = np.zeros(1500)
		odor1_changed=diff(odor1)
		odor2_changed = diff(odor2)
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
		#print(trials)
		#print(trials)
		licked = np.zeros(trials+1)
		trials = -1
		go_trial = 0
		ng_trial = 0
		lick_changed = diff(lick)
		pump_changed = diff(pump)
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
			if (time >=0) and (time<1900):
				if lick_changed[now_posit] == 1:

					diejia_trials[time] += lick[now_posit]
					if odor == 1:
						go_lick[go_trial][time] = lick_changed[now_posit]
					else:
						#print(time)
						#print(time)
						nogo_lick[ng_trial][time] = lick_changed[now_posit]
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
		x = range(trials+1)
		x_time = range(1500)
		i = 0
		tr, ti = np.shape(go_lick)
		ntr, nti = np.shape(nogo_lick)

		#print(np.max(go_lick))
		for j in range(tr):
			while i < ti:
				try:
					if go_lick[j][i] == 1:
						go_lick[j][i + 1] = 1
						go_lick[j][i + 2] = 1
						go_lick[j][i + 3] = 1
						go_lick[j][i + 4] = 1
						go_lick[j][i + 5] = 1
						go_lick[j][i + 6] = 1
						go_lick[j][i + 7] = 1
						i += 8
						#print(go_lick[j][i + 7])
					else:
						i += 1
				except:
					i += 1
					#print(go_lick[j][i + 7])
			i = 0
		i=0
		for j in range(ntr):
			while i < nti:
				try:
					if nogo_lick[j][i] == 1:
						nogo_lick[j][i + 1] = 1
						nogo_lick[j][i + 2] = 1
						nogo_lick[j][i + 3] = 1
						nogo_lick[j][i + 4] = 1
						nogo_lick[j][i + 5] = 1
						nogo_lick[j][i + 6] = 1
						nogo_lick[j][i + 7] = 1
						i += 8
					else:
						i += 1
				except:
					i += 1
			i=0
		if godor == "odor2":
			raster(nogo_lick,go_lick,name)
		else:
			raster(go_lick, nogo_lick, name)
		#
		# fig = plt.figure()
		# ax1 = fig.add_subplot(121)
		#
		# i = 0
		# tr,ti = np.shape(go_lick)
		# ntr, nti = np.shape(nogo_lick)
		# for j in range(tr):
		# 	while i < ti:
		# 		try:
		# 			if go_lick[j][i] == 1:
		# 				go_lick[j][i+1] = 1
		# 				go_lick[j][i + 2] = 1
		# 				go_lick[j][i + 3] = 1
		# 				go_lick[j][i + 4] = 1
		# 				go_lick[j][i + 5] = 1
		# 				go_lick[j][i + 6] = 1
		# 				go_lick[j][i + 7] = 1
		# 				i += 8
		# 			else:
		# 				i += 1
		# 		except:
		# 			i += 1
		#
		# 	i = 0
		# for j in range(ntr):
		# 	while i <nti:
		# 		try:
		# 			if nogo_lick[j][i] == 1:
		# 				nogo_lick[j][i+1] = 1
		# 				nogo_lick[j][i + 2] = 1
		# 				nogo_lick[j][i + 3] = 1
		# 				nogo_lick[j][i + 4] = 1
		# 				nogo_lick[j][i + 5] = 1
		# 				nogo_lick[j][i + 6] = 1
		# 				nogo_lick[j][i + 7] = 1
		# 				i += 8
		# 			else:
		# 				i += 1
		# 		except:
		# 			i += 1
		#
		# ax1.imshow(np.uint8(go_lick),cmap=plt.get_cmap('gray_r'),aspect='auto')
		# ax1.set_xlabel('Time(S)')
		# ax1.set_ylabel('Trials')
		# if godor == 'odor2':
		# 	ax1.set_title('lick in No-go trials')
		# else:
		# 	ax1.set_title('lick in Go-trials')
		# #print(go_trial)
		# ax1.plot([100,100],[0,go_trial],'k--',linewidth=1,color = 'red')
		# ax1.plot([300, 300], [0, go_trial], 'k--', linewidth=1,color = 'green')
		# ax1.plot([800, 800], [0, go_trial], 'k--', linewidth=1, color='green')
		# #ax1.annotate('odor-end',xy=(100,go_trial),xytext=(50,go_trial+5),fontsize = 8,xycoords = 'data')
		# fig.suptitle("Raster_of_"+number+"_"+jieduan+"_"+day)
		# xxx = [0,500,1000,1500]
		# plt.xticks(xxx,np.array([0,5,10,15]),rotation=0)
		# #plt.show()
		# #print(np.sum(nogo_lick))
		# #fig2 = plt.figure()
		# ax2 = fig.add_subplot(122)
		# if godor == 'odor2':
		# 	ax2.set_title('lick in Go trials')
		# else:
		# 	ax2.set_title('lick in No-Go trials')
		# #print(np.sum(nogo_lick))
		# #ax2.show(np.uint8(nogo_lick))
		# ax2.imshow(np.uint8(nogo_lick), cmap=plt.get_cmap('gray_r'),aspect='auto',interpolation=None,vmax=1,vmin=0,norm=None)
		# ax2.set_xlabel('Time(S)')
		#
		# ax2.plot([100,100],[0,ng_trial],'k--',linewidth=1,color = 'red')
		# ax2.plot([300, 300], [0, ng_trial], 'k--', linewidth=1,color = 'green')
		# ax2.plot([800, 800], [0, ng_trial], 'k--', linewidth=1, color='green')
		# plt.xticks(xxx, np.array([0, 5, 10, 15]), rotation=0)
		# #plt.show()
		# plt.savefig("Raster_of_"+number+"_"+jieduan+"_"+day+".png")
		# plt.close()
	#	print("===================="+"Raster_of_"+number+"_"+jieduan+"_"+day+".png"+" was successfully created!"+" ======================")

	print("================================================ end =======================================")


