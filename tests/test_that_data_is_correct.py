import unittest
import pickle
import os
import numpy as np

current_dir = os.path.dirname(os.path.realpath(__file__))

class TestThatDataIsCorrect(unittest.TestCase):

    def test_the_data(self):
        self._given_data()
        self._when_decoding_the_sentences()
        self._then_the_decoded_sentence_matches_the_real()

    def _given_data(self):
        ### load file randomly
        files = os.listdir(current_dir + '/../results/sentences/')
        which_file = np.random.randint(0, len(files), size=1)[0]
        file_name = files[which_file]

        with open(current_dir + '/../results/sentences/' + file_name, 'rb') as f:
             self.int_sentence_list, self.word_sentence_list = pickle.load(f)

        with open(current_dir + '/../results/word_index_most_common_50000_tokens.pickle', 'rb') as f:
            self.word_index_dict = pickle.load(f)

    def _when_decoding_the_sentences(self):
        self.index2word = self.word_index_dict['index2word']
        decoded_sentences = list()

        for sentence in self.int_sentence_list:
            decoded_sentences.append([self.index2word[k] for k in sentence])

        self.zipped = list(zip(decoded_sentences, self.word_sentence_list))

    def _then_the_decoded_sentence_matches_the_real(self):
        sample = np.random.choice(range(len(self.int_sentence_list)), size = 10, replace = True)

        for which_sentence in sample:

            decoded_sentence = self.zipped[which_sentence][0]
            real_sentence = self.zipped[which_sentence][1]

            number_of_tokens_equal = sum([a==b for a,b in zip(decoded_sentence, real_sentence)])
            number_of_tokens_in_sentence = len(real_sentence)

            self.assertTrue(number_of_tokens_equal / number_of_tokens_in_sentence > 0.8)

if __name__ == '__main__':
    unittest.main()
