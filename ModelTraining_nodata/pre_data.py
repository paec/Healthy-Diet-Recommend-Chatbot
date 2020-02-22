import pickle
import numpy as np

file = open('Lecture_reduce/training_iobse_reduce.txt', 'r',encoding='utf-8')

word_set = set()
label_set = set()

word_to_index = dict()
index_to_word = dict()

label_to_index = dict()
index_to_label = dict()

total_token_list = []
total_label_list = []

tmp_token = []
tmp_label = []

word_to_index['PAD'] = 0
index_to_word[0] = 'PAD'
word_to_index['UNK'] = 1
index_to_word[1] = 'UNK'
word_to_index['CLS'] = 2
index_to_word[2] = 'CLS'
word_to_index['SEP'] = 3
index_to_word[3] = 'SEP'

label_to_index['PAD'] = 0
index_to_label[0] = 'PAD'



for data in file:
    
    if data.strip() == '': #代表一個句子的結束 ( "\r\n".strip() = '' )
        
        if len(tmp_token) == 0:
            continue

        total_token_list.append(tmp_token) #將 這個句子的所有詞的list    加入到total list
        total_label_list.append(tmp_label) #將 這個句子的所有標籤的list  加入到total list
        
        tmp_token = []
        tmp_label = []

        continue


    word_label = data.strip().split('\t')

    word = word_label[0]

    if word == '*':
        word = 'CLS'
    if word == '。':
        word = 'SEP'

    label = word_label[1]

    tmp_token.append(word)  #將這個句子的各個詞加入到list
    tmp_label.append(label) #將這個句子的各個字加入到list

    if word != 'CLS' and word != 'SEP':
        word_set.add(word)  #將這個句子的各個詞加入到set(為了計算整個corpus有多少詞)

    label_set.add(label)    #將這個句子的各個詞加入到set(為了計算整個corpus有多少標籤)


for word in word_set:
    word_to_index[word] = len(word_to_index) #為每個詞 assign一個 唯一的數字，建立字典
    index_to_word[len(index_to_word)] = word #建立反查字典


for label in label_set:
    label_to_index[label] = len(label_to_index) #為每個標籤 assign一個 唯一的數字，建立字典
    index_to_label[len(index_to_label)] = label #建立反查字典


word_set.add('CLS')
word_set.add('SEP')
word_set.add('UNK')
word_set.add('PAD')
label_set.add('PAD')

print(len(label_set))

training_x =[]
training_y = []

#把句子中的每個詞，轉成數字後，存到list中(這個list即為一個句子)，然後再把這個list存到total list。
for token_list in total_token_list:

    tmp_training_x = []

    for token in token_list:
        tmp_training_x.append(word_to_index[token])

    training_x.append(tmp_training_x)

#把句子中的每個標籤，轉成數字後，存到list中(這個list即為一個句子)，然後再把這個list存到total list。
for label_list in total_label_list:

    tmp_training_y = []

    for label in label_list:
        tmp_training_y.append(label_to_index[label])

    training_y.append(tmp_training_y)



def padding(input_seq_list, padded_value=-1, vec_len=768, padding_size=-1):

    if padded_value == -1:
        padded_value = np.zeros(vec_len)

    padded_input_seq = []

    if padding_size == -1:  #這裡算出最長的句子長度 => padding_size
        for seq in input_seq_list:
            if len(seq) > padding_size:
                padding_size = len(seq)  

    print(padding_size,"*************************")

    for input_seq in input_seq_list:

        tmp_vec = []

        for single_vec in input_seq:
            tmp_vec.append(single_vec)

        for i in range(len(input_seq), padding_size):
            tmp_vec.append(padded_value)
       
        padded_input_seq.append(tmp_vec)
    

    return np.asarray(padded_input_seq)


# print(training_x)
# print(training_y)
#讓訓練資料中每個句子長度一致(最長句子的長度)，不足的補0。
training_x = padding(training_x,padded_value = 0) 
print(training_x.shape)
training_y = padding(training_y,padded_value = 0)
print(training_y.shape)
# print(training_x)
# print(training_y)

# print(training_x)
# print(training_y)

for key in label_to_index.keys():
    print(key,label_to_index[key])


exit()
root = 'feature/'
data = 'data/'


pickle.dump(word_set,open(root+'word_set_reduce.pkl','wb'))
pickle.dump(label_set,open(root+'label_set_reduce.pkl','wb'))
pickle.dump(word_to_index,open(root+'word_to_index_reduce.pkl','wb'))
pickle.dump(index_to_word,open(root+'index_to_word_reduce.pkl','wb'))
pickle.dump(label_to_index,open(root+'label_to_index_reduce.pkl','wb'))
pickle.dump(index_to_label,open(root+'index_to_label_reduce.pkl','wb'))
pickle.dump(training_x,open(data+'training_x_reduce.pkl','wb'))
pickle.dump(training_y,open(data+'training_y_reduce.pkl','wb'))

for key in label_to_index.keys():
    print(key,label_to_index[key])