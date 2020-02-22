import pickle
import keras
from keras.models import load_model
import numpy as np
import json
from keras_contrib.layers.crf import CRF
from keras_contrib.utils import save_load_utils
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras import backend as K
K.tensorflow_backend._get_available_gpus()
def turn_one_hot(total_list,size):

    one_hot_list = []

    for list in total_list:

        tmp_list = []

        for index in list:

            single_vec = np.zeros(size)
            single_vec[index] = 1
            tmp_list.append(single_vec)

        one_hot_list.append(tmp_list)

    return np.asarray(one_hot_list)


root = 'feature/'
data_root = 'data/'
training_x = pickle.load(open(data_root+'testing_x_reduce.pkl','rb'))
training_y = pickle.load(open(data_root+'testing_y_reduce.pkl.pkl','rb'))
testing_x = pickle.load(open(data_root+'training_x_reduce.pkl','rb'))
testing_y = pickle.load(open(data_root+'training_y_reduce.pkl','rb'))
word_set = pickle.load(open(root+'word_set_reduce.pkl','rb'))
word_to_index = pickle.load(open(root+'word_to_index_reduce.pkl','rb'))
index_to_word = pickle.load(open(root+'index_to_word_reduce.pkl','rb'))
label_set = pickle.load(open(root+'label_set_reduce.pkl','rb'))
label_to_index = pickle.load(open(root+'label_to_index_reduce.pkl','rb'))
index_to_label = pickle.load(open(root+'index_to_label_reduce.pkl','rb'))

training_x = training_x
training_y = training_y

#print(training_x)
#print(training_y)

X_test = testing_x[0:1]
Y_test = testing_y[0:1]
#print(len(label_set))
Y_test = turn_one_hot(Y_test,len(label_set))

#print(X_test)
#print(Y_test)

# exit()

from keras import backend as K

keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)

print(K.tensorflow_backend._get_available_gpus())

model = keras.Sequential()
model.add(keras.layers.Embedding(len(word_set),500,mask_zero=True)) #300
model.add(keras.layers.Bidirectional(keras.layers.LSTM(300,return_sequences=True))) #300
#model.add(keras.layers.LSTM(300,return_sequences=True))
# model.add(keras.layers.Activation('relu'))
# model.add(keras.layers.Dropout(0.5))
# model.add(keras.layers.TimeDistributed(keras.layers.Dense(len(label_set))))
model.add(keras.layers.Dense(len(label_set)))

CRF = CRF(len(label_set))
model.add(CRF)

# model.add(keras.layers.Activation('softmax')) #sigmoid


binary_loss = 'binary_crossentropy'
categorical_loss = 'categorical_crossentropy'
model.compile(optimizer='adam', loss=CRF.loss_function , metrics=[CRF.accuracy]) #categorical_loss #CRF.accuracy

#print(training_x.shape)

training_y = turn_one_hot(training_y,len(label_set))
#print(training_y.shape)

print(model.summary())
# exit()
# model= load_model('model/bilstm_ner.h5')

model.fit(training_x, training_y,epochs=3,val_split=0.25)#validation_data=(X_test, Y_test)
# model.save('model/bilstm_ner.h5')



result = model.predict(np.array([testing_x[23]])) # return (1,96,39) batch:1 ,timesteps:96 , label#:39

result = result[0] #(96,39)

for index,res in enumerate(result): # index => timesteps , res => 
 
    print(index_to_word[testing_x[23][index]],index_to_label[testing_y[23][index]],index_to_label[np.argmax(res)])
