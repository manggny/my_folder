import sys,os,numpy
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt,xlrd
from go.funcs import diff,make_list

if __name__ == '__main__':
	path = "C:/Users/manggny/Desktop/expdata/block"
	filelist = os.listdir(path)
	filelist_current = os.listdir()
	exist = 0


	for names in filelist_current:

		if names == 'go_nogo_result.xls':
			exist = 1
			break;
	if exist == 0:
		book = xlwt.Workbook(encoding='utf-8', style_compression=0)
		sheet = book.add_sheet('result', cell_overwrite_ok=True)
		sheet.write(0, 0, 'filename')
		sheet.write(0, 1, 'num of odor1 trials')
		sheet.write(0, 2, 'num of odor2 trials')
		sheet.write(0, 3, 'num of whole trials')
		sheet.write(0, 4, 'hit')
		sheet.write(0, 5, 'miss')
		sheet.write(0, 6, 'Accuracy for go trials')
		sheet.write(0, 7, 'FA')
		sheet.write(0, 8,'Correct reject')
		sheet.write(0, 9,'Accuracy for no-go trials')
		sheet.write(0, 10,'lick in iti (800~1500)')
		sheet.write(0, 11,'lick on time(0~800)')
		sheet.write(0, 12, 'number of no-act trials')
		sheet.write(0, 13, 'cut?')
		sheet.write(0, 14, 'odor1 licks')
		sheet.write(0, 15, 'odor2 licks')
		book.save('go_nogo_result.xls')

	for raw_file in filelist:
		if raw_file == 'go_nogo_result.xls':
			continue
		oldwb = xlrd.open_workbook('go_nogo_result.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		saved_files = old_sheet.col_values(0)


		print("================================================ start =======================================")

		filename = path+"/"+raw_file
		name,_ = raw_file.split(".")
		if name in saved_files:
			print("already exist, skip "+name)
			continue
		number,jieduan,day,godor,*_ = raw_file.split("_")
		odor1,odor2,lick,pump,action,airpuff,laser = make_list(filename)
		print(raw_file)
		cut_from, cut_to = 0, 240
		time = -1
		lickintime = 0
		lickiniti = 0
		odor1_lick = 0
		odor1_nlick = 0
		did = -1
		i = 0
		ndid = -1
		odor1_trial = 0
		odor2_trial = 0
		odor2_lick = 0
		odor2_nlick = 0
		stop = 0
		first = 0
		trials = 0
		now_trial = 0
		odor = 0

		trial_position = []
		odor1_posit = []
		odor2_posit = []
		first_licked = numpy.zeros(1900)
		odor1_changed = diff(odor1)
		odor2_changed = diff(odor2)
		lick_changed = diff(lick)
	#	print(sum(numpy.abs(lick_changed)))
		pump_changed = diff(pump)
		air_changed = diff(airpuff)
		action_changed = diff(action)
		#print(sum(numpy.abs(action_changed)))

		for k in range(len(odor1_changed)):
			if ((odor1_changed[k] == 1) and (odor1[k + 50] == 1)):
				trials += 1
				odor1_trial += 1
				#			go_trial_position.append(k)
			elif  ((odor2_changed[k] == 1) and (odor2[k + 50] == 1)):
				trials += 1
				odor2_trial += 1
		odor1_licks = numpy.zeros((odor1_trial,1900))
		odor2_licks = numpy.zeros((odor2_trial , 1900))
		odor1_action = numpy.zeros((odor1_trial,1900))
		odor2_action = numpy.zeros((odor2_trial,1900))
		odor1_pump = numpy.zeros((odor1_trial, 1900))
		odor2_pump = numpy.zeros((odor2_trial, 1900))
		odor1_air = numpy.zeros((odor1_trial, 1900))
		odor2_air = numpy.zeros((odor2_trial, 1900))

		od_laser = numpy.zeros((trials, 1900))
		now1_trial = -1
		now2_trial = -1
		#for i in trial_position:

			#	print(odor1_changed[i]+odor2_changed[i])
		i = 0
		if odor1_trial > odor2_trial:
			whichsgo = 1
		else:
			whichsgo = 2

		if cut_to > trials:
			print("error! Cut_to is bigger than whole trials!")
			cut_to = trials

		if now_trial < cut_from:
			now_trial = int(cut_from)

		while now_trial >= cut_from and now_trial < cut_to:

			while i + time < len(odor1_changed):
				if now_trial >= trials:
					break
				if time == -1:
					now_posit = i
				else:
					now_posit = i + time
				if time == -1:
					now_posit = i
				else:
					now_posit = i + time

				if odor1_changed[now_posit] == 1:
					#	print(now_posit)
					# print('shangsheng:'+str(i))
					i = now_posit
					stop = 1
					#trial_position.append(i)

					now_trial += 1
					odor1_posit.append(now_trial-1)
					now1_trial += 1
					time = 0
					first = 0
					did = 0
					odor = 1

				elif odor2_changed[now_posit] == 1:

					i = now_posit
					stop = 1
					#trial_position.append(i)
					now_trial += 1
					odor2_posit.append(now_trial - 1)
					now2_trial += 1
					time = 0
					first = 0
					# did = 0
					ndid = 0
					odor = 2

				if (time >= 0) and (time < 1900):
					if odor ==1:
						odor1_action[now1_trial][time] = action[now_posit]
						odor1_pump[now1_trial][time] = pump[now_posit]
						odor1_air[now1_trial][time] = airpuff[now_posit]
						if lick_changed[now_posit] == 1:
							odor1_licks[now1_trial][time] = lick_changed[now_posit]
					else:
						odor2_action[now2_trial][time] = action[now_posit]
						odor2_pump[now2_trial][time] = pump[now_posit]
						odor2_air[now2_trial][time] = airpuff[now_posit]
						if lick_changed[now_posit] == 1:
							odor2_licks[now2_trial][time] = lick_changed[now_posit]
				#
				if time is not -1:
					time += 1
				if (stop == 0):
					i += 1
		empty_odor1 = 0
		empty_odor2 = 0

		odor1_hit = 0
		odor1_miss = 0
		odor2_hit = 0
		odor2_miss = 0
		odor1_did = -1
		odor2_did = -1
		for tri in range(len(odor1_licks[:,1])):
			#if numpy.sum(odor1_licks[tri,:]) == 0:
			#	empty_odor1 += 1
			#	continue
			#else:
			# if tri<(cut_from*(0.8)) or tri>(cut_to*(0.8)):
			# 	continue
			odor1_did = 0
			for ms in range(len(odor1_licks[1,:])):
				if (ms <= 800) and (odor1_licks[tri,ms] == 1):
					lickintime += 1
				elif (ms > 800) and (ms <=1900) and (odor1_licks[tri,ms] == 1):
					lickiniti += 1
				if (odor1_licks[tri,ms] == 1) and (odor1_action[tri,ms]==1) and (odor1_did == 0):
					if (numpy.sum(odor1_pump[tri, ms:ms+50])+numpy.sum( odor1_air[tri, ms:ms+50])) < 10:
						print(tri)
						#input("there is no pump or air in odor1!! press enter to continue..")
					odor1_hit += 1
					odor1_did = 1
			if odor1_did == 0:
				odor1_miss += 1
		for tri in range(len(odor2_licks[:,1])):
#			if numpy.sum(odor2_licks[tri,:]) == 0:
#				empty_odor2 += 1
#				continue

#			else:
			odor2_did = 0
			for ms in range(len(odor2_licks[1,:])):
				if (ms <= 800) and (odor2_licks[tri,ms] == 1):
					lickintime += 1
				elif (ms > 800) and (ms <=1900) and (odor2_licks[tri,ms] == 1):
					lickiniti += 1
				if (odor2_licks[tri,ms] == 1) and (odor2_action[tri,ms]==1) and (odor2_did == 0):
					if (numpy.sum(odor2_pump[tri, ms:ms+50])+numpy.sum( odor2_air[tri, ms:ms+50])) < 10:
						print(tri)
						#input("there is no pump or air in odor2!! press enter to continue..")
					odor2_hit += 1
					odor2_did = 1
			if odor2_did == 0:
				odor2_miss += 1
		noact_trial = empty_odor1+empty_odor2
	#	print(odor1_hit,odor1_miss,odor2_hit,odor2_miss)
	#	print(noact_trial)

		print(raw_file + ":\n" + "odor1 trials : %f\nodor2 trials : %f" % (odor1_trial, odor2_trial))
		if whichsgo == 1:
			hit = odor1_hit
			miss = odor1_miss
			fa = odor2_hit
			cr = odor2_miss
		else:
			hit = odor2_hit
			miss = odor2_miss
			fa = odor1_hit
			cr = odor1_miss
		if (hit+miss) >1:
			accuracy = hit / (hit+miss)
		else:
			accuracy = 0
		print("lick on time : %f\nlick in iti : %f\nwhole trials : %f\nhit : %f\nmiss : %f\naccuracy percentage : %f\nfa : %f\ncorrect reject : %f" % (
			lickintime, lickiniti, trials, hit, miss, accuracy, fa, cr))
		print("no action trial num : %f\n"%(noact_trial))
		print("===============================================end=============================================")

		saved = 0
		if (cr+fa) >0:
			acc_nogo = cr / (cr+fa)
		else:
			acc_nogo = 0
		if odor2_trial == 1:
			odor2_trial = 0
		elif odor1_trial == 1:
			odor1_trial = 0
		for i in saved_files:
			if i == name:
				saved = 1
				break
		if saved == 0:
			sheet.write(len(saved_files), 0, name)
			sheet.write(len(saved_files), 1, str(odor1_trial))
			sheet.write(len(saved_files), 2, str(odor2_trial))
			sheet.write(len(saved_files), 3, str(trials))
			sheet.write(len(saved_files), 4, str(hit))
			sheet.write(len(saved_files), 5, str(miss))
			sheet.write(len(saved_files), 6, str(hit / (hit+miss)))
			sheet.write(len(saved_files), 7, str(fa))
			sheet.write(len(saved_files), 8, str(cr))
			sheet.write(len(saved_files), 9, str(acc_nogo))
			sheet.write(len(saved_files), 10, str(lickiniti))
			sheet.write(len(saved_files), 11, str(lickintime))
			sheet.write(len(saved_files), 12, str(noact_trial))
			sheet.write(len(saved_files), 13, str(cut_from)+'_'+str(cut_to))
			sheet.write(len(saved_files), 14, str(numpy.sum(odor1_licks)))
			sheet.write(len(saved_files), 15, str(numpy.sum(odor2_licks)))
			os.remove('go_nogo_result.xls')
			newwb.save('go_nogo_result.xls')
