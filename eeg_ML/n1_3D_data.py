#public
import sys, os
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

#private
from ReadIn_3D import unpickle
from Create_model_3D import createModel

#Settings 
batch_size = 256
epochs = 50
num_Classes = 10
MODEL_DIR = "./pilot_study_3D_100_1"  #FIXME
MKDIR = "mkdir -p " + MODEL_DIR
os.system(MKDIR)
checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),save_best_only=True)

all_data = unpickle("../make_pkl/fa+ob_pkl_100_3d.pkl")
train_data, test_data, train_labels_one_hot, test_labels_one_hot = train_test_split(all_data['data'], all_data['labels'])
#for i in range(len(test_data)):
#    print(test_data[i].shape)

#print(len(train_data));  print(type(train_data));
#print((train_data[0]).shape);  print(type(train_data[0]))
train_data = np.array(train_data)
test_data = np.array(test_data)
train_data = np.reshape(train_data, (train_data.shape[0],100,100,3))
test_data = np.reshape(test_data, (test_data.shape[0],100,100,3))

#print(train_labels_one_hot)
#print(type(train_labels_one_hot))
train_labels_one_hot = keras.utils.to_categorical(train_labels_one_hot, num_Classes)
test_labels_one_hot = keras.utils.to_categorical(test_labels_one_hot, num_Classes)
train_data = train_data.astype('float32')
test_data = test_data.astype('float32')
train_data /= 255
test_data /= 255

'''
datagen = \
    ImageDataGenerator(
    rotation_range=10.,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.,
    zoom_range=.1,
    horizontal_flip=True,
    vertical_flip=True)
datagen.fit(train_data)
'''
datagen = ImageDataGenerator(
#         zoom_range=0.2, # randomly zoom into images
#         rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=True)  # randomly flip images

print(train_data.shape, len(train_labels_one_hot));   
 
'''
#Checking
print NHuman_dict.keys();print NHuman_dict['data'][0];print len(NHuman_dict['data']);
print NHuman_dict['data'].shape;print len(NHuman_dict['data'][0]);
'''

#Model definition
CNN_Model = createModel((100,100,3), num_Classes)

# Training 
CNN_Model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])  
#history = CNN_Model.fit(train_data, train_labels_one_hot, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(test_data, test_labels_one_hot), callbacks=[checkpoint]) // without datagen
#history = CNN_Model.fit_generator(datagen.flow(train_data, train_labels_one_hot, batch_size=batch_size), epochs=epochs, validation_data=(test_data, test_labels_one_hot), callbacks=[checkpoint], workers=4)
history = CNN_Model.fit_generator(datagen.flow(train_data, train_labels_one_hot, batch_size=batch_size), steps_per_epoch=int(np.ceil(train_data.shape[0] / float(batch_size))), epochs=epochs, validation_data=(test_data, test_labels_one_hot),callbacks=[checkpoint], workers=4)

CNN_Model.evaluate(test_data, test_labels_one_hot)

# Loss Curves
plt.figure(figsize=[8,6])
plt.plot(history.history['loss'],'r',linewidth=3.0)
plt.plot(history.history['val_loss'],'b',linewidth=3.0)
plt.legend(['Training loss', 'Validation Loss'],fontsize=18, loc = 'best')
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Loss',fontsize=16)
plt.title('Loss Curves',fontsize=16)
plt.savefig(MODEL_DIR+"/Loss_curve.png")
  
# Accuracy Curves
plt.figure(figsize=[8,6])
plt.plot(history.history['acc'],'r',linewidth=3.0)
plt.plot(history.history['val_acc'],'b',linewidth=3.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18, loc = 'best')
plt.xlabel('Epochs ',fontsize=16)
plt.ylabel('Accuracy',fontsize=16)
plt.title('Accuracy Curves',fontsize=16)
plt.savefig(MODEL_DIR+"/Acc_curve.png")

