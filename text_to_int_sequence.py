import numpy as np
from text_utils import TextUtils
UNK = '<unk>'

class TextToIntSequence:

    def __init__(self, word2index):
        self.word2index = word2index


    def get_list_of_int_from_text(self, text):
        sentences = TextUtils.text_to_sentences(text) 
        sentences_as_int_lists = list()

        for sentence in sentences:
            int_sentence = []
            tokens_in_sentence = self._sentence_to_tokens(sentence)

            for token in tokens_in_sentence:
                if token in self.word2index:
                    int_sentence.append(self.word2index[token])
                else:
                    int_sentence.append(self.word2index[UNK])

            sentences_as_int_lists.append(int_sentence)

        return sentences_as_int_lists

    def _sentence_to_tokens(self, chunk):
            chunk = TextUtils.lower_case(chunk)
            chunk = TextUtils.filter_line(chunk)
            tokens = TextUtils.tokenize(chunk)
            tokens = TextUtils.remove_single_letter_tokens(tokens)
            tokens = TextUtils.convert_to_numeric_token(tokens)
            return tokens

