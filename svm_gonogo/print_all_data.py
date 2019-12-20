from xlutils.copy import copy
import xlwt, xlrd,os
import numpy as np
def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

if __name__=="__main__":
	test = np.zeros(700)

	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_20%/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	filelist = os.listdir(pkls_path)
	k = 0

	for file in filelist:
		name,s = file.split('.')
		if s != 'pkl':
			continue

		data = unpickle(pkls_path + file)

		odor1_hit = data['odor1'][0]
		odor1_hit_mean=np.zeros(700)
		odor2_hit_mean = np.zeros(700)
		odor2_noact_mean = np.zeros(700)
		odor2_miss_mean = np.zeros(700)
		tr,ti = odor1_hit.shape
		odor1_miss = data['odor1'][1]
		odor1_noact = data['odor1'][2]
		odor2_hit = data['odor2'][0]
		odor2_miss = data['odor2'][1]
		odor2_noact = data['odor2'][2]
		odor2_hit_pre = data['odor2_pre'][0]
		odor2_miss_pre = data['odor2_pre'][1]
		print(type(data['odor2_pre'][1]))
		odor2_noact_pre = data['odor2_pre'][2]
		odor1_hit_pre = data['odor1_pre'][0]
		#print(len(odor1_hit_pre))
		odor1_miss_pre = data['odor1_pre'][1]
		odor1_noact_pre = data['odor1_pre'][2]
		#print(odor1_noact_pre,odor1_hit_pre)

		tr2,*_ = odor2_noact.shape
		tr3,*_ = odor2_miss.shape
		print(tr2,tr3)
		if tr2 == 0 and tr3 >0:
			odor2_cr = odor2_miss
			odor2_cr_pre = odor2_miss_pre
		elif tr3 == 0 and tr2 > 0:
			odor2_cr = odor2_noact
			odor2_cr_pre = odor2_noact_pre
		elif tr3>0 and tr2>0:
			odor2_cr = np.vstack((odor2_miss,odor2_noact))
			odor2_miss_pre.extend(odor2_noact_pre)
			odor2_cr_pre = odor2_miss_pre




		#odor1_m = np.zeros(700)
		tr2,*_= odor1_noact.shape
		tr3,*_ = odor1_miss.shape
		#print(ti2,ti3)
		if np.ndim(odor1_noact)>1 and np.ndim(odor1_miss) > 1:
			tr2, ti2 = odor1_noact.shape
			tr3, ti3 = odor1_miss.shape
			if tr2 == 0 or ti2 == 0:
				odor1_m = odor1_miss
				odor1_m_pre = odor1_miss_pre
			elif tr3 ==0 or ti3 == 0:
				odor1_m = odor1_noact
				odor1_m_pre = odor1_noact_pre
			else:
				odor1_m = np.vstack((odor1_miss, odor1_noact))

		elif np.ndim(odor1_noact)<2:
			odor1_m = odor1_miss
			odor1_m_pre = odor1_miss_pre
		elif  np.ndim(odor1_miss)<2:
			odor1_m = odor1_noact
			odor1_m_pre = odor1_noact_pre
		odor1_miss_pre.extend(odor1_noact_pre)
		odor1_m_pre = odor1_miss_pre
		odor2_cr_mean = np.zeros(700)
		odor1_m_mean = np.zeros(700)
		odor1_miss_mean = np.zeros(700)
		tr,*_ = np.shape(odor1_miss)
		ntr,*_ = np.shape(odor2_hit)
		print(file)
		# for i in range(ntr):
		# 	print(odor1_m[i,100:110])
		for i in range(ti):
			odor1_hit_mean[i] = np.mean(odor1_hit[:,i])
			odor1_m_mean[i] = np.mean(odor1_m[:, i])
			# if tr > 0 and tr < 200:
			# 	print(odor1_miss.shape)
			# 	odor1_miss_mean[i] = np.mean(odor1_m[:, i])
			odor2_hit_mean[i] = np.mean(odor2_hit[:,i])
			odor2_cr_mean[i] = np.mean(odor2_cr[:,i])
			# odor2_noact_mean[i] = np.mean(odor2_noact[:, i])
			# odor2_miss_mean[i] = np.mean(odor2_miss[:, i])
		print('odor2 fa', np.shape(odor2_hit))
		print('odor2 cr', np.shape(odor2_cr))
		print('odor1 miss', np.shape(odor1_m))
		print('odor1 hit', np.shape(odor1_hit))

		#


		#sheet.write(0, k, file)
		if k == 0:
			print('k')
			go_h = odor1_hit
			go_h_pre = odor1_hit_pre
			go_m = odor1_m
			go_m_pre = odor1_m_pre
			nogo_cr = odor2_cr
			nogo_cr_pre = odor2_cr_pre
			nogo_fa = odor2_hit
			nogo_fa_pre = odor2_hit_pre
		else:
			print('kk')
			go_h =  np.vstack((go_h, odor1_hit))
			go_m = np.vstack((go_m, odor1_m))
			nogo_cr = np.vstack((nogo_cr, odor2_cr))
			nogo_fa = np.vstack((nogo_fa, odor2_hit))
			go_h_pre.extend(odor1_hit_pre)
			go_m_pre.extend(odor1_m_pre)
			nogo_fa_pre.extend(odor2_hit_pre)
			nogo_cr_pre.extend(odor2_cr_pre)
		print(len(go_h_pre))


		# for i in range(90,110):
		#
		# 	sheet.write(i-89, k, str(odor1_hit_mean[i]))
		# 	sheet.write(i - 89, k + 15, str(odor1_m_mean[i]))
		# 	sheet.write(i-60, k, str(odor2_cr_mean[i]))
		# 	sheet.write(i - 60, k + 15, str(odor2_hit_mean[i]))
		k += 1

	print(nogo_fa.shape)
	t_mean = np.zeros(700)
	oldwb = xlrd.open_workbook('result_all_20.xls')
	newwb = copy(oldwb)
	sheet_gohit = newwb.get_sheet(0)
	sheet_gom = newwb.get_sheet(1)
	sheet_nogocr = newwb.get_sheet(2)
	sheet_nogofa = newwb.get_sheet(3)

	sheet_gohit.write(0, 0, 'go-hit trials')
	sheet_gom.write(0, 0, 'go-miss trials')
	sheet_nogocr.write(0, 0, 'nogo-cr trials')
	sheet_nogofa.write(0, 0, 'nogo-fa trials')
	#
	tr,ti =go_h.shape
	for i in range(tr):
		for j in range(100,125):
			sheet_gohit.write(i, j-89, go_h[i,j])
		sheet_gohit.write(i, 15, go_h_pre[i])

	tr, ti = go_m.shape
	for i in range(tr):
		for j in range(100, 125):
			sheet_gom.write(i, j-89, go_m[i, j])
		sheet_gom.write(i, 15, go_m_pre[i])

	tr, ti = nogo_cr.shape
	for i in range(tr):
		for j in range(100, 125):
			sheet_nogocr.write(i, j-89, nogo_cr[i, j])
		sheet_nogocr.write(i, 15, nogo_cr_pre[i])

	tr, ti = nogo_fa.shape
	for i in range(tr):
		for j in range(100, 125):
			sheet_nogofa.write(i, j-89, nogo_fa[i, j])
		sheet_nogofa.write(i, 15, nogo_fa_pre[i])

	os.remove('result_all_20.xls')
	newwb.save('result_all_20.xls')
