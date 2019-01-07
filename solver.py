#!/usr/bin/env python3

import sys
import os
from visualizer import visualizer
from search import a_star_search
from is_solvable import is_solvable
import parser
import heuristics
import solved_states


if __name__ == '__main__':
    data = parser.get_input()
    if not data:
        sys.exit(0)
    puzzle, size, args = data
    solved = solved_states.KV[args.s](size)
    if not is_solvable(puzzle, solved, size):
        print('this puzzle is not solvable')
        sys.exit(0)
    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    HEURISTICS = [heuristics.KV[args.f]]
    res = a_star_search(puzzle, solved, size, HEURISTICS, TRANSITION_COST)
    if not res:
        print('solution not found')
        sys.exit(0)
    steps, pqueue, open_set, closed_set, evaluated, rediscovered = res
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

