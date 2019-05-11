from xlutils.copy import copy
import xlwt, xlrd,csv
from openpyxl import workbook
import sys, os

user_path = "C:/Users/manggny/Desktop/data/user_record"
sys.path.append("C:/Users/manggny/Desktop/data/user_record")
filelist = os.listdir(user_path)

for filename in filelist:
	filename = user_path + '/'+filename
	if filename == 'C:/Users/manggny/Desktop/data/user_record/all_users_records.xls':
		continue
	else:
		oldwb = xlrd.open_workbook('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
		newwb = copy(oldwb)
		sheet = newwb.get_sheet(0)
		old_sheet = oldwb.sheet_by_index(0)
		now_wb = csv.reader(open(filename,'r'))
		# now_sheet = now_wb.get_sheet(0)
		# saved_files = now_sheet.row_values(1)
		print(filename)
		q = 0
		for i in now_wb:
			print('now '+i[0])
			if i[0]  == 'rank':
				continue
			else:
				saved_files = old_sheet.col_values(0)
				for k in range(len(i)):
					sheet.write(len(saved_files)+q, k, i[k])
				q += 1
		os.remove('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
		newwb.save('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
