#!/usr/bin/env pypy3

import sys
from time import perf_counter
from npuzzle.visualizer import visualizer
from npuzzle.search import a_star_search
from npuzzle.is_solvable import is_solvable
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import solved_states


if __name__ == '__main__':
    data = parser.get_input()
    if not data:
        sys.exit()
    puzzle, size, args = data
    solved = solved_states.KV[args.s](size)
    if not is_solvable(puzzle, solved, size):
        print('this puzzle is not solvable')
        sys.exit(0)
    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    HEURISTICS = [heuristics.KV[args.f]]
    t_start = perf_counter()
    res = a_star_search(puzzle, solved, size, HEURISTICS, TRANSITION_COST)
    t_delta = perf_counter() - t_start
    print('search finished in %.4f second(s)' % (t_delta))
    if not res:
        print('solution not found')
        sys.exit(0)
    steps, pqueue, open_set, closed_set, evaluated, rediscovered = res
    print('%d evaluated nodes, %.8f second(s) per node' % (evaluated, t_delta / evaluated))
    print('success')
    print('current g value', steps[-1].g)
    print('length of solution', len(steps))
    for s in steps:
        print(s.data, 'g value', s.g, 'h value', s.h, 'f value', s.f, 'n value', s.n)
    print('current open set', len(open_set))
    print('current queue size', len(pqueue))
    print('closed set count', len(closed_set))
    print('nodes evaluated', evaluated)
    print('rediscovered nodes', rediscovered)
    if args.v:
        visualizer(steps, size)

