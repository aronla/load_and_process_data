import multiprocessing as mp, os
from collections import Counter
import data_to_tf_records as dttf
import time
import pickle
import pool_wrapper

#init objects
cores = 3
pool = mp.Pool(cores)
jobs = []

root_dir = '/Users/aron/programming/projects/load_and_process_data/'
data_dir = root_dir + 'tests/sentence_test/'
save_dir = root_dir + 'results/tf_records/'

file_names = os.listdir(data_dir)

for index, file_name in enumerate(file_names):
    file_name = data_dir + file_name
    jobs.append(pool.apply_async(pool_wrapper.data_to_tf_records_wrapper, (file_name, save_dir, index)))

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()
