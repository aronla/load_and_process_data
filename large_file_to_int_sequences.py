import multiprocessing as mp, os
from collections import Counter
import time
import pickle
from text_to_int_sequence import TextToIntSequence

file_name = '/Users/aron/data/deepdata_large.txt'
word_index_dict = pickle.load(open('results/word_index_most_common_50000_tokens.pickle', 'rb'))
word2index = word_index_dict['word2index']
text_to_int_sequence = TextToIntSequence(word2index)

def process_wrapper(chunk_start, chunk_size, total_chunks):
    with open(file_name, 'r') as f:
        current = mp.current_process()
        process_id = current._identity[0]

        f.seek(chunk_start)
        text = f.read(chunk_size)

        int_sentence_list, word_sentence_list = text_to_int_sequence.get_list_of_int_from_text(text)

        with open('results/sentences/worker_' + str(process_id) + '_chunk_' + str(chunk_start) + '_sentences.pickle', 'wb') as f:
            pickle.dump([int_sentence_list, word_sentence_list], f)

        print(str(chunk_start / total_chunks) + ' % done')

def chunkify(fname, size=1024*1024*100):
    file_end = os.path.getsize(fname)
    total_chunks = file_end
    with open(fname,'rb') as f:
        chunk_end = f.tell()
        while True:
            chunk_start = chunk_end
            f.seek(size,1)
            f.readline()
            chunk_end = f.tell()
            yield chunk_start, chunk_end - chunk_start, total_chunks
            if chunk_end > file_end:
                break

#init objects
cores = 4
pool = mp.Pool(cores)
jobs = []

#create jobs
for chunk_start, chunk_size, total_chunks in chunkify(file_name):
    jobs.append(pool.apply_async(process_wrapper, (chunk_start, chunk_size, total_chunks)) )

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()
