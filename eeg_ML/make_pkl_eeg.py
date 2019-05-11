import csv,os
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

from ML_funcs import get_hzs_wave,mean_range    #(filename)

def z_score(whole,score):  #홀 은 전체 분포를 만들 데이터, 넘파이 like; score는 변환할 구체적 score들 넘파이 like
	whole_std = np.std(whole)
	whole_mean = np.mean(whole)
	z = np.zeros(np.alen(score))
	for i in range(np.alen(score)):
		#print(whole_std)
		z[i] = (score[i]-whole_mean)/whole_std
	return z



ONE_TRIAL_TIME = 600

path = 'F:/data_eeg/all_txts'

filename = path + '/1-1_Baseline CorrectionA.txt'

#all = ['Fp1','Fp2','F3','F4','C3','C4','P3','P4' O1 O2 F7 F8 T7 T8 P7 P8 Fz Cz Pz VEOG FC1 FC2 CP1 CP2 FC5 FC6 CP5 CP6 FT9 FT10 TP9 TP10 F1 F2 C1 C2 P1 P2 AF3 AF4 FC3 FC4 CP3 CP4 PO3 PO4 F5 F6 C5 C6 P5 P6 AF7 AF8 FT7 FT8 TP7 TP8 PO7 PO8 Fpz CPz POz Oz]

dummy = open(filename,'r')
for line in dummy:
	ALL=line.split()
	break
#
# print(ALL)
LA = ['F7', 'F5', 'F3', 'FT7', 'FC5', 'FC3']
LA_n =[]
MA = ['F1', 'Fz', 'F2', 'FC1', 'FC2']
MA_n = []
RA= ['F8', 'F6', 'F4','FT8', 'FC6', 'FC4']
RA_n = []
LP = ['P7', 'P5', 'P3', 'TP7', 'CP5', 'CP3']
LP_n = []
MP = ['P1', 'Pz', 'P2', 'CP1', 'CPz', 'CP2']
MP_n = []
RP = ['P8', 'P6', 'P4', 'TP8', 'CP6', 'CP4']
RP_n = []

all_n = []

for i in range(len(ALL)):
	if ALL[i] in LA:
		LA_n.append(i)
		all_n.append(i)
	elif ALL[i] in MA:
		MA_n.append(i)
		all_n.append(i)
		print(ALL[i])
	elif ALL[i] in RA:
		RA_n.append(i)
		all_n.append(i)
	elif ALL[i] in LP:
		LP_n.append(i)
		all_n.append(i)
	elif ALL[i] in MP:
		MP_n.append(i)
		all_n.append(i)
	elif ALL[i] in RP:
		RP_n.append(i)
		all_n.append(i)



# print(LA_n)
# print(MA_n)
# print(RA_n)
# print(LP_n)
# print(MP_n)
# print(RP_n)
# #
filelist = os.listdir(path)
# 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
# result_LA = {'data':[],'labels':[]}
# result_MA = {'data':[],'labels':[]}
# result_RA = {'data':[],'labels':[]}
# result_LP = {'data':[],'labels':[]}
# result_MP = {'data':[],'labels':[]}
# result_RP = {'data':[],'labels':[]}
result = {'data':[],'labels':[]}

# labels = R=0,I=1,A=2,B=3 , 1,2 BOTH ARE SUPPRESION

x1 = np.linspace(-2, 10, 600)

for file in filelist:
	filename = path + '/' + file
	name,s = file.split('.')
	if s != 'txt':
		continue
	label = name[-1]
	print('label',label)
	print(file)
	if label == 'A':
		print('label is A')
		label = 1  # labels = R=0,I=2,A=1,B=2 , A = suppression success
	elif label == 'R':
		print('label is R')
		label = 0
	elif label == 'I':
		print('label is I')
		label = 2
	elif label == 'B':
		print('label is B')
		label = 2
	a = np.loadtxt(filename,skiprows=1,dtype=float)
	# print(type(a))
	# print(a.shape)
	DAT, _ = a.shape
	trial_num = int(DAT / ONE_TRIAL_TIME)
	all_data = np.zeros((DAT,len(all_n),3))
	for col in range(len(all_n)):
		map = get_hzs_wave(a[:,all_n[col]])
		theta = map[0][1]
		print('theta : ', map[0][0])
		alpha = map[1][1]
		print('alpha : ', map[1][0])
		beta = map[2][1]
		print('beta : ', map[2][0])
		all_data[:,col,0] = theta
		all_data[:, col, 1] = alpha
		all_data[:, col, 2] = beta
		# print(all_data[:,col,0])
		# print('theta',theta)
		# print(DAT)
		# print(len(all_data[:, col, 0]))
		# print('theta', len(theta))
	print(len(all_data[1,:,1]))
	for i in range(trial_num):
		trial_data = np.zeros((35,24,3))
		idx_start = i*600
		idx_end = 600*(i+1)
		for j in range(len(all_n)):
			#print(idx_start,idx_end)
			dummy = all_data[idx_start:idx_end,j,0]
		#	print('dummy',len(dummy))
			dummy = z_score(dummy[:100], dummy)
			t_trial = mean_range(dummy)
			trial_data[j,:,0] = t_trial
			dummy = all_data[idx_start:idx_end, j, 1]
		#	print('dummy', len(dummy))
			dummy = z_score(dummy[:100], dummy)
			a_trial = mean_range(dummy)
			trial_data[j, :, 1] = a_trial
			dummy = all_data[idx_start:idx_end, j, 2]
		#	print('dummy', len(dummy),np.mean(dummy))
			dummy = z_score(dummy[:100], dummy)
		#	print(np.mean(dummy))
			b_trial = mean_range(dummy)
			trial_data[j, :, 2] = b_trial
		result['data'].append(trial_data)
		result['labels'].append(label)
	print(file + ' was done!')

print('all files were done!')
print('length:',len(result['data']),len(result['labels']))

output = open('F:/zhaopian/result_3d_pkl.pkl', 'wb')
pkl.dump(result, output)
output.close()
#
print('F:/zhaopian/result_3d_pkl.pkl was saved!')
#
print('finish!')
#
#
# #
# # print('F:/zhaopian/result_LA_pkl.pkl was saved!')
# #
# # output = open('F:/zhaopian/result_MA_pkl.pkl', 'wb')
# # pkl.dump(result_MA, output)
# # output.close()
# #
# # print('F:/zhaopian/result_MA_pkl.pkl was saved!')
# #
# # output = open('F:/zhaopian/result_RA_pkl.pkl', 'wb')
# # pkl.dump(result_RA, output)
# # output.close()
# #
# # print('F:/zhaopian/result_RA_pkl.pkl was saved!')
# #
# # output = open('F:/zhaopian/result_LP_pkl.pkl', 'wb')
# # pkl.dump(result_LP, output)
# # output.close()
#
# print('F:/zhaopian/result_LP_pkl.pkl was saved!')
#
# output = open('F:/zhaopian/result_MP_pkl.pkl', 'wb')
# pkl.dump(result_MP, output)
# output.close()
#
# print('F:/zhaopian/result_MP_pkl.pkl was saved!')
#
# output = open('F:/zhaopian/result_RP_pkl.pkl', 'wb')
# pkl.dump(result_RP, output)
# output.close()



# print(trial_data)
			# plt.title(name)# 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
			# plt.plot(x1, trial_data[:,0], 'r', label='LA')
			# plt.plot(x1, trial_data[:,1], 'b', label='MA')
			# plt.plot(x1, trial_data[:, 2], 'g', label='RA')
			# plt.plot(x1, trial_data[:, 3], 'p', label='LP')
			# plt.plot(x1, trial_data[:, 4], 'y', label='MP')
			# plt.plot(x1, trial_data[:, 5], 'o', label='RP')
			# plt.xlabel('Time(s)')
			# plt.ylabel('z-score')
			# plt.legend(loc='upper right')
			# plt.show()


#for k in LA_n:
				# 	trial_data[t,0] += a[j,k] # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 0] == 0:
				# 	print('LA zero!!')
				# else:
				# 	trial_data[t, 0] = trial_data[t,0]/len(LA_n)
				# for k in MA_n:
				# 	trial_data[t, 1] += a[j, k]  # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 1] == 0:
				# 	print('MA zero!!')
				# else:
				# 	trial_data[t, 1] = trial_data[t,1]/len(MA_n)
				# for k in RA_n:
				# 	trial_data[t, 2] += a[j, k]  # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 2] == 0:
				# 	print('RA zero!!')
				# else:
				# 	trial_data[t, 2] = trial_data[t,2]/len(RA_n)
				# for k in LP_n:
				# 	trial_data[t, 3] += a[j, k]  # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 3] == 0:
				# 	print('LP zero!!')
				# else:
				# 	trial_data[t,3] = trial_data[t,3]/len(LP_n)
				# for k in MP_n:
				# 	trial_data[t, 4] += a[j, k]  # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 4] == 0:
				# 	print('MP zero!!')
				# else:
				# 	trial_data[t, 4] = trial_data[t,4]/len(MP_n)
				# for k in RP_n:
				# 	trial_data[t, 5] += a[j, k]  # 0 = LA_n, 1=MA_n, 2=RA_n, 3=LP_n, 4=mp_N, 5=RP_n
				# if trial_data[t, 5] == 0:
				# 	print('RP zero!!')
				# else:
				# 	trial_data[t, 5] = trial_data[t,5]/len(RP_n)