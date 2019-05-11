from xlutils.copy import copy
import xlwt, xlrd,sys,os
from datetime import datetime,timedelta
from xlrd import xldate_as_tuple
import numpy as np
from statsmodels.stats.anova import anova_lm

def load_data(filename,date): # 11 datas around the date.
	fenge = xlrd.open_workbook(filename)
	sheet = fenge.sheet_by_index(0)
	raw_end = sheet.col_values(6)
	raw_exchange = sheet.col_values(7)

	shichang = xlrd.open_workbook('300zhibiao.xlsx')
	ssheet = shichang.sheet_by_index(0)
	sraw_end = ssheet.col_values(6)
	sraw_exchange = ssheet.col_values(7)

	end_price = []
	ex_amount = []
	for i in range(1,len(raw_end)):
		if isinstance(raw_end[i],str):
			continue
		else:
			end_price.append(raw_end[i])
			ex_amount.append(raw_exchange[i])

	send_price = []
	sex_amount = []
	for i in range(1, len(sraw_end)):
		if isinstance(sraw_end[i], str):
			continue
		else:
			send_price.append(sraw_end[i])
			sex_amount.append(sraw_exchange[i])

	rate_end = []
	rate_ex = []
	for i in range(1,len(end_price)):
		if i == 1:
			rate_end.append(0)
			rate_ex.append(0)
		elif end_price[i-1] == 0 or ex_amount[i-1] == 0:
			print(filename)
			return
		else:
			rate_end.append((end_price[i]-end_price[i-1])/end_price[i-1])
			rate_ex.append((ex_amount[i]-ex_amount[i-1])/ex_amount[i-1])

	srate_end = []
	srate_ex = []
	for i in range(1, len(send_price)):
		if i == 1:
			srate_end.append(0)
			srate_ex.append(0)
		elif send_price[i - 1] == 0 or sex_amount[i - 1] == 0:
			print('!!!')
			return
		else:
			srate_end.append((send_price[i] - send_price[i - 1]) / send_price[i - 1])
			srate_ex.append((sex_amount[i] - sex_amount[i - 1]) / sex_amount[i - 1])

	date_list = []
	for i in range(1,len(raw_end)):
		cell = sheet.cell_value(i, 2)
		if cell == '':
			continue
		date1 = datetime(*xldate_as_tuple(cell, 0))
		cell = date1.strftime('%Y/%m/%d')
		date_list.append(cell)

	sdate_list = []
	for i in range(1, len(sraw_end)):
		scell = ssheet.cell_value(i, 2)
		if scell == '':
			continue
		sdate = datetime(*xldate_as_tuple(scell, 0))
		scell = sdate.strftime('%Y/%m/%d')
		sdate_list.append(scell)

	start_p = 0
	ss_p = 0

	for i in range(1,len(date_list)):
		if date_list[i]>= date and date_list[i-1]<date:
			start_p = i

			break

	for i in range(1,len(sdate_list)):
		if sdate_list[i]>= date and sdate_list[i-1]<date:
			ss_p = i

			break


	end_datas = rate_end[start_p-5:start_p+6]
	ex_datas = rate_ex[start_p - 5:start_p + 6]

	s_end_data = srate_end[ss_p-5:ss_p+6]
	s_ex_data = srate_ex[ss_p - 5: ss_p + 6]

	#print(len(end_datas[:][1]))
	return end_datas,ex_datas,s_end_data,s_ex_data


if __name__=="__main__":
	fenge = xlrd.open_workbook('fenge.xlsx')
	sheet = fenge.sheet_by_index(0)
	raw_code = sheet.col_values(0)
	code_list = []
	for i in range(1,len(raw_code)):
		code_list.append(raw_code[i])
	baogao_date = []
	shishi_date = []
	chuxi_date = []
	shangshi_date = []

	for i in range(1,len(raw_code)):
		cell_baogao = sheet.cell_value(i, 2)
		cell_shishi = sheet.cell_value(i, 11)
		cell_chuxi = sheet.cell_value(i, 14)
		cell_shangshi = sheet.cell_value(i, 16)

		baogao_date1 = datetime(*xldate_as_tuple(cell_baogao, 0))
		shishi_date1 = datetime(*xldate_as_tuple(cell_shishi, 0))
		chuxi_date1 = datetime(*xldate_as_tuple(cell_chuxi, 0))
		shangshi_date1 = datetime(*xldate_as_tuple(cell_shangshi, 0))

		cell_baogao = baogao_date1.strftime('%Y/%m/%d')
		cell_shishi = shishi_date1.strftime('%Y/%m/%d')
		cell_chuxi = chuxi_date1.strftime('%Y/%m/%d')
		cell_shangshi = shangshi_date1.strftime('%Y/%m/%d')

		baogao_date.append(cell_baogao)
		shishi_date.append(cell_shishi)
		chuxi_date.append(cell_chuxi)
		shangshi_date.append(cell_shangshi)



	path = 'C:/Users/manggny/PycharmProjects/my_folder/재근오빠/psx'
	file_lists = os.listdir('C:/Users/manggny/PycharmProjects/my_folder/재근오빠/psx')


	for i in range(len(code_list)):
		dummy = str(int(code_list[i]))
		while len(dummy) < 6:
			dummy = '0'+dummy
		code_list[i] = dummy

	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
	sheet1 = book.add_sheet('baogao', cell_overwrite_ok=True)
	sheet2 = book.add_sheet('shishi', cell_overwrite_ok=True)
	sheet3 = book.add_sheet('chuxi', cell_overwrite_ok=True)
	sheet4 = book.add_sheet('shangshi', cell_overwrite_ok=True)
	sheet1.write(0, 0, 'name')
	sheet1.write(0, 1, 'D -5')
	sheet1.write(0, 2, 'D -4')
	sheet1.write(0, 3, 'D -3')
	sheet1.write(0, 4, 'D -2')
	sheet1.write(0, 5, 'D -1')
	sheet1.write(0, 6, 'D')
	sheet1.write(0, 7, 'D +1')
	sheet1.write(0, 8, 'D +2')
	sheet1.write(0, 9, 'D +3')
	sheet1.write(0, 10, 'D +4')
	sheet1.write(0, 11, 'D +5')
	sheet4.write(0, 0, 'name')
	sheet4.write(0, 1, 'D -5')
	sheet4.write(0, 2, 'D -4')
	sheet4.write(0, 3, 'D -3')
	sheet4.write(0, 4, 'D -2')
	sheet4.write(0, 5, 'D -1')
	sheet4.write(0, 6, 'D')
	sheet4.write(0, 7, 'D +1')
	sheet4.write(0, 8, 'D +2')
	sheet4.write(0, 9, 'D +3')
	sheet4.write(0, 10, 'D +4')
	sheet4.write(0, 11, 'D +5')
	sheet2.write(0, 0, 'name')
	sheet2.write(0, 1, 'D -5')
	sheet2.write(0, 2, 'D -4')
	sheet2.write(0, 3, 'D -3')
	sheet2.write(0, 4, 'D -2')
	sheet2.write(0, 5, 'D -1')
	sheet2.write(0, 6, 'D')
	sheet2.write(0, 7, 'D +1')
	sheet2.write(0, 8, 'D +2')
	sheet2.write(0, 9, 'D +3')
	sheet2.write(0, 10, 'D +4')
	sheet2.write(0, 11, 'D +5')
	sheet3.write(0, 0, 'name')
	sheet3.write(0, 1, 'D -5')
	sheet3.write(0, 2, 'D -4')
	sheet3.write(0, 3, 'D -3')
	sheet3.write(0, 4, 'D -2')
	sheet3.write(0, 5, 'D -1')
	sheet3.write(0, 6, 'D')
	sheet3.write(0, 7, 'D +1')
	sheet3.write(0, 8, 'D +2')
	sheet3.write(0, 9, 'D +3')
	sheet3.write(0, 10, 'D +4')
	sheet3.write(0, 11, 'D +5')




	for i in range(len(code_list)):

		filename = path+'/'+str(code_list[i])+'.xlsx'
		sheet1.write(i+1, 0, str(code_list[i]))
		sheet2.write(i+1, 0, str(code_list[i]))
		sheet3.write(i+1, 0, str(code_list[i]))
		sheet4.write(i+1, 0, str(code_list[i]))

		#baogao
		end_baogao,ex_baogao,send_baogao,sex_baogao = load_data(filename,baogao_date[i])
		# shishi
		end_shishi, ex_shishi,send_shishi, sex_shishi = load_data(filename, shishi_date[i])
		# chuxi
		end_chuxi, ex_chuxi,send_chuxi, sex_chuxi = load_data(filename, chuxi_date[i])
		# shangshi
		end_shangshi, ex_shangshi,send_shangshi, sex_shangshi = load_data(filename, shangshi_date[i])

		for j in range(len(ex_baogao)):
			# sheet1.write(i+1, j + 1, str((ex_baogao[j]-sex_baogao[j])))
			# sheet2.write(i+1, j + 1, str((ex_shishi[j]-sex_shishi[j])))
			# sheet3.write(i+1, j + 1, str((ex_chuxi[j]-sex_chuxi[j])))
			# sheet4.write(i+1, j + 1, str((ex_shangshi[j]-sex_shangshi[j])))
			sheet1.write(i + 1, j + 1, str((end_baogao[j] - send_baogao[j])))
			sheet2.write(i + 1, j + 1, str((end_shishi[j] - send_shishi[j])))
			sheet3.write(i + 1, j + 1, str((end_chuxi[j] - send_chuxi[j])))
			sheet4.write(i + 1, j + 1, str((end_shangshi[j] - send_shangshi[j])))

	book.save('end_price_result.xls')