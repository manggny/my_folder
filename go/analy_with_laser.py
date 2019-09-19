import sys, os
import numpy as np

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import diff, make_list,dPrime
from go.funcs import raster_laser, div_by_laser,first_lick_plot,make_gonogolick,div_by_odor,averplot

if __name__ == '__main__':
	path = "F:/Insula-Gcamp6/behav/after 04/gonogo_laser"#D:\expdata\laser"#F:/gonogodata/nodelay/laser"#F:/gonogodata/nodelay/laser"
	filelist = os.listdir(path)
	filelist_current = os.listdir()
	exist = 0

	for names in filelist_current:

		if names == 'go_nogo_result_laser_08.xls':
			exist = 1
			break;
		if names == "lateral":
			continue
	if exist == 0:
		book = xlwt.Workbook(encoding='utf-8', style_compression=0)
		sheet = book.add_sheet('result', cell_overwrite_ok=True)
		sheet.write(0, 0, 'filename')
		sheet.write(0, 1, 'num of odor1 trials')
		sheet.write(0, 2, 'num of odor2 trials')
		sheet.write(0, 3, 'num of whole trials')
		sheet.write(0, 4, 'num of odor1_laser')
		sheet.write(0, 5, 'num of odor2_laser')
		sheet.write(0, 6, 'Laser hit')
		sheet.write(0, 7, 'Laser miss')
		sheet.write(0, 8, 'Laser FA')
		sheet.write(0, 9, 'Laser CR')
		sheet.write(0, 10, 'Laser d')
		sheet.write(0, 11, 'Laser beta')
		sheet.write(0, 12, 'odor1 laser_lick')
		sheet.write(0, 13, 'odor2 laser lick')
		sheet.write(0, 14, 'odor1 laser_firstlick(ms)')
		sheet.write(0, 15, 'odor2 laser_firstlick(ms)')
		sheet.write(0, 16, 'no-Laser hit')
		sheet.write(0, 17, 'no-Laser miss')
		sheet.write(0, 18, 'no-Laser FA')
		sheet.write(0, 19, 'no-Laser CR')
		sheet.write(0, 20, 'no-Laser d')
		sheet.write(0, 21, 'no-Laser b')
		sheet.write(0, 22, 'odor1 no-laser_lick')
		sheet.write(0, 23, 'odor2 no-laser_lick')
		sheet.write(0, 24, 'odor1 no-laser_firstlick(ms)')
		sheet.write(0, 25, 'odor2 no-laser_firstlick(ms)')
		book.save('go_nogo_result_laser_08.xls')

	for raw_file in filelist:
		if raw_file == 'go_nogo_result_laser_08.xls':
			continue
		oldwb = xlrd.open_workbook('go_nogo_result_laser_08.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		saved_files = old_sheet.col_values(0)

	#	print("================================================ start =======================================")

		odor_time = 100
		delay = 200
		action_time = 200
		relative_time = odor_time + delay + action_time

		print("================================================ start =======================================")

		filename = path + "/" + raw_file
		name, *_ = raw_file.split(".")
		print(name)
	#	print(name)

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
		odor1_laser_lick,odor1_nolaser_lick = div_by_laser(odor1_lick,odor1_laser)
		odor2_laser_lick, odor2_nolaser_lick = div_by_laser(odor2_lick, odor2_laser)
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
		laser1_hit = 0
		laser1_miss = 0
		laser2_hit = 0
		laser2_miss = 0
		nolaser1_hit = 0
		nolaser1_miss = 0
		nolaser2_hit = 0
		nolaser2_miss = 0
		laser_trial = 0

		for tri in range(len(odor1_lick[:, 1])):
			if np.sum(odor1_laser[tri,0:200])>5:
				laser_trial = 1

			else:
				laser_trial = 0

			odor1_did = 0
			if np.sum(odor1_lick[tri, :]) == 0:
				empty_odor1 += 1
			# continue
			for ms in range(len(odor1_lick[1, :])):
				if (ms <= relative_time) and (odor1_lick[tri, ms] == 1):
					lickintime += 1
				elif (ms > relative_time) and (ms <= 1900) and (odor1_lick[tri, ms] == 1):
					lickiniti += 1
				if (odor1_pump[tri, ms] == 1 or odor1_airpuff[tri, ms] == 1) and (odor1_did == 0):
					if (np.sum(odor1_pump[tri, ms:ms + 50]) + np.sum(odor1_airpuff[tri, ms:ms + 50])) > 10:
						#print(tri)
						odor1_hit += 1
						odor1_did = 1
					if laser_trial == 1:

						laser1_hit += 1
					else:
						nolaser1_hit += 1


			if odor1_did == 0:
				odor1_miss += 1
				if laser_trial == 1:
					laser1_miss += 1
				else:
					nolaser1_miss += 1
		for tri in range(len(odor2_lick[:, 1])):
			odor2_did = 0
			if np.sum(odor2_laser[tri,0:200])>5:
				laser_trial = 1
			else:
				laser_trial = 0
			if np.sum(odor2_lick[tri, :]) == 0:
				empty_odor2 += 1
			# continue
			for ms in range(len(odor2_lick[1, :])):
				if (ms <= relative_time) and (odor2_lick[tri, ms] == 1):
					lickintime += 1
				elif (ms > relative_time) and (ms <= 1900) and (odor2_lick[tri, ms] == 1):
					lickiniti += 1
				if (odor2_pump[tri, ms] == 1 or odor2_airpuff[tri, ms] == 1) and (odor2_did == 0):
					if (np.sum(odor2_pump[tri, ms:ms + 50]) + np.sum(odor2_airpuff[tri, ms:ms + 50])) > 10:
						#print(tri)
						odor2_hit += 1
						odor2_did = 1
					if laser_trial == 1:
						laser2_hit += 1
					else:
						nolaser2_hit += 1
			if odor2_did == 0:
				odor2_miss += 1
				if laser_trial == 1:
					laser2_miss += 1
				else:
					nolaser2_miss += 1
		noact_trial = empty_odor1 + empty_odor2

		odor1_trial, _ = np.shape(odor1_lick)
		odor2_trial, _ = np.shape(odor2_lick)
		trials = odor1_trial + odor2_trial
	#	print(raw_file + ":\n" + "odor1 trials : %f\nodor2 trials : %f" % (odor1_trial, odor2_trial))
		if whichsgo == 1:
			hit = odor1_hit
			miss = odor1_miss
			fa = odor2_hit
			cr = odor2_miss
			laser_hit = laser1_hit
			laser_miss = laser1_miss
			laser_cr = laser2_miss
			laser_fa = laser2_hit
			nolaser_hit = nolaser1_hit
			nolaser_miss = nolaser1_miss
			nolaser_fa = nolaser2_hit
			nolaser_cr = nolaser2_miss
		else:
			hit = odor2_hit
			miss = odor2_miss
			fa = odor1_hit
			cr = odor1_miss
			laser_hit = laser2_hit
			laser_miss = laser2_miss
			laser_cr = laser1_miss
			laser_fa = laser1_hit
			nolaser_hit = nolaser2_hit
			nolaser_miss = nolaser2_miss
			nolaser_fa = nolaser1_hit
			nolaser_cr = nolaser1_miss
		if (hit + miss) > 1:
			accuracy = hit / (hit + miss)
		else:
			accuracy = 0
		laser_out = dPrime(laser_hit,laser_miss,laser_fa,laser_cr)
		print(nolaser_hit, nolaser_miss, nolaser_fa, nolaser_cr)
		nolaser_out = dPrime(nolaser_hit, nolaser_miss, nolaser_fa, nolaser_cr)
		laser_d = laser_out['d']
		laser_b = laser_out['b']

		nolaser_d = nolaser_out['d']
		nolaser_b = nolaser_out['b']

		saved = 0
		if (cr + fa) > 0:
			acc_nogo = cr / (cr + fa)
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

		print(raw_file + ":\n" + "odor1 trials : %f\nodor2 trials : %f" % (odor1_trial, odor2_trial))

		print(
			"lick on time : %f\nlick in iti : %f\nwhole trials : %f\nhit : %f\nmiss : %f\naccuracy percentage : %f\nfa : %f\ncorrect reject : %f" % (
				lickintime, lickiniti, trials, hit, miss, accuracy, fa, cr))
		print("no action trial num : %f\n" % (noact_trial))
		print("===============================================end=============================================")

		saved = 0
		# print("test:",odor1_laser[21,0:500],odor1_action[21,0:500],odor1_pump[21,0:500],odor1_lick[21,290:500])
		tr, ti = np.shape(odor1_laser_lick)
		trn, tin = np.shape(odor1_nolaser_lick)
		ntr, nti = np.shape(odor2_laser_lick)
		trn2, tin2 = np.shape(odor2_nolaser_lick)
		real_tr =0
		real_trn = 0
		real_ntr = 0
		real_trn2 = 0
		for i in range(len(odor1_laser_lick[:,1])):
			if np.sum(odor1_laser_lick[i,200:500]) > 1:
				real_tr += 1
		for i in range(len(odor1_nolaser_lick[:, 1])):
			if np.sum(odor1_nolaser_lick[i, 200:500]) > 1:
				real_trn += 1
		for i in range(len(odor2_laser_lick[:, 1])):
			if np.sum(odor2_laser_lick[i, 200:500]) > 1:
				real_ntr += 1
		for i in range(len(odor2_nolaser_lick[:, 1])):
			if np.sum(odor2_nolaser_lick[i, 200:500]) > 1:
				real_trn2 += 1

		print("trials!:\n")
		print(ntr,trn2)
		print(
			"odor1:\nlaser lick : %f\nno-laser lick : %f\nodor2:\nlaser lick: %f\nno-laser lick : %f\n" % (
			np.sum(odor1_laser_lick[:,:500])/tr, np.sum(odor1_nolaser_lick[:,:500])/trn, np.sum(odor2_laser_lick[:,:500])/ntr,
			np.sum(odor2_nolaser_lick[:,:500])/trn2))

		for i in saved_files:
			if i == name:
				saved = 1
				break
		odor1_plot = name + 'odor1 with laser'
		odor2_plot = name + 'odor2 with laser'
		odor1_aver_laser_first=0
		odor1_aver_nolaser_first=0
		odor2_aver_laser_first=0
		odor2_aver_nolaser_first=0
		if (np.sum(odor1_laser_lick) != 0):
			odor1_aver_laser_first,odor1_aver_nolaser_first = first_lick_plot(odor1_laser_lick, odor1_nolaser_lick, odor1_plot,delay = 200)
			averplot(odor1_laser_lick, odor1_nolaser_lick, odor1_plot)

		if (np.sum(odor2_laser_lick) != 0):
			odor2_aver_laser_first, odor2_aver_nolaser_first = first_lick_plot(odor2_laser_lick, odor2_nolaser_lick, odor2_plot,delay = 200)
			averplot(odor2_laser_lick, odor2_nolaser_lick, odor2_plot)

		if saved == 0:
			sheet.write(len(saved_files), 0, name)
			sheet.write(len(saved_files), 1, str(odor1_trial))
			sheet.write(len(saved_files), 2, str(odor2_trial))
			sheet.write(len(saved_files), 3, str(trials))
			sheet.write(len(saved_files), 4, str(tr))
			sheet.write(len(saved_files), 5, str(ntr))
			sheet.write(len(saved_files), 6, str(laser_hit))
			sheet.write(len(saved_files), 7, str(laser_miss))
			sheet.write(len(saved_files), 8, str(laser_fa))
			sheet.write(len(saved_files), 9, str(laser_cr))
			sheet.write(len(saved_files), 10, str(laser_d))
			sheet.write(len(saved_files), 11, str(laser_b))
			sheet.write(len(saved_files), 12, str(np.sum(odor1_laser_lick[:,200:500])/real_tr))
			sheet.write(len(saved_files), 13, str(np.sum(odor2_laser_lick[:,200:500])/real_ntr))
			sheet.write(len(saved_files), 14, str(odor1_aver_laser_first))
			sheet.write(len(saved_files), 15, str(odor2_aver_laser_first))
			sheet.write(len(saved_files), 16, str(nolaser_hit))
			sheet.write(len(saved_files), 17, str(nolaser_miss))
			sheet.write(len(saved_files), 18, str(nolaser_fa))
			sheet.write(len(saved_files), 19, str(nolaser_cr))
			sheet.write(len(saved_files), 20, str(nolaser_d))
			sheet.write(len(saved_files), 21, str(nolaser_b))
			sheet.write(len(saved_files), 22, str(np.sum(odor1_nolaser_lick[:,200:500])/real_trn))
			sheet.write(len(saved_files), 23, str(np.sum(odor2_nolaser_lick[:,200:500])/real_trn2))
			sheet.write(len(saved_files), 24, str(odor1_aver_nolaser_first))
			sheet.write(len(saved_files), 25, str(odor2_aver_nolaser_first))
			os.remove('go_nogo_result_laser_08.xls')
			newwb.save('go_nogo_result_laser_08.xls')
		i = 0

		for j in range(tr):
			while i < ti:
				try:
					if odor1_laser_lick[j][i] == 1:
						odor1_laser_lick[j][i + 1] = 1
						odor1_laser_lick[j][i + 2] = 1
						odor1_laser_lick[j][i + 3] = 1
						odor1_laser_lick[j][i + 4] = 1
						odor1_laser_lick[j][i + 5] = 1
						#odor1_laser_lick[j][i + 6] = 1
						#odor1_laser_lick[j][i + 7] = 1
						i += 6
					# print(go_lick[j][i + 7])
					elif odor1_nolaser_lick[j][i] == 1:
						odor1_nolaser_lick[j][i + 1] = 1
						odor1_nolaser_lick[j][i + 2] = 1
						odor1_nolaser_lick[j][i + 3] = 1
						odor1_nolaser_lick[j][i + 4] = 1
						odor1_nolaser_lick[j][i + 5] = 1
					#	odor1_nolaser_lick[j][i + 6] = 1
					#	odor1_nolaser_lick[j][i + 7] = 1
						i += 6
					else:
						i += 1
				except:
					i += 1
				# print(go_lick[j][i + 7])
			i = 0
		i = 0
		for j in range(ntr):
			while i < nti:
				try:
					if odor2_laser_lick[j][i] == 1:
						odor2_laser_lick[j][i + 1] = 1
						odor2_laser_lick[j][i + 2] = 1
						odor2_laser_lick[j][i + 3] = 1
						odor2_laser_lick[j][i + 4] = 1
						odor2_laser_lick[j][i + 5] = 1
					#	odor2_laser_lick[j][i + 6] = 1
					#	odor2_laser_lick[j][i + 7] = 1
						i += 6
					elif odor2_nolaser_lick[j][i] == 1:
						odor2_nolaser_lick[j][i + 1] = 1
						odor2_nolaser_lick[j][i + 2] = 1
						odor2_nolaser_lick[j][i + 3] = 1
						odor2_nolaser_lick[j][i + 4] = 1
						odor2_nolaser_lick[j][i + 5] = 1
					#	odor2_nolaser_lick[j][i + 6] = 1
					#	odor2_nolaser_lick[j][i + 7] = 1
						i += 6


					else:
						i += 1
				except:
					i += 1
			i = 0
		odor1_ras = name + 'odor1 with laser'
		odor2_ras = name + 'odor2 with laser'
		raster_laser(odor1_laser_lick, odor1_nolaser_lick, odor1_ras,delay = 200)
		raster_laser(odor2_laser_lick, odor2_nolaser_lick, odor2_ras,delay = 200)


