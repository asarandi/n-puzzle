#!/usr/bin/env pypy3

import sys
from time import perf_counter
from npuzzle.visualizer import visualizer
from npuzzle.search import a_star_search
from npuzzle.is_solvable import is_solvable
from npuzzle import colors
from npuzzle.colors import color
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import solved_states
import resource

if __name__ == '__main__':
    data = parser.get_input()
    if not data:
        sys.exit()
    puzzle, size, args = data
    solved = solved_states.KV[args.s](size)
    if not is_solvable(puzzle, solved, size):
        print(color('red','this puzzle is not solvable'))
        sys.exit(0)
    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    colors.ENABLED = True

    HEURISTIC = heuristics.KV[args.f]
    if args.u:
        HEURISTIC = heuristics.uniform_cost
    t_start = perf_counter()
    m_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    res = a_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST)
    m_delta = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - m_start
    t_delta = perf_counter() - t_start

    print(color('cyan','search duration') + ' %.4f second(s)' % (t_delta))
    print(color('yellow','memory usage') + ' %d bytes' % (m_delta))
    if not res:
        print(color('red','solution not found'))
        sys.exit(0)

    steps, pqueue, open_set, closed_set, evaluated, rediscovered = res

    print(color('green','%d evaluated nodes %.8f second(s) per node') % (len(closed_set), t_delta / len(closed_set)))
    print('length of solution', len(steps))
    for s in steps:
        print(s)
    print(color('cyan','current open set'), len(open_set))
    print(color('yellow','current queue size'), len(pqueue))
    print('closed set count', len(closed_set))
    print('nodes evaluated', evaluated)
    print('rediscovered nodes', rediscovered)
    if args.v:
        visualizer(steps, size)

