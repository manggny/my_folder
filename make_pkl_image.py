import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os,Image

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

if __name__ == '__main__':
    path = 'F:/zhaopian/objects'
    par_path = 'F:/zhaopian'
    filelist = os.listdir(path)
    result_path = 'F:/zhaopian'

    result_dict = {'data':[],'labels':[],'filenames':[]}

    for file in filelist:
        files = path + '/' + file
        img = mpimg.imread(files)
        #img = Image.open(files)
        img = rgb2gray(img)
        #plt.imshow(img, cmap='Greys_r')
        # plt.show()
        #print(img.shape)
        #print(img.shape)
        #out = img.resize((200,200),Image.ANTIALIAS)
        #out.show()
        #out.save(files)
        result_dict['data'].append(img)
        result_dict['labels'].append(100)
        result_dict['filenames'].append(file)
        print(files + " was done!")
    output = open(par_path + '/objects_pkl.pkl', 'wb')
    pkl.dump(result_dict, output)
    output.close()

