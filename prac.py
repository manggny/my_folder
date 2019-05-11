import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os,Image

path = 'F:/zhaopian/objects'
par_path = 'F:/zhaopian/all'

filelist = os.listdir(path)

for files in filelist:
	files = path + '/'+files
	img = Image.open(files)
	out = img.resize((50,50),Image.ANTIALIAS)
	out.save(files)
	print(files + ' was done!')


#out.save(files)


# file = par_path + '/faces_pkl.pkl'
# pkl_file = open(file, 'rb')
# faces = pkl.load(pkl_file)
# print(type(faces['data'][1]))
# print(faces['data'][1].shape)
# print(np.alen(faces['labels'][1]))
# print(np.alen(faces['filenames'][1]))
# print(np.alen(faces['data']))
# print(np.max(faces['labels']))
# print(np.alen(faces['filenames']))
