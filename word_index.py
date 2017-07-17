import nltk
from collections import Counter
import pickle
import time
UNK = '<unk>'
START = '<start>'
END = '<end>'

from read_text_file import ReadTextFile
from text_utils import TextUtils

class WordIndex:

    def __init__(self):
        self.read_text_file = ReadTextFile('/Users/aron/data/deepdata_large.txt')

    def _create_token_counter(self):
        self.total_counter = Counter()
        k = 0
        for chunk in self.read_text_file.read_in_chunks(100000000, number_of_chunks_to_read = None):
            time_start = time.time()
            tokens = self._process_chunk_to_tokens(chunk)
            present_counter = Counter(tokens)

            time_end = time.time()
            print('time for tokenization ' + str(time_end - time_start) + ' seconds.')
            time_start = time.time()

            self.total_counter = self.total_counter + present_counter

            time_end = time.time()
            print('time for counter addition ' + str(time_end - time_start) + ' seconds.')

            k += 1
            if k % 10 == 0:
                print('On chunk number ' + str(k) )

    def _process_chunk_to_tokens(self, chunk):
            chunk = TextUtils.lower_case(chunk)
            chunk = TextUtils.filter_line(chunk)
            tokens = TextUtils.tokenize(chunk)
            tokens = TextUtils.remove_single_letter_tokens(tokens)
            tokens = TextUtils.convert_to_numeric_token(tokens)
            return tokens

    def get_word_index(self, counter):
        index2word = ['_'] + [UNK] + [START] + [END] + [ x for x in counter]
        word2index = dict([(w,i) for i,w in enumerate(index2word)] )
        return index2word, word2index #, freq_dist

    def create_and_save_word_index(self, file_name):
        self._create_token_counter()
        self.save_word_index(self.total_counter)

    def save_word_index_from_counter(self, file_name, counter):
        index2word, word2index = self.get_word_index(counter) 
        data = {'index2word': index2word, 'word2index': word2index, 'counter': counter}
        with open('results/' + file_name, 'wb') as f:
            pickle.dump(data, f)

if __name__ == '__main__':
    word_index = WordIndex()
    # word_index.save_word_index('wordindex.pickle')
    most_common_counter = pickle.load(open('results/most_common_50000_tokens_counter.pickle', 'rb'))
    word_index.save_word_index_from_counter('word_index_most_common_50000_tokens.pickle', most_common_counter)
