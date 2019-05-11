# it is a function make tdms files to pkl type.

from nptdms import TdmsFile
import binascii
from datetime import datetime
from io import BytesIO
import logging
import os,sys
import numpy as np
import pickle as pkl

path = 'F:/Insula-Gcamp6/record/gonogo day1'
par_path = 'F:/Insula-Gcamp6/record'
r_path = 'F:/Insula-Gcamp6/record/result_pkl'
filelist = os.listdir(path)
result_list = os.listdir(r_path)
for f in filelist:
	filepath = path+'/'+f
	filename = f.split('.')
	filename = filename[0]
	w_filename = filename+'.pkl'
	if w_filename in result_list:
		print(w_filename + ' is already exist! skip..')
		continue
	file = TdmsFile(filepath)
	output = open(par_path+'/result_pkl/'+filename+'.pkl', 'wb')
	pkl.dump(file, output)
	output.close()

#pkl_file = open('weights.pkl', 'rb')
#weights = pkl.load(pkl_file)
