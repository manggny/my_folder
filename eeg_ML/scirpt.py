from sklearn import preprocessing
import tensorflow as tf
import keras,os
#from tensorflow.keras.models import Sequantial
from keras.models import Sequential
from keras.layers import Dense,Dropout,LSTM,CuDNNLSTM,BatchNormalization
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

## private

from ML_funcs import unpickle,create_model


MODEL_DIR = "./pilot_study_3D_100_1"  #FIXME
MKDIR = "mkdir -p " + MODEL_DIR
os.system(MKDIR)

BATCH_SIZE = 128

EPOCHS = 50

def create_models(input_shape): #tuple for input_shape
	model = Sequential()
	model.add(LSTM(128,input_shape=input_shape,return_sequences=True))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
	model.add(Dropout(0.1))
	model.add(BatchNormalization())

	model.add(LSTM(128, input_shape=input_shape))
	model.add(Dropout(0.2))
	model.add(BatchNormalization())

	model.add(Dense(32, activation='relu'))
	model.add(Dropout(0.2))

	model.add(Dense(4, activation='softmax'))
	opt = keras.optimizers.Adam(lr = 0.001,decay=1e-6)
	model.compile(Loss='sparse_categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

	checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR, 'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),
								 save_best_only=True)

	history = model.fit(train_x,train_y,batch_size=BATCH_SIZE,epochs=EPOCHS,validation_data=(val_x,val_y),callbacks=[checkpoint])

	return model


