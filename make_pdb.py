#!/usr/bin/env pypy3

import argparse
import pickle
from npuzzle import solved_states
from npuzzle import search
from collections import deque
import mmap

def node_to_bytes(node):
    b = bytearray()
    i = 0
    while i < len(node):
        b.append((node[i] << 4) + node[i+1])
        i += 2
    return bytes(b)

def bytes_to_node(b):
    lst = []
    for i in b:
        lst.append(i >> 4)
        lst.append(i & 15)
    return tuple(lst)

def database_put(node, extra, database, save_if_less=False):
    RECORD_SIZE = 9
    NUM_RECORDS = len(database) // RECORD_SIZE
    b = node_to_bytes(node)
    idx = (hash(b) % NUM_RECORDS) * RECORD_SIZE
    while True:
        rec = database[idx:idx + 8]
        if sum(rec) == 0:
            break
        if rec == b:
            break
        idx += RECORD_SIZE
        if idx >= len(database):
            idx = 0
    if save_if_less:
        if rec == b:
            if database[idx+8] <= extra:
                return
    database[idx:idx + 8] = b
    database[idx+8] = extra

def database_get(node, database):
    RECORD_SIZE = 9
    NUM_RECORDS = len(database) // RECORD_SIZE
    b = node_to_bytes(node)
    idx = (hash(b) % NUM_RECORDS) * RECORD_SIZE
    while True:
        rec = database[idx:idx + 8]
        if sum(rec) == 0:
            return None
        if rec == b:
            return int(database[idx+8])
        idx += RECORD_SIZE
        if idx >= len(database):
            idx = 0

def pattern_plus_zero(node, pattern, filler):
    lst = list(node)
    for i, val in enumerate(lst):
        if val != 0 and val not in pattern:
            lst[i] = filler
    return tuple(lst)
    
def pattern_only(node, pattern, filler):
    lst = list(node)
    for i, val in enumerate(lst):
        if val not in pattern:
            lst[i] = filler
    return tuple(lst)


# # # # # # # # # # # # # # # # # # # # # # # # # 
## # # # # # # # # # # # # # # # # # # # # # # ##
# # # # # # # # # # # # # # # # # # # # # # # # # 


patterns = {
        (1,5,6,9,10,13) : 2,
        (7,8,11,12,14,15) : 2,
        (2,3,4) : 1
        }

for PAT1, filler in patterns.items():

    visited_size = 57657600 * 9 * 2
    visited = mmap.mmap(-1, visited_size)
    result_size = 5765760 * 12 #9 too small
    result = mmap.mmap(-1, result_size)
    
    root = pattern_plus_zero((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0), PAT1, filler)
    database_put(root, 1, visited)
    queue = deque([(root, 0)])
    evaluated = 0

    while queue:
        node, g = queue.popleft()
        evaluated += 1
        if evaluated % 1000000 == 0:
            print(evaluated)
        pp = pattern_only(node, PAT1, filler)
        database_put(pp, g, result, True)
        moves = search.possible_moves(node, 4)
        for m in moves:
            if database_get(m, visited) != None:
                continue    # record exists
            database_put(m, 1, visited)
            cc = pattern_only(m, PAT1, filler)
            queue.append((m, database_get(pp, result) + 1))
            
    print('done')
    fn = str(PAT1) + '.pdb'
    with open(fn, 'wb') as fp:
        fp.write(result)
        fp.close()
    result.close()
    visited.close()

