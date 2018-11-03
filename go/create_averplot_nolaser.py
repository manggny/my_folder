import sys, os
import numpy as np
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
from go.funcs import make_list,first_lick_plot
from go.funcs import div_by_laser,make_gonogolick,div_by_odor,averplot


if __name__ == '__main__':
	path = "F:/gonogodata/nodelay"
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
		if raw_file == 'go_nogo_result_laser.xls':
			continue
		oldwb = xlrd.open_workbook('go_nogo_result_laser.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		saved_files = old_sheet.col_values(0)

		print("================================================ start =======================================")


		filename = path + "/" + raw_file
		name, _ = raw_file.split(".")
		print(name)

		if name in saved_files:
			print("already exist, skip " + name)
			continue

		number, jieduan, day, godor, Hz, *_ = raw_file.split("_")
		odor1, odor2, lick, pump, action, airpuff, laser = make_list(filename)
		odor1_lick,odor2_lick = make_gonogolick(odor1,odor2,lick)
		odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(odor1,odor2,action,airpuff,pump,laser)
		odor1_action_laser,odor1_action_nolaser = div_by_laser(odor1_action,odor1_laser)
		odor1_lick_laser, odor1_lick_nolaser = div_by_laser(odor1_lick, odor1_laser)
		odor2_action_laser, odor2_action_nolaser = div_by_laser(odor2_action, odor2_laser)
		odor2_lick_laser, odor2_lick_nolaser = div_by_laser(odor2_lick, odor2_laser)
		# odor1 / odor2_lick_laser/nolaser
		# odor1 / odor2_action_laser/nolaser
		tr,ti = np.shape(odor1_lick)
		tr2, ti2 = np.shape(odor2_lick)

		if godor == "odor2":
			averplot(odor2_lick,odor1_lick,name)
		else:
			averplot(odor1_lick, odor2_lick, name)

		if godor == "odor2":
			first_lick_plot(odor2_lick,odor1_lick,name)
		else:
			first_lick_plot(odor1_lick, odor2_lick, name)