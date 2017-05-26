import unittest
import pickle
import os
import numpy as np
import sys
import tensorflow as tf

#add ../
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import data_to_tf_records

current_dir = os.path.dirname(os.path.realpath(__file__))

class TestDataToTFRecords(unittest.TestCase):

    data_to_tf_records = None

    def test_data_to_tf_records(self):
        self._given_data_to_tf_records()
        self._when_we_create_TF_records()
        self._then_we_can_decode()

    def _given_data_to_tf_records(self):
        self.data_to_tf_records = data_to_tf_records.DataToTFRecords()

    def _when_we_create_TF_records(self):
        self.data_to_tf_records.main()

    def _then_we_can_decode(self):

        tfrecord_file = 'test_tf.tfrecord'
        batch = self._get_batch_input([tfrecord_file])

        with tf.Session() as sess:
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)

            print(sess.run(batch))

            coord.request_stop()
            coord.join(threads)

    def _read_and_decode(self, filename_queue):
        ### read and decode te examples from the TFRecord-file

        reader = tf.TFRecordReader()

        _, serialized_example = reader.read(filename_queue)

        context_features = {
            "length": tf.FixedLenFeature([], dtype=tf.int64)
            }

        sequence_features = {
            "tokens": tf.FixedLenSequenceFeature([], dtype=tf.int64),
        }

        # Parse the example
        sequence_parsed = tf.parse_single_sequence_example(
            serialized=serialized_example,
            context_features = context_features,
            sequence_features = sequence_features
        )

        return sequence_parsed

    def _get_batch_input(self, file_names, batch_size = 2, capacity = 2, min_after_dequeue = 5):
        file_names_with_dirs = [file_name for file_name in file_names]
        filename_queue = tf.train.string_input_producer(file_names_with_dirs)
        with tf.name_scope('input'):
            input = self._read_and_decode(filename_queue)

            tokens = input[1]['tokens']
            length = input[0]['length']

            ### dynamic_pad is needed for sequences of different lengths
            input_batch = tf.train.batch([length, tokens], batch_size=batch_size, capacity = capacity, dynamic_pad = True)

        return input_batch


if __name__ == '__main__':
    unittest.main()
