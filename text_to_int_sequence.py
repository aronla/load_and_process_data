import numpy as np
from text_utils import TextUtils
UNK = '<unk>'
NUM = '<NUM>'
MIXED_NUM = '<MIXED_NUM>'
MIN_SENTENCE_LENGTH = 15

class TextToIntSequence:

    def __init__(self, word2index):
        self.word2index = word2index

    def get_list_of_int_from_text(self, text):
        sentences = TextUtils.text_to_sentences(text)
        sentences_as_int_lists = list()
        sentences_lists = list()

        for sentence in sentences:
            int_sentence = []
            tokens_in_sentence = self._sentence_to_tokens(sentence)
            tokens_in_sentence = self._filter_sentence(tokens_in_sentence)

            for token in tokens_in_sentence:
                if token in self.word2index:
                    int_sentence.append(self.word2index[token])
                else:
                    int_sentence.append(self.word2index[UNK])

            if(len(int_sentence) != 0):
                sentences_as_int_lists.append(int_sentence)
                sentences_lists.append(tokens_in_sentence)


        return sentences_as_int_lists, sentences_lists

    def _sentence_to_tokens(self, chunk):
            chunk = TextUtils.lower_case(chunk)
            chunk = TextUtils.filter_line(chunk)
            tokens = TextUtils.tokenize(chunk)
            tokens = TextUtils.remove_single_letter_tokens(tokens)
            tokens = TextUtils.convert_to_numeric_token(tokens)
            return tokens

    def _filter_sentence(self, sentence):
        sentence_length = len(sentence)
        number_of_tokens_of_max_length_2 = len([x for x in sentence if len(x) < 3])
        number_of_num_tokens = len([x for x in sentence if x == NUM or x == MIXED_NUM])
        if sentence_length < MIN_SENTENCE_LENGTH:
            return []
        elif number_of_tokens_of_max_length_2/sentence_length > 0.7:
            return []
        elif number_of_num_tokens/sentence_length > 0.5:
            return []
        else:
            return sentence
