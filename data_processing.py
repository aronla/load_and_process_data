import numpy as np

class DataProcessing:
    sentence_length = 300
    cumul = 0
    no_of_examples = 10
    def __init__(self):
        self.data_set = np.zeros(shape = (self.no_of_examples, self.sentence_length))

    def get_training_set_as_integers(self, data):
        training_set = self._dataset_set_as_integers(data)
        return training_set

    def _dataset_set_as_integers(self, dataset):
        toknized_dataset = self.get_dataset_as_tokenized_sentences(dataset)

        integer_dataset = list()
        for sentence in toknized_dataset:
            integer_sentence = self._convert_sentence_to_integer_sentence(sentence)
            integer_dataset.append(integer_sentence)
        return integer_dataset

    def get_dataset_as_tokenized_sentences(self, dataset):
        tokenized_sentences = []
        for training_example in dataset:
            sentence = [[token] for token in training_example]
            tokenized_sentences.append(sentence)
        return tokenized_sentences

    def _convert_sentence_to_integer_sentence(self, sentence_as_tokens):
        return [self._token_to_integer(token[0]) for token in sentence_as_tokens]

    def _token_to_integer(self, token):
        FIXED_ALPHABET_SIZE = 100000
        return abs(hash(token)) % (FIXED_ALPHABET_SIZE-1)+1

    def get_sentences(self, words):
            sentences = []
            while len(words) > 9:
                if words == []:
                    break
                sentence = words[0:self.sentence_length]
                sentences.append(sentence)
                words = words[(self.sentence_length+1):-1]
            return sentences

    def process_data(self, txt):
        words = txt.split(' ')
        if len(words) >= self.sentence_length:
            sentences = self.get_sentences(words)
            sentences_as_integers = self.get_training_set_as_integers(sentences)

            if len(sentences_as_integers[-1]) != self.sentence_length:
                sentences_as_integers = sentences_as_integers[0:-1]

            sentences_as_integers = np.array(sentences_as_integers)
            no_of_rows = sentences_as_integers.shape[0]

            self.data_set[self.cumul:(self.cumul + no_of_rows)] = sentences_as_integers
            self.cumul += no_of_rows
