import pickle
from keras.models import load_model
import numpy as np
from keras_contrib.layers.crf import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras import backend as K
K.tensorflow_backend._get_available_gpus()

# file = open("./BILSTM-CRF_eval/_test6.txt","w",encoding="utf8")

custom_objects={'CRF': CRF,
                'crf_loss': crf_loss,
                'crf_viterbi_accuracy': crf_viterbi_accuracy}
root = 'feature/'
data_root = 'data/'
testing_x = pickle.load(open(data_root+'test_x_n_half.pkl','rb'))
testing_y = pickle.load(open(data_root+'test_y_n_half.pkl','rb'))
word_set = pickle.load(open(root+'word_set.pkl','rb'))
word_to_index = pickle.load(open(root+'word_to_index.pkl','rb'))
index_to_word = pickle.load(open(root+'index_to_word.pkl','rb'))
label_set = pickle.load(open(root+'label_set.pkl','rb'))
label_to_index = pickle.load(open(root+'label_to_index.pkl','rb'))
index_to_label = pickle.load(open(root+'index_to_label.pkl','rb'))
modeldir = "embedding = 300 , lstm = 300/"
model= load_model(modeldir+'withCRFweights.03-16.79.hdf5',custom_objects=custom_objects)

for num in range(len(testing_x)):

    if num%100==0:
        print(num)

    result = model.predict(np.array([testing_x[num]])) #(1,96,39) batch:1 ,timesteps:96 , label#:39
    # print(np.shape([testing_x[num]]))
    # print(np.shape(result))

    result = result[0] #(96,39)


    for index,res in enumerate(result): # index => timesteps , res => 39 label
        
        print(index_to_word[testing_x[num][index]],index_to_label[testing_y[num][index]],index_to_label[np.argmax(res)])
        
        # file.write(index_to_word[testing_x[num][index]]+" "+index_to_label[testing_y[num][index]]+" "+index_to_label[np.argmax(res)]+"\n")
        # if index_to_word[testing_x[num][index]] == "SEP":
        #     file.write("\n")
        #     break


