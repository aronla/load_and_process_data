
import data_to_tf_records as dttf

def data_to_tf_records_wrapper(file_name, save_dir, index):
       data_to_tf_records = dttf.DataToTFRecords()
       save_file_name = save_dir + 'tf_data_' + str(index) + '.tfrecord'
       data_to_tf_records.load_and_write(file_name, save_file_name) 
