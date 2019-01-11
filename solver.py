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


colors.ENABLED = True
YES_COLOR = 'green'
NO_COLOR = 'red'
def color_yes_no(v):
    return color(YES_COLOR, 'YES') if v else color(NO_COLOR, 'NO')


def verbose_info(args, puzzle, solved, size):
    opts1 = {'greedy search': args.g,
            'uniform cost search': args.u,
            'solvable': is_solvable(puzzle, solved, size),
            'visualizer': args.v}
    opt_color = 'cyan2'
    for k,v in opts1.items():
        print(color(opt_color, k), color_yes_no(v))

    opts2 = {'heuristic function': args.f,
            'puzzle size': str(size),
            'solution type': args.s,
            'initial state': str(puzzle),
            'final state': str(solved)}
    for k,v in opts2.items():
        print(color(opt_color, k), v)





    '''
    opt_values = [args.g, args.u, is_solvable(puzzle, solved, size), args.v]
    

    option_color = 'cyan'
    print(color
    greedy search: YES/NO
    uniform cost search: YES/NO
    solvable: YES/NO
    visualizer: YES/NO
    solution type
    initial state
    final state
    heuristic
    '''

if __name__ == '__main__':
    data = parser.get_input()
    if not data:
        sys.exit()
        
    puzzle, size, args = data
    solved = solved_states.KV[args.s](size)

    verbose_info(args, puzzle, solved, size)

    if not is_solvable(puzzle, solved, size):
        print(color('red','this puzzle is not solvable'))
        sys.exit(0)

    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    HEURISTIC = heuristics.KV[args.f]
    if args.u:
        HEURISTIC = heuristics.uniform_cost

    t_start = perf_counter()
    m_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    res = a_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST)
    m_delta = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - m_start
    t_delta = perf_counter() - t_start

    success, steps, queue, open_set, closed_set = res
    print(color('yellow','search duration') + ' %.4f second(s)' % (t_delta))
    fmt = color('yellow','%d evaluated nodes %.8f second(s) per node')
    print(fmt % (len(closed_set), t_delta / max(len(closed_set),1) ))
    print(color('yellow','memory usage') + ' %d bytes' % (m_delta))
    if success:
        print(color('green','length of solution'), len(steps))
        for s in steps:
            print(s)
    else:
        print(color('red','solution not found'))
    print(color('magenta','current open set'), len(open_set))
    print(color('magenta','current queue size'), len(queue))
    print(color('magenta','closed set count'), len(closed_set))
    if success and args.v:
        visualizer(steps, size)

