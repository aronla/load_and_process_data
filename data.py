EN_WHITELIST = '0123456789abcdefghijklmnopqrstuvwxyz ' # space is included in whitelist
EN_BLACKLIST = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\''

FILENAME = r'/Users/aron/data/deepdata_large.txt'

UNK = 'unk'
VOCAB_SIZE = 6000

import random
import sys

import nltk
import itertools
from collections import defaultdict

import numpy as np

import pickle


def ddefault():
    return 1

'''
 read lines from file
     return [list of lines]

'''
def read_lines(filename):
    file = open(filename)
    txt = file.read()
    import ipdb; ipdb.set_trace()
    # file.read().split('\n')[:-1]
    return txt.split('\n')[:-1] 


'''
 split sentences in one line
  into multiple lines
    return [list of lines]

'''
def split_line(line):
    return line.split('.')


'''
 remove anything that isn't in the vocabulary
    return str(pure ta/en)

'''
def filter_line(line, whitelist):
    return ''.join([ ch for ch in line if ch in whitelist ])


'''
 read list of words, create index to word,
  word to index dictionaries
    return tuple( vocab->(word, count), idx2w, w2idx )

'''
def index_(tokenized_sentences, vocab_size):
    # get frequency distribution
    freq_dist = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    # get vocabulary of 'vocab_size' most used words
    vocab = freq_dist.most_common(vocab_size)
    # index2word
    index2word = ['_'] + [UNK] + [ x[0] for x in vocab ]
    # word2index
    word2index = dict([(w,i) for i,w in enumerate(index2word)] )
    return index2word, word2index, freq_dist




'''
 replace words with indices in a sequence
  replace with unknown if word not in lookup
    return [list of indices]

'''
def pad_seq(seq, lookup, maxlen):
    indices = []
    for word in seq:
        if word in lookup:
            indices.append(lookup[word])
        else:
            indices.append(lookup[UNK])
    return indices + [0]*(maxlen - len(seq))


def process_data():

    print('\n>> Read lines from file')
    lines = read_lines(filename=FILENAME)

    # change to lower case (just for en)
    lines = [ line.lower() for line in lines ]

    print('\n:: Sample from read(p) lines')
    print(lines[121:125])

    # filter out unnecessary characters
    print('\n>> Filter lines')
    lines = [ filter_line(line, EN_WHITELIST) for line in lines ]
    print(lines[121:125])

    # # filter out too long or too short sequences
    # print('\n>> 2nd layer of filtering')
    # lines = filter_data(lines)
    # print('\nq : {0}'.format(lines[60]))


    # convert list of [lines of text] into list of [list of words ]
    print('\n>> Segment lines into words')
    tokenized = [ wordlist.split(' ') for wordlist in lines ]
    print('\n:: Sample from segmented list of words')
    print('\nq : {0}'.format(tokenized[60]))
    print('\nq : {0}'.format(tokenized[61]))


    # indexing -> idx2w, w2idx : en/ta
    print('\n >> Index words')
    idx2w, w2idx, freq_dist = index_( tokenized, vocab_size=VOCAB_SIZE)

    # print('\n >> Zero Padding')
    # idx = zero_pad(tokenized, w2idx)

    # print('\n >> Save numpy arrays to disk')
    # # save them
    # np.save('idx.npy', idx)

    # let us now save the necessary dictionaries
    metadata = {
            'w2idx' : w2idx,
            'idx2w' : idx2w,
            'freq_dist' : freq_dist
                }

    # write to disk : data control dictionaries
    with open('results/metadata.pickle', 'wb') as f:
        pickle.dump(metadata, f)

def load_data(PATH=''):
    # read data control dictionaries
    with open(PATH + 'metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    # read numpy arrays
    idx = np.load(PATH + 'idx.npy')
    return metadata, idx


if __name__ == '__main__':
    process_data()
