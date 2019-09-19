import sys, os
import numpy as np
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list
from go.funcs import div_by_laser,make_gonogolick,div_by_odor,raster


if __name__ == '__main__':
	path = "F:/Insula-Gcamp6/behav/gonogo-record"#F:/ACC-Camk2/Gono-go/behavior_trainning/Camk2_chr2/12.23_"#F:/ACC-Camk2/Gono-go/behavior_trainning/Camk2_GTACR1/onlygo"#F:/ACC-Camk2/Gono-go/behavior_trainning/Camk2_chr2/habi"
	filelist = os.listdir(path)
	filelist_current = os.listdir()
	exist = 0

	for names in filelist_current:
		if names == 'go_nogo_result_laser.xls':
			exist = 1
			break
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
		sheet.write(0, 10, 'odor1 laser_lick')
		sheet.write(0, 11, 'odor2 laser lick')
		sheet.write(0, 12, 'no-Laser hit')
		sheet.write(0, 13, 'no-Laser miss')
		sheet.write(0, 14, 'no-Laser FA')
		sheet.write(0, 15, 'no-Laser CR')
		sheet.write(0, 16, 'odor1 no-laser_lick')
		sheet.write(0, 17, 'odor2 no-laser_lick')

		book.save('go_nogo_result_laser.xls')

	for raw_file in filelist:


		oldwb = xlrd.open_workbook('go_nogo_result_laser.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		saved_files = old_sheet.col_values(0)

		print("================================================ start =======================================")


		filename = path + "/" + raw_file
		name, _ = raw_file.split(".")
		exname = "Raster_of_" + name + ".png"
		savepath = "figures/raster"
		saved_filelist = os.listdir(savepath)
		if exname in saved_filelist:
			print("this raster is exist already! Skip" + raw_file)
			continue
		print(name)


		if name in saved_files:
			print("already exist, skip " + name)
			continue

		number, jieduan, day, godor, Hz, *_ = raw_file.split("_")
		odor1, odor2, lick, pump, action, airpuff, laser = make_list(filename)
		odor1_lick,odor2_lick = make_gonogolick(odor1,odor2,lick,delay=200)
		odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(odor1,odor2,action,airpuff,pump,laser,delay=200)


		# odor1 / odor2_lick_laser/nolaser
		# odor1 / odor2_action_laser/nolaser
		tr,ti = np.shape(odor1_lick)
		tr2, ti2 = np.shape(odor2_lick)
		i = 0
		for j in range(tr):
			while i < ti:
				try:
					if odor1_lick[j][i] == 1:
						odor1_lick[j][i + 1] = 1
						odor1_lick[j][i + 2] = 1
						odor1_lick[j][i + 3] = 1
						odor1_lick[j][i + 4] = 1
						odor1_lick[j][i + 5] = 1
						odor1_lick[j][i + 6] = 1
						odor1_lick[j][i + 7] = 1
						i += 8
						#print(go_lick[j][i + 7])
					else:
						i += 1
				except:
					i += 1
					#print(go_lick[j][i + 7])
			i = 0
		i=0
		for j in range(tr2):
			while i < ti2:
				try:
					if odor2_lick[j][i] == 1:
						odor2_lick[j][i + 1] = 1
						odor2_lick[j][i + 2] = 1
						odor2_lick[j][i + 3] = 1
						odor2_lick[j][i + 4] = 1
						odor2_lick[j][i + 5] = 1
						odor2_lick[j][i + 6] = 1
						odor2_lick[j][i + 7] = 1
						i += 8
					else:
						i += 1
				except:
					i += 1
			i=0
		if godor == "odor2":
			raster(odor2_lick,odor1_lick,name,"Go_trials_lick","No-Go_trials_lick")
		else:
			raster(odor1_lick, odor2_lick, name, "Go_trials_lick", "No-Go_trials_lick")

		#print(len(odor1_lick[1,:]))