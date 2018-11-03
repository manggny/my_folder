import sys, os
import numpy as np

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list,averplot
from go.funcs import make_gonogolick, div_by_odor,raster

if __name__ == '__main__':
	path = "F:/ACC-Camk2/Gono-go/behavior_trainning/Camk2_GTACR1/training"
	filelist = os.listdir(path)
	filelist_current = os.listdir()
	exist = 0

	for names in filelist_current:
		if names == 'go_nogo_result.xls':
			exist = 1
			break
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
		sheet.write(0, 10,'lick in iti (800~)')
		sheet.write(0, 11,'lick on time(0~800)')
		sheet.write(0, 12, 'number of no-act trials')
		book.save('go_nogo_result.xls')



	for raw_file in filelist:
		if raw_file == 'go_nogo_result.xls':
			continue
		oldwb = xlrd.open_workbook('go_nogo_result.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		saved_files = old_sheet.col_values(0)
		odor_time = 100
		delay = 200
		action_time = 500
		relative_time = odor_time+delay+action_time

		print("================================================ start =======================================")

		filename = path + "/" + raw_file
		name, _ = raw_file.split(".")
		print(name)

		if name in saved_files:
			print("already exist, skip " + name)
			continue
		try:
			number, jieduan, day, godor, *_ = raw_file.split("_")
		except:
			continue
		odor1, odor2, lick, pump, action, airpuff, laser = make_list(filename)
		odor1_lick, odor2_lick = make_gonogolick(odor1, odor2, lick,delay = 200)
		odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
			odor1, odor2, action, airpuff, pump, laser,delay = 200)
		if godor == 'odor2':
			whichsgo = 2
		else:
			whichsgo = 1

		odor1_hit = 0
		odor1_miss = 0
		odor2_hit = 0
		odor2_miss = 0
		odor1_did = -1
		odor2_did = -1
		lickintime = 0
		lickiniti = 0
		empty_odor1 = 0
		empty_odor2 = 0
		for tri in range(len(odor1_lick[:, 1])):
			# if numpy.sum(odor1_licks[tri,:]) == 0:
			#	empty_odor1 += 1
			#	continue
			# else:
			# if tri<(cut_from*(0.8)) or tri>(cut_to*(0.8)):
			# 	continue
			odor1_did = 0
			if np.sum(odor1_lick[tri,:]) == 0:
				empty_odor1 += 1
				#continue
			for ms in range(len(odor1_lick[1, :])):
				if (ms <= 800) and (odor1_lick[tri, ms] == 1):
					lickintime += 1
				elif (ms > 800) and (ms <= 1900) and (odor1_lick[tri, ms] == 1):
					lickiniti += 1
				if (odor1_lick[tri, ms] == 1) and (odor1_action[tri, ms] == 1) and (odor1_did == 0):
					if (np.sum(odor1_pump[tri, ms:ms + 50]) + np.sum(odor1_airpuff[tri, ms:ms + 50])) < 10:
						print(tri)

					odor1_hit += 1
					odor1_did = 1
			if odor1_did == 0:
				odor1_miss += 1
		for tri in range(len(odor2_lick[:, 1])):
			odor2_did = 0
			if np.sum(odor2_lick[tri,:]) == 0:
				empty_odor2 += 1
				#continue
			for ms in range(len(odor2_lick[1, :])):
				if (ms <= relative_time) and (odor2_lick[tri, ms] == 1):
					lickintime += 1
				elif (ms > relative_time) and (ms <= 1900) and (odor2_lick[tri, ms] == 1):
					lickiniti += 1
				if (odor2_lick[tri, ms] == 1) and (odor2_action[tri, ms] == 1) and (odor2_did == 0):
					if (np.sum(odor2_pump[tri, ms:ms + 50]) + np.sum(odor2_airpuff[tri, ms:ms + 50])) < 10:
						print(tri)
					odor2_hit += 1
					odor2_did = 1
			if odor2_did == 0:
				odor2_miss += 1
		noact_trial = empty_odor1 + empty_odor2

		odor1_trial,_ = np.shape(odor1_lick)
		odor2_trial, _ = np.shape(odor2_lick)
		trials = odor1_trial+odor2_trial
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
		if (hit + miss) > 1:
			accuracy = hit / (hit + miss)
		else:
			accuracy = 0
		print(
			"lick on time : %f\nlick in iti : %f\nwhole trials : %f\nhit : %f\nmiss : %f\naccuracy percentage : %f\nfa : %f\ncorrect reject : %f" % (
				lickintime, lickiniti, trials, hit, miss, accuracy, fa, cr))
		print("no action trial num : %f\n" % (noact_trial))
		print("===============================================end=============================================")

		saved = 0
		if (cr + fa) > 0:
			acc_nogo = cr / (cr + fa)
		else:
			acc_nogo = 0
		if odor2_trial == 1:
			odor2_trial = 0
		elif odor1_trial == 1:
			odor1_trial = 0

#		plot_laser(odor1_laser_first_licked, odor1_nolaser_first_licked, odor1_ras)
#		plot_laser(odor2_laser_first_licked, odor2_nolaser_first_licked, odor2_ras)


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
			sheet.write(len(saved_files), 6, str(accuracy))
			sheet.write(len(saved_files), 7, str(fa))
			sheet.write(len(saved_files), 8, str(cr))
			sheet.write(len(saved_files), 9, str(acc_nogo))
			sheet.write(len(saved_files), 10, str(lickiniti))
			sheet.write(len(saved_files), 11, str(lickintime))
			sheet.write(len(saved_files), 12, str(noact_trial))
			os.remove('go_nogo_result.xls')
			newwb.save('go_nogo_result.xls')
