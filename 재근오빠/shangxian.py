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

	mean_baogao_end = np.zeros(11)
	mean_shishi_end = np.zeros(11)
	mean_chuxi_end = np.zeros(11)
	mean_shangshi_end = np.zeros(11)
	mean_baogao_ex = np.zeros(11)
	mean_shishi_ex = np.zeros(11)
	mean_chuxi_ex = np.zeros(11)
	mean_shangshi_ex = np.zeros(11)

	for i in range(len(code_list)):
		dummy = str(int(code_list[i]))
		while len(dummy) < 6:
			dummy = '0'+dummy
		code_list[i] = dummy


	for i in range(len(code_list)):

		filename = path+'/'+str(code_list[i])+'.xlsx'

		#baogao
		end_baogao,ex_baogao,send_baogao,sex_baogao = load_data(filename,baogao_date[i])
		# shishi
		end_shishi, ex_shishi,send_shishi, sex_shishi = load_data(filename, shishi_date[i])
		# chuxi
		end_chuxi, ex_chuxi,send_chuxi, sex_chuxi = load_data(filename, chuxi_date[i])
		# shangshi
		end_shangshi, ex_shangshi,send_shangshi, sex_shangshi = load_data(filename, shangshi_date[i])

		for j in range(len(end_baogao)):
			# mean_baogao_end[j] += (end_baogao[j]-send_baogao[j])/send_baogao[j]
			# mean_shishi_end[j] += (end_shishi[j]-send_shishi[j])/send_shishi[j]
			# mean_chuxi_end[j] += (end_chuxi[j]-send_chuxi[j])/send_chuxi[j]
			# mean_shangshi_end[j] += (end_shangshi[j]-send_shangshi[j])/send_shangshi[j]
			# mean_baogao_ex[j] += (ex_baogao[j]-sex_baogao[j])/sex_baogao[j]
			# mean_shishi_ex[j] += (ex_shishi[j]-sex_shishi[j])/sex_shishi[j]
			# mean_chuxi_ex[j] += (ex_chuxi[j]-sex_chuxi[j])/sex_chuxi[j]
			# mean_shangshi_ex[j] += (ex_shangshi[j]-sex_shangshi[j])/sex_shangshi[j]
			#
			mean_baogao_end[j] += end_baogao[j] - send_baogao[j]
			mean_shishi_end[j] += end_shishi[j] - send_shishi[j]
			mean_chuxi_end[j] += end_chuxi[j] - send_chuxi[j]
			mean_shangshi_end[j] += end_shangshi[j] - send_shangshi[j]
			mean_baogao_ex[j] += ex_baogao[j] - sex_baogao[j]
			mean_shishi_ex[j] += ex_shishi[j] - sex_shishi[j]
			mean_chuxi_ex[j] += ex_chuxi[j] - sex_chuxi[j]
			mean_shangshi_ex[j] += ex_shangshi[j] - sex_shangshi[j]

	mean_baogao_end = mean_baogao_end/len(code_list)
	mean_shishi_end = mean_shishi_end/len(code_list)
	mean_chuxi_end = mean_chuxi_end/len(code_list)
	mean_shangshi_end = mean_shangshi_end/len(code_list)
	mean_baogao_ex = mean_baogao_ex/len(code_list)
	mean_shishi_ex = mean_shishi_ex/len(code_list)
	mean_chuxi_ex = mean_chuxi_ex/len(code_list)
	mean_shangshi_ex = mean_shangshi_ex/len(code_list)
	print(len(code_list))

	print('mean_baogao_end')
	print(mean_baogao_end)
	print('mean_shishi_end')
	print(mean_shishi_end)
	print('mean_chuxi_end')
	print(mean_chuxi_end)
	print('mean_shangshi_end')
	print(mean_shangshi_end)
	print('mean_baogao_ex')
	print(mean_baogao_ex)
	print('mean_shishi_ex')
	print(mean_shishi_ex)
	print('mean_chuxi_ex')
	print(mean_chuxi_ex)
	print('mean_shangshi_ex')
	print(mean_shangshi_ex)

	# 	end_before_fenge = np.array(end_before_fenge)
	# 	#print(end_before_fenge)
	# 	end_fenge=np.array(end_fenge)
	# 	end_after_fenge=np.array(end_after_fenge)
	# 	ex_before_fenge= np.array(ex_before_fenge)
	# 	ex_fenge = np.array(ex_fenge)
	# 	ex_after_fenge = np.array(ex_after_fenge)
	#
	# 	mean_before_end.append(np.mean(end_before_fenge))
	# 	mean_end.append(np.mean(end_fenge))
	# 	mean_after_end.append(np.mean(end_after_fenge))
	# 	mean_before_ex.append(np.mean(ex_before_fenge))
	# 	mean_ex.append(np.mean(ex_fenge))
	# 	mean_after_ex.append(np.mean(ex_after_fenge))
	#
	# m_be_end = sum(mean_before_end)/len(mean_before_end)
	# m_end = sum(mean_end) / len(mean_end)
	# m_after_end = sum(mean_after_end) / len(mean_after_end)
	# m_be_ex = sum(mean_before_ex) / len(mean_before_ex)
	# m_ex = sum(mean_ex) / len(mean_ex)
	# m_after_ex = sum(mean_after_ex) / len(mean_after_ex)


		# if i == 0:
		# 	mean_before_end = end_before_fenge
		# 	mean_end = end_fenge
		# 	mean_after_end = end_after_fenge
		# 	mean_before_ex = ex_before_fenge
		# 	mean_ex = ex_fenge
		# 	mean_after_ex = ex_after_fenge
		# else:
		# 	for j in range(30):
		# 		#print(len(mean_before_end),len(end_before_fenge))
		# 		mean_before_end[j] += end_before_fenge[j]
		# 		#mean_end = end_fenge
		# 		mean_after_end[j] = end_after_fenge[j]
		# 		mean_before_ex[j] = ex_before_fenge[j]
		# 		#mean_ex = ex_fenge
		# 		mean_after_ex[j] = ex_after_fenge[j]



	# print(mean_before_end)







