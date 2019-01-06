import sys, os

sys.path.append("C:/Users/manggny/PycharmProjects/Project-pre/func")
from xlutils.copy import copy
import xlwt, xlrd
import numpy as np
from go.funcs import make_list,diff
from go.funcs import div_by_laser,make_gonogolick,div_by_odor

path = "F:/gonogodata/nodelay/laser"
raw_file = '#3_gonogo20laser_d5_odor2_1.lvm'
filename = path + "/" + raw_file
name, _ = raw_file.split(".")
delay = 0
odor1, odor2, lick, pump, action, airpuff, laser = make_list(filename)

firstlick_row_odor_col_laser = np.zeros((5,3,2,2)) # 3 dims, first is number of oppo trials before trial onset, rows are odor.
# the last dim means trial number of specific contition
odor1_changed = diff(odor1)
odor2_changed = diff(odor2)
lick_changed = diff(lick)
laser_trial = 0
odor1_trial = 0
odor2_trial = 0
trials = 0
time = -1
maxtime = 0
trial_start =0
for k in range(len(odor1_changed)):
	if ((odor1_changed[k] == 1) and (odor1[k + 50] == 1)):
		trials += 1
		odor1_trial += 1
		if time > maxtime:
			maxtime = time
		time = 0
		#			go_trial_position.append(k)
	elif ((odor2_changed[k] == 1) and (odor2[k + 50] == 1)):
		trials += 1
		odor2_trial += 1
		if time > maxtime:
			maxtime = time
		time = 0
	if time is not -1:
		time += 1
maxtime = int(np.ceil((maxtime/100)))
odor1_licks = np.zeros((odor1_trial, maxtime*100))
odor2_licks = np.zeros((odor2_trial, maxtime*100))
now1_trial = -1
now2_trial = -1
now_trial = 0
i=0
time = -500
stop =0
odor = 0
now_posit = 0
pre_odor = 0
con_odor = 0
before_num = 0
now_odor = 0
changed = 0
while now_trial >= 0 and now_trial < trials:
	#print(sum(odor2))
	while i + time < len(odor1_changed):
	#	print(now_posit)
		if now_trial >= trials:
			break
		if time == -500:
			now_posit = i
		else:
			now_posit = i + time

		if (odor1_changed[now_posit] == 1 and trial_start == 0):
			if np.sum(laser[now_posit-200:now_posit+100]) > 10:
				laser_trial = 1
			else:
				laser_trial = 0
			pre_odor = now_odor
			now_odor = 1
			changed = 0
			trial_start = 1
			licked = 0
			i = now_posit
			stop = 1
			now_trial += 1
			now1_trial += 1
			if now1_trial > 0:
				for q in range(delay):
					odor1_licks[now1_trial-1][-q] = 0
			time = -delay
			first = 0
			odor = 1
			if pre_odor != now_odor:
				changed = 1
				con_odor += 1
				before_num = con_odor
				con_odor = 0
			elif pre_odor != 0 and (pre_odor == now_odor):
				changed = 0
				con_odor += 1
				before_num = 0
				print(con_odor)
			continue
		elif (odor2_changed[now_posit] == 1 and trial_start ==0):
			if np.sum(laser[now_posit-200:now_posit+100]) > 10:
				laser_trial = 1
			else:
				laser_trial = 0
			pre_odor = now_odor
			now_odor = 2
			changed = 0
			trial_start = 1
			licked = 0
			i = now_posit
			stop = 1
			now_trial += 1
			now2_trial += 1
			if now2_trial > 0:
				for q in range(delay):
					odor2_licks[now2_trial-1][-q] = 0
			time = -delay
			first = 0
			odor = 2
			if pre_odor != now_odor:
				changed = 1
				con_odor += 1
				before_num = con_odor
				con_odor = 0
			elif pre_odor != 0 and (pre_odor == now_odor):
				changed = 0
				con_odor += 1
				before_num = 0
				#print(con_odor)
			continue

		if (time < 1000) and (time > -500):
			if (time > 100) and (time < 1000) and (licked == 0) and(lick_changed[now_posit] == 1):
				licked = 1
				if changed == 1:
					if before_num < 5:
						firstlick_row_odor_col_laser[before_num,int(odor),int(laser_trial),0] += delay+time
						firstlick_row_odor_col_laser[before_num, int(odor), int(laser_trial), 1] += 1
						print(before_num)
					elif before_num >= 5:
						firstlick_row_odor_col_laser[4, int(odor), int(laser_trial),0] += delay + time
						firstlick_row_odor_col_laser[4, int(odor), int(laser_trial), 1] += 1
					con_odor = 0
					before_num = 0
				else:
					firstlick_row_odor_col_laser[0, int(odor), int(laser_trial),0] += delay + time
					firstlick_row_odor_col_laser[0, int(odor), int(laser_trial), 1] += 1
		#
		if time > -400:
			time += 1
		if (stop == 0):
			i += 1
		if (odor1_changed[now_posit] == -1) or (odor2_changed[now_posit] == -1) or (time>500):
			trial_start = 0

print(firstlick_row_odor_col_laser[:,:,:,0]/firstlick_row_odor_col_laser[:,:,:,1])
print(firstlick_row_odor_col_laser[:,:,:,1])
#print(trials)