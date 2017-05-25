import multiprocessing as mp, os
from collections import Counter
import time
import pickle
from text_to_int_sequence import TextToIntSequence

word_index_dict = pickle.load(open('results/word_index_most_common_50000_tokens.pickle', 'rb'))
word2index = word_index_dict['word2index']
text_to_int_sequence = TextToIntSequence(word2index)

def process(line):
    ct = Counter(line)

def process_wrapper(chunkStart, chunkSize):
    with open('/Users/aron/data/deepdata_small.txt', 'r') as f:
        current = mp.current_process()
        process_id = current._identity[0]

        print(chunkStart)
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            seq_list = text_to_int_sequence.get_list_of_int_from_text(line)
            with open('results/sentences/worker_' + str(process_id) + '_chunk_' + str(chunkStart) + '_sentences.pickle', 'wb') as f:
                pickle.dump(seq_list, f)

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

#init objects
cores = 4
pool = mp.Pool(cores)
jobs = []

#create jobs
for chunkStart, chunkSize in chunkify('/Users/aron/data/deepdata_small.txt'):
    jobs.append(pool.apply_async(process_wrapper, (chunkStart, chunkSize)) )

#wait for all jobs to finish
for job in jobs:
    job.get()

#clean up
pool.close()
