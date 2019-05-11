import keras,os
#from tensorflow.keras.models import Sequantial
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.environ["TF_CPP_MIN_LOG_LEVEL"]='2'

## PRI
from ML_funcs import unpickle,create_model

## setting enviroment and data
MODEL_DIR = "F:/data_eeg/result_model_LA"
dic_file = 'F:/data_eeg/all_pkl/result_LA_pkl.pkl'
BATCH_SIZE = 128
EPOCHS = 20
num_Classes = 4

checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR,'M_{epoch:03d}_l_{loss:.3f}_vl_{val_loss:.3f}.hdf5'),save_best_only=True)
all_data = unpickle(dic_file)

train_data, test_data, train_labels_one_hot, test_labels_one_hot = train_test_split(all_data['data'], all_data['labels'])
#print('before',train_labels_one_hot.shape, test_labels_one_hot.shape)
train_data = np.array(train_data)
test_data = np.array(test_data)
print(train_data.shape,test_data.shape)
train_data = np.reshape(train_data, (train_data.shape[0],600,1))
test_data = np.reshape(test_data, (test_data.shape[0],600,1)) # do it if need to change data struct
print(train_data.shape,test_data.shape)

# train_labels_one_hot = keras.utils.to_categorical(train_labels_one_hot, num_Classes)
# test_labels_one_hot = keras.utils.to_categorical(test_labels_one_hot, num_Classes)
train_data = train_data.astype('float32')
test_data = test_data.astype('float32')
print(train_data.shape, len(train_labels_one_hot))
#print(train_labels_one_hot.shape, test_labels_one_hot.shape)

print(train_data.shape[1:])
print(train_data[1,:].shape)
EEG_RNN = create_model(train_data.shape[1:], num_Classes)
opt = keras.optimizers.Adam(lr = 0.001,decay=1e-6)
EEG_RNN.compile(loss='sparse_categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

history = EEG_RNN.fit(train_data,train_labels_one_hot,batch_size=BATCH_SIZE,epochs=EPOCHS,validation_data=(test_data,test_labels_one_hot),callbacks=[checkpoint])
EEG_RNN.evaluate(test_data, test_labels_one_hot)

# Loss Curves
plt.figure(figsize=[8, 6])
plt.plot(history.history['loss'], 'r', linewidth=3.0)
plt.plot(history.history['val_loss'], 'b', linewidth=3.0)
plt.legend(['Training loss', 'Validation Loss'], fontsize=18, loc='best')
plt.xlabel('Epochs ', fontsize=16)
plt.ylabel('Loss', fontsize=16)
plt.title('Loss Curves', fontsize=16)
plt.savefig(MODEL_DIR + "/Loss_curve.png")

# Accuracy Curves
plt.figure(figsize=[8, 6])
plt.plot(history.history['acc'], 'r', linewidth=3.0)
plt.plot(history.history['val_acc'], 'b', linewidth=3.0)
plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize=18, loc='best')
plt.xlabel('Epochs ', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.title('Accuracy Curves', fontsize=16)
plt.savefig(MODEL_DIR + "/Acc_curve.png")









