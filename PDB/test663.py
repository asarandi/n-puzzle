#!/usr/bin/env pypy3

import pickle
import time


input_files = [
        'zero_last.[1,5,6,9,10,13].pdb',
        'zero_last.[2,3,4].pdb',
        'zero_last.[7,8,11,12,14,15].pdb'
        ]

dictionaries = []
for f in input_files:
    dictionaries.append(pickle.load(open(f,'rb')))
    print('loaded',f)

for d in dictionaries:
    max_k = None
    max_v = -1
    min_k = None
    min_v = 100
    for k,v in d.items():
        if v > max_v:
            max_v = v
            max_k = k
        if v < min_v:
            min_v = v
            min_k = k
    print('file',f,'len', len(d))
    print('max k', max_k, 'max v', max_v)
    print('min k', min_k, 'min v', min_v)
    for k,v in d.items():
        if v == min_v:
            print('min k,v',k,v)
        if v == max_v:
            print('max k,v',k,v)
