from xlutils.copy import copy
import xlwt, xlrd,os
import numpy as np
import pickle as pkl
import sklearn.preprocessing

def unpickle(infile):
	import pickle
	with open(infile, 'rb') as fo:
		# pickle.dump(pickle.load(fo), infile, protocol=2)
		data = pickle.load(fo)
	fo.close()
	return data

if __name__=="__main__":
	pkls_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/all_ai_new_20%/'
	result_path = 'F:/Insula-Gcamp6/record/record_split_by_behav/'
	result_file_cr = '20%_nogo_cr_trials.pkl'
	result_file_fa = '20%_nogo_fa_trials.pkl'
	result_file_hit = '20%_nogo_hit_trials.pkl'
	result_file_miss = '20%_nogo_miss_trials.pkl'
	filelist = os.listdir(pkls_path)
	k = 0
	all_odor2_hit = np.array([])
	all_odor2_cr = np.array([])
	all_odor1_miss = np.array([])
	all_odor1_hit = np.array([])

	for file in filelist:
		name,s = file.split('.')
		if s != 'pkl':
			continue
		print(file)
		data = unpickle(pkls_path + file)
		odor1_miss = data['odor1'][1]
		odor1_noact = data['odor1'][2]
		if np.alen(all_odor2_hit) == 0:
			all_odor2_hit = data['odor2'][0]
		else:
			all_odor2_hit = np.vstack((all_odor2_hit,data['odor2'][0]))

		if np.alen(all_odor1_hit) == 0:
			all_odor1_hit = data['odor1'][0]
		else:
			all_odor1_hit = np.vstack((all_odor1_hit,data['odor1'][0]))

		odor2_miss = data['odor2'][1]
		odor2_noact = data['odor2'][2]
		tr2, *_ = odor2_noact.shape
		tr3, *_ = odor2_miss.shape
		print(tr2, tr3)
		if tr2 == 0 and tr3 > 0:
			odor2_cr = odor2_miss
		elif tr3 == 0 and tr2 > 0:
			odor2_cr = odor2_noact
		elif tr3 > 0 and tr2 > 0:
			odor2_cr = np.vstack((odor2_miss, odor2_noact))

		if np.alen(all_odor2_cr) == 0:
			all_odor2_cr = odor2_cr
		else:
			all_odor2_cr = np.vstack((all_odor2_cr,odor2_cr))


		tr2,*_= odor1_noact.shape
		tr3,*_ = odor1_miss.shape
		#print(ti2,ti3)
		if np.ndim(odor1_noact)>1 and np.ndim(odor1_miss) > 1:
			tr2, ti2 = odor1_noact.shape
			tr3, ti3 = odor1_miss.shape
			if tr2 == 0 or ti2 == 0:
				odor1_m = odor1_miss
			elif tr3 ==0 or ti3 == 0:
				odor1_m = odor1_noact
			else:
				odor1_m = np.vstack((odor1_miss, odor1_noact))

		if np.alen(all_odor1_miss) == 0:
			all_odor1_miss = odor1_m
		else:
			all_odor1_miss = np.vstack((all_odor1_miss,odor1_m))

		print(all_odor2_hit.shape, np.ndim(all_odor2_hit),np.alen(all_odor2_hit))
		print(all_odor2_cr.shape, np.ndim(all_odor2_cr), np.alen(all_odor2_cr))
	print(all_odor2_hit.shape,np.ndim(all_odor2_hit))
	output = open(result_path+result_file_fa, 'wb')
	pkl.dump(all_odor2_hit, output)
	output.close()

	output = open(result_path + result_file_cr, 'wb')
	pkl.dump(all_odor2_cr, output)
	output.close()

	output = open(result_path + result_file_hit, 'wb')
	pkl.dump(all_odor1_hit, output)
	output.close()

	output = open(result_path + result_file_miss, 'wb')
	pkl.dump(all_odor1_miss, output)
	output.close()

