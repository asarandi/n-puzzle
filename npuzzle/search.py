from copy import deepcopy
from heapq import heappush, heappop, heapify

EMPTY_TILE = 0

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.f = None
        self.g = None
        self.h = None
        self.n = None

def clone_and_swap(data,y0,y1):
    clone = deepcopy(list(data))
    tmp = clone[y0]
    clone[y0] = clone[y1]
    clone[y1] = tmp
    return tuple(clone)

def possible_moves(data, size):
    res = []
    y = data.index(EMPTY_TILE)
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

def a_star_search(puzzle, solved, size, HEURISTICS, TRANSITION_COST):
    root = Node(puzzle)
    unique_id = 0
    root.n = unique_id
    root.g = 0
    root.h = 0
    for h in HEURISTICS:
        root.h += h(puzzle, solved, size)
    root.f = root.g + root.h
    pqueue = []
    open_set = {}
    heappush(pqueue, (root.f, root.n, root))
    open_set[root.data] = root
    closed_set = {}
    evaluated = 0
    rediscovered = 0
    while pqueue:
        f_score, node_id, e = heappop(pqueue)
        if e.data not in open_set:
            continue
        evaluated += 1
        if e.data == solved:
            steps = []
            while True:
                steps.append(e)
                if not e.parent:
                    break
                e = e.parent
            steps = list(reversed(steps))
            return (steps, pqueue, open_set, closed_set, evaluated, rediscovered)
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
                    for h in HEURISTICS:
                        n.h += h(m, solved, size)
                unique_id += 1
                n.n = unique_id
                n.parent = e
                n.g = tentative_g
                n.f = n.g + n.h
                heappush(pqueue, (n.f, n.n, n))
    return None
