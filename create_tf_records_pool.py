import multiprocessing as mp, os
from collections import Counter
import data_to_tf_records as dttf
import time
import pickle

#init objects
cores = 4
pool = mp.Pool(cores)
jobs = []

def process_wrapper(file_name, index):
       data_to_tf_records = dttf.DataToTFRecords()
       save_file_name = 'tf_data_' + str(index) + '.tfrecord'
       data_to_tf_records.load_and_write(file_name, save_file_name) 

#create jobs
file_names = os.listdir()

for index, file_name in enumerate(file_names):
    jobs.append(pool.apply_async(process_wrapper, file_name, index))

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()
