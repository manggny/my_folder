# it is a function make tdms files to pkl type.

from nptdms import TdmsFile
import binascii
from datetime import datetime
from io import BytesIO
import logging
import os,sys
import numpy as np
import pickle as pkl

path = 'F:/ACC-Camk2/GCAMP6/RECORD'
par_path = 'F:/ACC-Camk2/GCAMP6'
filelist = os.listdir(path)
for f in filelist:
	filepath = path+'/'+f
	filename = f.split('.')
	filename = filename[0]
	file = TdmsFile(filepath)
	output = open(par_path+'/record_pkls/'+filename+'.pkl', 'wb')
	pkl.dump(file, output)
	output.close()

#pkl_file = open('weights.pkl', 'rb')
#weights = pkl.load(pkl_file)
