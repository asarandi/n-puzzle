#!/usr/bin/env pypy3

import sys
import os
from copy import deepcopy
from time import sleep
from heapq import heappush, heappop, heapify
from math import sqrt
import argparse
from visualizer import visualizer
import heuristics

def error_exit(msg):
    print(msg)
    sys.exit(1)  

def validate_size(data):
    if len(data[0]) != 1:
        error_exit('invalid input')                                                 #first list[] in data must be size of matrix
    size = data.pop(0)[0]
    if size < 2:                                                                    # too small?
        error_exit('invalid input')
    if len(data) != size:                                                           # data[] should be an array of size N lists[]
        error_exit('invalid input')
    for line in data:                                                               # each list[] must be of size N (data must be square matrix)
        if len(line) != size:
            error_exit('invalid input')
    expanded = []
    for line in data:
        for x in line:
            expanded.append(x)
    generated = [x for x in range(size**2)]
    difference = [x for x in generated if x not in expanded]
    if len(difference) != 0:
        error_exit('invalid input')
    return size

def clone_and_swap(data,y0,y1):
    clone = deepcopy(list(data))
    tmp = clone[y0]
    clone[y0] = clone[y1]
    clone[y1] = tmp
    return tuple(clone)

def possible_moves(data, size):
    res = []
    y = data.index(0)
    if y % size > 0:
        left = clone_and_swap(data,y,y-1)
        res.append(left)
    if y % size + 1 < size:
        right = clone_and_swap(data,y,y+1)
        res.append(right)
    if y - size >= 0:
        up = clone_and_swap(data,y,y-size)
        res.append(up)
    if y + size < len(data):
        down = clone_and_swap(data,y,y+size)
        res.append(down)
    return res

NODE_MAX_SCORE = 999999

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.f = None
        self.g = None
        self.h = None
        self.n = None

def solved_zero_first(size):
    return tuple([x for x in range(size*size)])

def solved_zero_last(size):
    lst = [x for x in range(1,size*size)]
    lst.append(0)
    return tuple(lst)

def solved_snail(size):
    lst = [[0 for x in range(size)] for y in range(size)]
    moves = [(0,1),(1,0),(0,-1),(-1,0)]
    row = 0
    col = 0
    i = 1
    final = size * size
    size -= 1
    done = False
    while not done and size > 0:
        for move in moves:
            if done:
                break
            for _ in range(size):
                lst[row][col] = i
                row += move[0]
                col += move[1]
                i += 1
                if i == final:
                    done = True
                    break
        row += 1
        col += 1
        size -= 2

    res = []
    for row in lst:
        for i in row:
            res.append(i)
    return tuple(res)

def count_inversions(puzzle):
    res = 0
    for i in range(len(puzzle) - 1):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] and puzzle[j]:     #skip zero
                if puzzle[i] > puzzle[j]:
                    res += 1
    print('inversions', res)
    return res

def is_solvable(puzzle, size):
    inversions = count_inversions(puzzle)
    if size % 2 == 1:   # n is odd, 3x3 puzzle, 5x5 puzzle
        if inversions % 2 == 0:
            return True
    else:               # n is even
        zero_row = size - puzzle.index(0) // size
        if zero_row % 2 == 0 and inversions % 2 == 1:
            return True
        if zero_row % 2 == 1 and inversions % 2 == 0:
            return True
    return False





                            
                            
HEURISTICS = {
        'hamming':      heuristics.hamming,
        'chebyshev':    heuristics.chebyshev,
        'manhattan':    heuristics.manhattan,
        'euclidean':    heuristics.euclidean,
        'euclidea2':    heuristics.euclidean2,
        'conflicts':    heuristics.linear_conflicts,
        'gaschnig':     heuristics.gaschnig,
        'misplaced':    heuristics.misplaced,
        'suminv':       heuristics.suminv
        }

parser = argparse.ArgumentParser(description='n-puzzle 42')

parser.add_argument('-g', action='store_true', help='greedy search')
parser.add_argument('-u', action='store_true', help='uniform-cost search')
parser.add_argument('-f', help='heuristic function',
        choices=list(HEURISTICS.keys()), default='manhattan')
parser.add_argument('-s', help='solved state of the puzzle',
        choices=['zerofirst', 'zerolast', 'snail'], default='snail')
parser.add_argument('-v', action='store_true', help='gui visualize solution')
parser.add_argument('file', help='input file')

args = parser.parse_args()

with open(args.file) as fp:
    data = fp.read().splitlines()
    fp.close()

data = [line.split('#')[0] for line in data]                                        #remove comments
data = [line for line in data if len(line) > 0]                                     #remove empty lines
data = [[int(x) for x in line.split(' ') if len(x) > 0] for line in data]           #convert to ints

size = validate_size(data)
flat = []
for line in data:
    for itm in line:
        flat.append(itm)
data = tuple(flat)

solved = None
if args.s == 'zerofirst':
    solved = solved_zero_first(size)
elif args.s == 'zerolast':
    solved = solved_zero_last(size)
elif args.s == 'snail':                                       #default
    solved = solved_snail(size)

if not is_solvable(data, size):
    print('this puzzle is unsolvable')
    sys.exit(0)

TRANSITION_COST = 1
if args.g:
    TRANSITION_COST = 0


print('initial state', data)
print('final state', solved)

for k in HEURISTICS:
    print(k,'score\t: ', HEURISTICS[k](data,solved,size))

root = Node(data)
unique_id = 0
root.n = unique_id
root.g = 0
root.h = HEURISTICS[args.f](data, solved, size)
root.f = root.g + root.h
opened = []
open_set = {}
heappush(opened, (root.f, root.n, root))
open_set[root.data] = root
closed_set = {}
success = False

evaluated = 0
rediscovered = 0
while opened and not success:
    f_score, node_id, e = heappop(opened)
    if e.data not in open_set:
        continue

    evaluated += 1
    if e.data == solved:
        success = True
        steps = []
        while True:
            steps.append(e)
            if not e.parent:
                break
            e = e.parent
        steps = list(reversed(steps))
        print('success')
        print('current g value', steps[-1].g)
        print('length of solution', len(steps))
        for s in steps:
            print(s.data, 'g value', s.g, 'h value', s.h, 'f value', s.f, 'n value', s.n)
        print('current open set', len(open_set))
        print('current queue size', len(opened))
        print('closed set count', len(closed_set))
        print('nodes evaluated', evaluated)
        print('rediscovered nodes', rediscovered)
        if args.v:
            visualizer(steps, size)
        break
    else:

        del open_set[e.data]
        closed_set[e.data] = e
        moves = possible_moves(e.data, size)
        tentative_g = e.g + TRANSITION_COST

        for m in moves:
            if m in closed_set:
                continue
            if m in open_set:
                if tentative_g >= open_set[m].g:
                    continue
                n = open_set[m]
                rediscovered += 1
            else:
                n = Node(m)
                open_set[m] = n
                n.h = 0
                if not args.u:
                    n.h = HEURISTICS[args.f](m, solved, size)
            unique_id += 1
            n.n = unique_id
            n.parent = e
            n.g = tentative_g
            n.f = n.g + n.h
            heappush(opened, (n.f, n.n, n))
