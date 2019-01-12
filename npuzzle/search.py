from itertools import count
from heapq import heappush, heappop
from collections import OrderedDict
from math import inf

EMPTY_TILE = 0

def clone_and_swap(data,y0,y1):
    clone = list(data)
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

def ida_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST):
    def search(path, g, bound):
        node = next(reversed(path))
        f = g + HEURISTIC(node, solved, size)
        if f > bound:
            return f
        if node == solved:
            return True
        ret = inf
        moves = possible_moves(node, size)
        for m in moves:
            if m not in path:
                path[m] = next(c)
                t = search(path, g + TRANSITION_COST, bound)
                if t is True:
                    return True
                if t < ret:
                    ret = t
                path.popitem()
        return ret

    c = count()
    bound = HEURISTIC(puzzle, solved, size)
    path = OrderedDict()
    path[puzzle] = next(c)
    while path:
        t = search(path, 0, bound)
        if t is True:
            print('ida star found')#, path, bound)
            res = list(path)
            print('ida star length', len(path))
            for r in res:
                print(r, path[r])
            return True
        elif t is inf: 
            print('ida star not found')#, path, bound)
            return False
        else:
            bound = t   


def a_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST):
    c = count()
    queue = [(0, next(c), puzzle, 0, None)]
    open_set = {}
    closed_set = {}
    while queue:
        _, _, node, node_g, parent = heappop(queue)
        if node == solved:
            steps = [node]
            while parent is not None:
                steps.append(parent)
                parent = closed_set[parent]
            steps.reverse()
            return (True, steps, queue, open_set, closed_set)
        if node in closed_set:
            continue
        closed_set[node] = parent
        tentative_g = node_g + TRANSITION_COST
        moves = possible_moves(node, size)
        for m in moves:
            if m in closed_set:
                continue
            if m in open_set:
                move_g, move_h = open_set[m]
                if move_g <= tentative_g:
                    continue
            else:
                move_h = HEURISTIC(m, solved, size)
            open_set[m] = tentative_g, move_h
            heappush(queue, (move_h + tentative_g, next(c), m, tentative_g, node))
    return (False, [], queue, open_set, closed_set)
