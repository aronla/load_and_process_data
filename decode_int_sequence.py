import pickle
import os 
dir = 'results/sentences/'


with open('results/word_index_most_common_50000_tokens.pickle', 'rb') as f:
    word_index_dict = pickle.load(f)


index2word = word_index_dict['index2word']


files_in_dir = os.listdir(dir)

file_name = files_in_dir[1]
with open(dir + file_name, 'rb') as f:
    list_of_sentences, text_sentences = pickle.load(f)

sentences = list()
for sentence in list_of_sentences:
    sentences.append([index2word[k] for k in sentence])


zipped = list(zip(sentences, text_sentences))

