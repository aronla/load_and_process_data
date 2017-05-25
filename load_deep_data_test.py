import numpy as np
import pickle
import sys
from read_text_file import ReadTextFile
from text_to_int_sequence import TextToIntSequence

############################## Class to read the content of (a large) file and parse it into a matrix of ints

class CreateDataset:

    file_name = '/Users/aron/data/deepdata.txt'
    read_data = ReadTextFile(file_name)
    text_to_int_sequence = TextToIntSequence()

    def create_data(self):
        for piece in self.read_data.read_in_chunks():
            self.text_to_int_sequence.get_list_of_int_from_text(piece)

        self.data_set = self.data_processing.data_set

    def create_data_file(self):
        self.create_data()
        print(self.data_set)
        pickle.dump(self.data_set, open('dataset.pickle', 'wb'))

if __name__ == '__main__':
    create_dataset = CreateDataset()
    create_dataset.create_data_file()
