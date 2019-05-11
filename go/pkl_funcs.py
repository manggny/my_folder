import numpy as np
import pickle as pkl
import sys, os
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")

from go.funcs import make_list,diff
from go.funcs import div_by_laser,make_gonogolick,div_by_odor

def make_lvm_to_pkl(lvm_filepath):
	resultpath = 'F:/ACC-Camk2/0109~gonogo/gonogopkl'

	a = lvm_filepath.split('/')
	filename = a[-1]
	#print(filename)
	name,*_ = filename.split('.')
	result_filename = name+'.pkl'
	files = os.listdir(resultpath)
	if result_filename in files:
		print(result_filename+" is already exist! skip~")
		return resultpath+'/'+name+'.pkl'

	#print(name)
	odor1, odor2, lick, pump, action, airpuff, laser = make_list(lvm_filepath)
	print(sum(laser))
	dlaser = np.array(diff(laser))
	print(sum(np.abs(dlaser)))
	odor1_lick, odor2_lick = make_gonogolick(odor1, odor2, lick,delay=200)
	#print(np.sum(odor1_lick))

	odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
	odor1, odor2, action, airpuff, pump, laser,delay=200)
	# lasers = 0
	# for i in range(np.alen(odor1_laser[:,1])):
	# 	if np.sum(odor1_laser[i,0:200]) > 10:
	# 		lasers += 1
	# for i in range(np.alen(odor2_laser[:,1])):
	# 	if np.sum(odor2_laser[i,0:200]) > 10:
	# 		lasers += 1
	print(np.sum(odor1_laser))
	print(np.sum(odor2_laser))
	# print(np.sum(np.abs(np.diff(odor1_laser))))
	# print(np.sum(np.abs(np.diff(odor2_laser))))
	tr, ti = np.shape(odor1_lick)
	#print(tr, ti)

	odor1_lick = np.delete(odor1_lick,[0,1,2,3,4,5,6,7],0)
	odor2_lick = np.delete(odor2_lick, [0, 1], 0)
	odor1_action= np.delete(odor1_action, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_airpuff = np.delete(odor1_airpuff, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_pump = np.delete(odor1_pump, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_laser = np.delete(odor1_laser, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor2_action = np.delete(odor2_action, [0, 1], 0)
	odor2_airpuff = np.delete(odor2_airpuff, [0, 1], 0)
	odor2_pump = np.delete(odor2_pump, [0, 1], 0)
	odor2_laser = np.delete(odor2_laser, [0, 1], 0)


	result_dict = {'odor1_lick':odor1_lick, 'odor2_lick':odor2_lick,'odor1_action':odor1_action, 'odor1_airpuff':odor1_airpuff, 'odor1_pump':odor1_pump, 'odor1_laser':odor1_laser, 'odor2_action':odor2_action, 'odor2_airpuff':odor2_airpuff, 'odor2_pump':odor2_pump, 'odor2_laser':odor2_laser}
	result_filename = resultpath+'/'+name+'.pkl'
	output = open(result_filename, 'wb')
	pkl.dump(result_dict, output)
	#print(result_dict.items())
	output.close()
	return result_filename

def connecting_to_pkl(pkl_name,lvm_filepath):
	cue_pkl_file = open(pkl_name, 'rb')
	ori = pkl.load(cue_pkl_file)


	odor1, odor2, lick, pump, action, airpuff, laser = make_list(lvm_filepath)
	print(sum(laser))
	dlaser = np.array(diff(laser))
	print(sum(np.abs(dlaser)))
	odor1_lick, odor2_lick = make_gonogolick(odor1, odor2, lick,delay = 200)
	odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
		odor1, odor2, action, airpuff, pump, laser,delay=200)
	lasers = 0
	for i in range(np.alen(odor1_laser[:,1])):
		if np.sum(odor1_laser[i,0:200]) > 10:
			lasers += 1
	for i in range(np.alen(odor2_laser[:,1])):
		if np.sum(odor2_laser[i,200]) > 10:
			lasers += 1
	print(lasers)
	print(np.sum(odor1_laser))
	print(np.sum(odor2_laser))
	odor1_lick = np.delete(odor1_lick, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor2_lick = np.delete(odor2_lick, [0, 1], 0)
	odor1_action = np.delete(odor1_action, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_airpuff = np.delete(odor1_airpuff, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_pump = np.delete(odor1_pump, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor1_laser = np.delete(odor1_laser, [0, 1, 2, 3, 4, 5, 6, 7], 0)
	odor2_action = np.delete(odor2_action, [0, 1], 0)
	odor2_airpuff = np.delete(odor2_airpuff, [0, 1], 0)
	odor2_pump = np.delete(odor2_pump, [0, 1], 0)
	odor2_laser = np.delete(odor2_laser, [0, 1], 0)

	print("1")
	ori['odor1_lick'] = np.vstack((ori['odor1_lick'],odor1_lick))
	ori['odor2_lick'] = np.vstack((ori['odor2_lick'], odor2_lick))
	ori['odor1_action'] = np.vstack((ori['odor1_action'], odor1_action))
	ori['odor1_airpuff'] = np.vstack((ori['odor1_airpuff'], odor1_airpuff))
	ori['odor1_pump'] = np.vstack((ori['odor1_pump'], odor1_pump))
	ori['odor1_laser'] = np.vstack((ori['odor1_laser'], odor1_laser))
	ori['odor2_action'] = np.vstack((ori['odor2_action'], odor2_action))
	ori['odor2_airpuff'] = np.vstack((ori['odor2_airpuff'], odor2_airpuff))
	ori['odor2_pump'] = np.vstack((ori['odor2_pump'], odor2_pump))
	ori['odor2_laser'] = np.vstack((ori['odor2_laser'], odor2_laser))


	tr,ti = np.shape(ori['odor1_lick'])
	ntr, nti = np.shape(ori['odor2_lick'])

	out_file = open(pkl_name, 'wb')
	pkl.dump(ori, out_file)
	out_file.close()
	cue_pkl_file.close()
	print("3")
	print(lvm_filepath + " has been added ! now whole odor1 trial number is "+ str(tr) + '. odor2 tn is '+ str(ntr))
	return pkl_name


if __name__=="__main__":
	path = 'F:/ACC-Camk2/0109~gonogo/gonogo test with laser'
	pkl_path = 'F:/ACC-Camk2/0109~gonogo/gonogopkl'
	filename1 = path + '/#f3_chr_gonogolaser_0110_odor1_6.lvm'
	filename2 = path + '/#f3_chr_gonogolaser_0111_odor1_4.lvm'
	filename3 = path + '/#f3_chr_gonogolaser_0112_odor1_3.lvm'
	filename4 = path + '/#f3_chr_gonogolaser_0113_odor1_3.lvm'
	#filename5 = path + '/#4_gta_gonogolaser_0121_odor1_2.lvm'

	pkl_file = make_lvm_to_pkl(filename1)

	connecting_to_pkl(pkl_file,filename2)
	connecting_to_pkl(pkl_file, filename3)
	connecting_to_pkl(pkl_file, filename4)
	#connecting_to_pkl(pkl_file, filename5)