import pickle
import numpy as np
import json

import tensorflow as tf
from keras.models import load_model
from keras_contrib.layers.crf import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from keras import backend as K
from extraLabel import extraDisLabel

K.tensorflow_backend._get_available_gpus()

modeldir = "./"

model= ""
graph= ""

root = 'feature/'

word_set = pickle.load(open(root+'word_set.pkl','rb'))
word_to_index = pickle.load(open(root+'word_to_index.pkl','rb'))
index_to_word = pickle.load(open(root+'index_to_word.pkl','rb'))
label_set = pickle.load(open(root+'label_set.pkl','rb'))
label_to_index = pickle.load(open(root+'label_to_index.pkl','rb'))
index_to_label = pickle.load(open(root+'index_to_label.pkl','rb'))



def loadmodel():
    global model
    custom_objects={'CRF': CRF,
                'crf_loss': crf_loss,
                'crf_viterbi_accuracy': crf_viterbi_accuracy} #
    model = load_model(modeldir+'withCRFweights.03-16.79.hdf5',custom_objects=custom_objects)
            # this is key : save the graph after loading the model
    global graph
    graph = tf.get_default_graph()



def text2index(text):
    x = list()
    # x.append(2)
    for word in text:
        if word =="。" or word==".":
            x.append(3)
        elif not word in word_to_index:
            # x.append(1)
            pass
        else:
            x.append(word_to_index[word])      
    x.extend([0]*(96-len(x)))
    x = np.expand_dims(np.array(x),0)

    return x

loadmodel()


   
def predict(text):

    global graph

    # text = "我覺得肚子痛"
    x = text2index(text)
    result =""
    with graph.as_default():
        result = model.predict(x)[0]
    
    wordlist = list()
    labellist = list()

    for index,res in enumerate(result): # index => timesteps , res => 39 label
        
        if index_to_word[x[0][index]] == 'PAD':
            break
        elif index_to_word[x[0][index]] == 'CLS':
            wordlist.append(".")
            labellist.append("O")
        elif index_to_word[x[0][index]] == 'SEP':
            wordlist.append(",")
            labellist.append("O")
        else:
            wordlist.append(index_to_word[x[0][index]])
            labellist.append(index_to_label[np.argmax(res)])
    
    jsonresult = {"wordlist":wordlist,"labellist":labellist}

    jsonresult = json.dumps(jsonresult,ensure_ascii=False)
    # print(jsonresult)
    return jsonresult


if __name__ == '__main__':
    result = predict("我剛才肚子痛")
    print(result)

    while True:
        try:
            text = input()
            result = predict(text)
            print("model_all")
            result = json.loads(result)
            print(result)
            
            for i in range(len(result['wordlist'])):
                print(result['wordlist'][i]," ",result['labellist'][i])
            dislist = extraDisLabel(result)
            print(dislist)
        except:
            pass