#!/usr/bin/env python3

import sys
from copy import deepcopy
from heapq import heappush, heappop

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
        res.append(('LEFT', left))
    if (y % size) + 1 < size:
        right = clone_and_swap(data,y,y+1)
        res.append(('RIGHT', right))
    if y - size >= 0:
        up = clone_and_swap(data,y,y-size)
        res.append(('UP', up))
    if y + size < len(data):
        down = clone_and_swap(data,y,y+size)
        res.append(('DOWN', down))
    return res
                
def make_2d_array(tpl, size):
    lst = list(tpl)
    res = []
    for y in range(size):
        row = []
        for x in range(size):
            row.append(tpl[y*size+x])
        res.append(row)
    return res

def get_yx_coordinates(lst2d, size, itm):
    for y in range(size):
        for x in range(size):
            if lst2d[y][x] == itm:
                return (y,x)
    return None

def euclidean_distance(y0,x0,y1,x1):
    y = y0 - y1
    x = x0 - x1
    return (y*y) + (x*x)


def heuristic(candidate, solved, size):
    res = 0
    candidate = make_2d_array(candidate, size)
    solved = make_2d_array(solved, size)
    for y in range(size):
        for x in range(size):
            if solved[y][x] != candidate[y][x]:
                y1, x1 = get_yx_coordinates(candidate, size, solved[y][x])
                res += euclidean_distance(y,x,y1,x1)
    return res

NODE_MAX_SCORE = 999999
class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.f = NODE_MAX_SCORE
        self.g = NODE_MAX_SCORE
        self.h = NODE_MAX_SCORE
        self.n = -1
        self.direction = None

#--------------------------------------------------

data = []
for line in sys.stdin:
    data.append(int(line.strip()))

size = data[0]
data = data[1:]
data = tuple(data)
original = deepcopy(data)

solved_3 = [0,1,2,3,4,5,6,7,8]
solved_4 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
solved_5 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24]
if size == 3: solved = solved_3
elif size == 4: solved = solved_4
elif size == 5: solved = solved_5
else: sys.exit(0)
solved = tuple(solved)

root = Node(data)
root.f = 0
root.g = 0
root.h = heuristic(root.data, solved, size)
root.n = 1
opened = []
open_set = {}

heappush(opened, (root.f, root.n, root))

open_set[root.data] = root
closed_set = {}
success = False

open_count = 1
while opened and not success:
    f_score, n_score, e = heappop(opened) #select_by_f_score(opened)
    del open_set[e.data]

    if e.data == solved:
        success = True
        steps = []
        while True:
            if not e.parent:
                break
            steps.append(e)
            e = e.parent
        steps = list(reversed(steps))
        print(len(steps))
        for s in steps:
            print(s.direction)
        break
    else:
        closed_set[e.data] = e
        moves = possible_moves(e.data, size)
        for direction, m in moves:
            if m in closed_set: continue

            tentative_g = e.g + 1
            if m not in open_set:
                n = Node(m)
                open_set[m] = n
            else:                
                n = open_set[m]
                if tentative_g >= n.g:
                    continue
                opened.remove((n.f, n.n, n))

            n.direction = direction
            open_count += 1
            n.n = open_count
            n.parent = e
            n.g = tentative_g         
            n.h = heuristic(n.data, solved, size)
            n.f = n.g * n.h
            heappush(opened, (n.f, n.n, n))
