from itertools import count
from heapq import heappush, heappop
from collections import deque
from math import inf

EMPTY_TILE = 0


def clone_and_swap(puzzle, i, j):
    clone = list(puzzle)
    clone[i], clone[j] = clone[j], clone[i]
    return tuple(clone)


# UDLR
def possible_moves(puzzle, size):
    res = []
    i = puzzle.index(EMPTY_TILE)
    if i - size >= 0:
        res.append(clone_and_swap(puzzle, i, i - size))
    if i + size < len(puzzle):
        res.append(clone_and_swap(puzzle, i, i + size))
    if i % size > 0:
        res.append(clone_and_swap(puzzle, i, i - 1))
    if i % size + 1 < size:
        res.append(clone_and_swap(puzzle, i, i + 1))
    return res


def ida_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST):
    def search(path, g, bound, evaluated):
        evaluated += 1
        node = path[0]
        f = g + HEURISTIC(node, solved, size)
        if f > bound:
            return f, evaluated
        if node == solved:
            return True, evaluated
        ret = inf
        moves = possible_moves(node, size)
        for m in moves:
            if m not in path:
                path.appendleft(m)
                t, evaluated = search(path, g + TRANSITION_COST, bound, evaluated)
                if t is True:
                    return True, evaluated
                if t < ret:
                    ret = t
                path.popleft()
        return ret, evaluated

    bound = HEURISTIC(puzzle, solved, size)
    path = deque([puzzle])
    evaluated = 0
    while path:
        t, evaluated = search(path, 0, bound, evaluated)
        if t is True:
            path.reverse()
            return (True, path, {"space": len(path), "time": evaluated})
        elif t is inf:
            return (False, [], {"space": len(path), "time": evaluated})
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
            return (True, steps, {"space": len(open_set), "time": len(closed_set)})
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
    return (False, [], {"space": len(open_set), "time": len(closed_set)})
