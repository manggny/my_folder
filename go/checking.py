import numpy as np
import pickle as pkl
import sys, os
sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")

from go.funcs import make_list,diff
from go.funcs import div_by_laser,make_gonogolick,div_by_odor

lvm_filepath = 'F:/ACC-Camk2/0109~gonogo/gonogo test with laser/#2_gta_gonogolaser_0118_odor1_2.lvm'
resultpath = 'F:/ACC-Camk2/0109~gonogo/gonogopkl'



#print(name)
odor1, odor2, lick, pump, action, airpuff, laser = make_list(lvm_filepath)
print(sum(laser))
dlaser = np.array(diff(laser))
dodor1 = np.array(diff(odor1))
print(sum(np.abs(dlaser)))
odor1_lick, odor2_lick = make_gonogolick(odor1, odor2, lick,delay=200)
#print(np.sum(odor1_lick))

numpy_ordor = []
odor1_action, odor1_airpuff, odor1_pump, odor1_laser, odor2_action, odor2_airpuff, odor2_pump, odor2_laser = div_by_odor(
odor1, odor2, action, airpuff, pump, laser,delay=200)
for i in range(np.alen(odor1_laser[:,1])):
	if np.sum(odor1_laser[i,0:200]) > 10:
		numpy_ordor.append(1)
	else:
		numpy_ordor.append(0)

print(numpy_ordor)

list_odor = []
for i in range(np.alen(dodor1)):
	if dodor1[i] == 1 and (sum(laser[i-200:i])>10):
		list_odor.append(1)
	elif dodor1[i] == 1 and (sum(laser[i-200:i])<10):
		list_odor.append(0)

print(list_odor)

