from xlutils.copy import copy
import xlwt, xlrd,csv
from openpyxl import workbook
import sys, os

user_path = "C:/Users/manggny/Desktop/data/user_record"
round_path = "C:/Users/manggny/Desktop/data/round_record"

filelist = os.listdir(round_path)

oldwb = xlrd.open_workbook('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
newwb = copy(oldwb)
sheet = newwb.get_sheet(0)
old_sheet = oldwb.sheet_by_index(0)
round = old_sheet.col_values(1) # user name
#round = round[1:]

username = old_sheet.col_values(2) # user name
#username = username[1:]

print(len(round))

for i in range(len(round)):
	if i == 0:
		continue

	score = -1000
	rank = 0
	filename = round_path + '/round_'+round[i]+'.csv'

	with open(filename, 'r') as csvfile:
		reader = csv.reader(csvfile)
		rows = [row for row in reader]
		r_score = [row[5] for row in rows]
		r_username = [a[0] for a in rows]

		r_username = r_username[1:]
		r_score = r_score[1:]
		#print(filename)
		print(r_username)
		print(r_score)

	for k in range(len(r_username)):
		if r_username[k] == username[i]:
			score = float(r_score[k])
			break

	for k in range(len(r_score)):
		r_score[k] = float(r_score[k])

	r_score.sort()

	for k in range(len(r_score)):
		if r_score[k] == score:
			rank = k+1
			break

	sheet.write(i, 13, str((rank-1)/(len(r_score)-1)))

os.remove('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
newwb.save('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')







	#now_wb = csv.reader(open(filename, 'r'))


#
# for filename in filelist:
# 	filename = user_path + '/'+filename
# 	if filename == 'C:/Users/manggny/Desktop/data/user_record/all_users_records.xls':
# 		continue
# 	else:
# 		oldwb = xlrd.open_workbook('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
# 		newwb = copy(oldwb)
# 		sheet = newwb.get_sheet(0)
# 		old_sheet = oldwb.sheet_by_index(0)
# 		now_wb = csv.reader(open(filename,'r'))
# 		# now_sheet = now_wb.get_sheet(0)
# 		# saved_files = now_sheet.row_values(1)
# 		print(filename)
# 		q = 0
# 		for i in now_wb:
# 			print('now '+i[0])
# 			if i[0]  == 'rank':
# 				continue
# 			else:
# 				saved_files = old_sheet.col_values(0)
# 				for k in range(len(i)):
# 					sheet.write(len(saved_files)+q, k, i[k])
# 				q += 1
# 		os.remove('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
# 		newwb.save('C:/Users/manggny/Desktop/data/user_record/all_users_records.xls')
