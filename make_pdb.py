#!/usr/bin/env pypy3

import argparse
import pickle
from npuzzle import solved_states
from npuzzle import search
from collections import deque

def pattern_plus_zero(node, pattern):
    lst = list(node)
    for i, val in enumerate(lst):
        if val != 0 and val not in pattern:
            lst[i] = -1
    return tuple(lst)
    
def pattern_only(node, pattern):
    lst = list(node)
    for i, val in enumerate(lst):
        if val not in pattern:
            lst[i] = -1
    return tuple(lst)

parser = argparse.ArgumentParser(description='pdbgen for n-puzzle solver')
parser.add_argument('solution', help='solved state', choices=list(solved_states.KV.keys()))
args = parser.parse_args()

PUZZLE_SIZE = 4

'''
patterns = [
        [1,2,5,9,13],
        [3,6,10,14,15],
        [4,7,8,11,12]
        ]
'''



closed_set = {}
open_set = set()
PAT1 = [4,7,8,11,12]  #[3,6,10,14,15]       #[1,2,5,9,13]
board   =   (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
root = pattern_plus_zero(board, PAT1)   # XXX with zero !!
open_set.add(root)
queue = deque([(root, 0)])
db = {}

while queue:
    node, g = queue.popleft()
    open_set.remove(node)
    closed_set[node] = g
    pp = pattern_only(node, PAT1)
    if pp not in db:
        db[pp] = g
    moves = search.possible_moves(node, PUZZLE_SIZE)
    for m in moves:
        if m in open_set:
            continue
        mp = pattern_only(m, PAT1)
        if mp in db:
            if db[mp] > db[pp] + 1:
                db[mp] = db[pp] + 1
        if m in closed_set:
            continue
        open_set.add(m)
        queue.append((m, db[pp] + 1))

print('closed set', len(closed_set))
print('db', len(db))

fn = '%dx%d-%s.%s.pdb' % (PUZZLE_SIZE,PUZZLE_SIZE,args.solution, str(PAT1).replace(', ', '_')[1:-1])
with open(fn, 'wb') as fp:
    pickle.dump(db, fp)
    fp.close()
