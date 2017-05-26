import tensorflow as tf
import pickle
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

class DataToTFRecords:
    int_sentence_list = None
    word_sentence_list = None

    def load_data(self, file_name):
        with open(file_name, 'rb') as f:
            self.int_sentence_list, self.word_sentence_list = pickle.load(f)

    def write_to_tfrecords(self, tfrecord_file):
        ### create SequenceExamples and save them into a TFrecord-file
        writer = tf.python_io.TFRecordWriter(tfrecord_file)

        for int_sentence in self.int_sentence_list:
            example = tf.train.SequenceExample()
            ft_tokens = example.feature_lists.feature_list['tokens']
            example.context.feature['length'].int64_list.value.append(len(int_sentence))

            for t in int_sentence:
                ft_tokens.feature.add().int64_list.value.append(t)
            writer.write(example.SerializeToString())

        writer.close()

    def load_and_write(self, file_name, save_file_name):
        self.load_data(file_name)
        self.write_to_tfrecords(save_file_name)

    def main(self):
        file_name = current_dir + '/tests/test_data.pickle'
        save_file_name = 'tf_test.tfrecord'
        self.load_and_write(file_name, save_file_name)
