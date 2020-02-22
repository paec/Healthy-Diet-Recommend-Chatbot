import pickle

root = "./"
word_set = pickle.load(open(root+'word_set.pkl','rb'))
word_to_index = pickle.load(open(root+'word_to_index.pkl','rb'))
index_to_word = pickle.load(open(root+'index_to_word.pkl','rb'))
label_set = pickle.load(open(root+'label_set.pkl','rb'))
label_to_index = pickle.load(open(root+'label_to_index.pkl','rb'))
index_to_label = pickle.load(open(root+'index_to_label.pkl','rb'))

print(len(word_set))
print(len(word_to_index))
print(len(index_to_word))
print(len(label_set))
print(len(label_to_index))
print(len(index_to_label))
print(label_to_index)
word_set = pickle.load(open(root+'word_set_reduce.pkl','rb'))
word_to_index = pickle.load(open(root+'word_to_index_reduce.pkl','rb'))
index_to_word = pickle.load(open(root+'index_to_word_reduce.pkl','rb'))
label_set = pickle.load(open(root+'label_set_reduce.pkl','rb'))
label_to_index = pickle.load(open(root+'label_to_index_reduce.pkl','rb'))
index_to_label = pickle.load(open(root+'index_to_label_reduce.pkl','rb'))

print(len(word_set))
print(len(word_to_index))

print(len(index_to_word))
print(len(label_set))
print(len(label_to_index))
print(len(index_to_label))
print(label_to_index)