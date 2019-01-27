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
    
puzzles = {
        
#------------------------------------------------------------------------------
#
#        snail solution and 6-6-3 pattern groups
#        
#        01 02 03 04         01               02 03 04
#        12 13 14 05         12        13 14        05
#        11 -- 15 06         11 --        15        06
#        10 09 08 07         10 09 08               07
#
    #    'snail': {            
    #        'goal': [1,2,3,4,12,13,14,5,11,0,15,6,10,9,8,7],
    #        'patterns': [
    #            [1,12,11,10,9,8],
    #            [2,3,4,5,6,7],
    #            [13,14,15]
    #            ],
    #        'fillers': [13,13,1]
    #        },
#---#---------------------------------------------------------------------------
#
#   #     zero_first solution and pattern groups
#   #     
#   #     -- 01 02 03         --     01       02 03 
#   #     04 05 06 07         04     05 06       07
#   #     08 09 10 11         08     09 10       11
#   #     12 13 14 15         12     13       14 15
#
    #    'zero_first': {
    #        'goal': [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
    #        'patterns': [
    #            [1,2,3,7,11,15],
    #            [4,5,6,9,10,14],
    #            [8,12,13]
    #            ],
    #        'fillers': [8,8,1]
    #        },
#------------------------------------------------------------------------------
#
#        zero_last solution and its pattern groups
#                
#        01 02 03 04         01       02 03 04
#        05 06 07 08         05 06               07 08
#        09 10 11 12         09 10               11 12
#        13 14 15 --         13               14 15 --
#
        'zero_last': {
            'goal': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],
            'patterns': [
                [1,5,6,9,10,13,0],
                [7,8,11,12,14,15,0],
                [2,3,4,0]
                ],
            'fillers': [2,2,1]
            }
}

#------------------------------------------------------------------------------

def node_to_key(node, pattern):
    res = 0
    for p in pattern:
        res <<= 4
        res += node.index(p)
    return res

def key_to_node(key, pattern, filler):
    res = [filler for x in range(16)]
    for p in reversed(pattern):
        res[key & 0xf] = p
        key >>= 4
    return tuple(res)

for puzzle_name, puzzle_data in puzzles.items():
    for idx, pattern in enumerate(puzzle_data['patterns']):
        filler = puzzle_data['fillers'][idx]
        output_file = '%s.%s.pdb' % (puzzle_name, str(pattern).replace(' ',''))
        print('bfs progress for:', output_file)

        visited = set()
        result = {}
        
        root = node_to_key(puzzle_data['goal'], pattern)
        queue = deque([root << 8])
        evaluated = 0
        while queue:
            long_key_g = queue.popleft()
            g = long_key_g & 0xff
            long_key = long_key_g >> 8
            short_key = long_key_g >> 12

            evaluated += 1
            if evaluated % 1000000 == 0:
                print('evaluated', evaluated)
            
            if short_key in result:
                existing_g = result[short_key]
                if existing_g > g:
                    result[short_key] = g
                else:
                    g = existing_g
            else:
                result[short_key] = g

            node = key_to_node(long_key, pattern, filler)
            moves = search.possible_moves(node, 4)  #4=size
            for m in moves:
                mk = node_to_key(m, pattern)
                if mk in visited:
                    continue
                visited.add(mk)
                queue.append((mk << 8) + g + 1)
        
        visited.clear()
        print(output_file, 'bfs done, writing to disk..')
        pickle.dump(result, open(output_file, 'wb'))
        print('saved')
        print('----------------------------------------')
