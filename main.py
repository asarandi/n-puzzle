#!/usr/bin/env python3

import sys
import resource
from time import perf_counter
from npuzzle.visualizer import visualizer
from npuzzle.search import a_star_search, ida_star_search
from npuzzle.is_solvable import is_solvable
from npuzzle import colors
from npuzzle.colors import color
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import solved_states

def pretty_print_steps(steps, size):
    width = len(str(size*size))
    decor = '-'
    for n in range(len(steps)):
        if n == 0:
            print('-[initial state]%s' % (4*decor,))
        else:
            print('-[step %2d]%s' % (n,10*decor,))    
        print()
        for i in range(size):
            for j in range(size):
                tile = str(steps[n][i*size+j])
                if tile == '0':
                    tile = color('red2', '-'*width)
                print(' %*s' % (width, tile), end='')
            print()
        print()
    print('%s' % (20*decor,))


def color_yes_no(v):
    return color('green', 'YES') if v else color('red', 'NO')

def verbose_info(args, puzzle, solved, size):
    opts1 = {'greedy search:': args.g,
            'uniform cost search:': args.u,
            'visualizer:': args.v,
            'solvable:': is_solvable(puzzle, solved, size)
            }
    opt_color = 'cyan2'
    for k,v in opts1.items():
        print(color(opt_color, k), color_yes_no(v))

    opts2 = {'heuristic function:': color('green2', args.f),
            'puzzle size:': str(size),
            'solution type:': color('green2', args.s),
            'initial state:': str(puzzle),
            'final state:': str(solved)}
    for k,v in opts2.items():
        print(color(opt_color, k), v)
   
    print(color('blue2', 'heuristic scores for initial state'))
    for k,v in heuristics.KV.items():
        print(color('blue2', '  - ' + k + '\t:'), v(puzzle, solved, size))

    print(color('red2', 'search algorithm:'), 'IDA*' if args.ida else 'A*')

#########################################################################################

if __name__ == '__main__':
    data = parser.get_input()
    if not data:
        sys.exit()        
    puzzle, size, args = data
    if args.c:
        colors.enabled = True

    if args.ida:
        args.g = False

    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    HEURISTIC = heuristics.KV[args.f]
    if args.u:
        HEURISTIC = heuristics.uniform_cost

    solved = solved_states.KV[args.s](size)
    verbose_info(args, puzzle, solved, size)
    if not is_solvable(puzzle, solved, size):
        print(color('red','this puzzle is not solvable'))
        sys.exit(0)

    maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(color('red', 'max rss before search:'), maxrss)

    t_start = perf_counter()
    if args.ida:
        res = ida_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST)
    else:
        res = a_star_search(puzzle, solved, size, HEURISTIC, TRANSITION_COST)
    t_delta = perf_counter() - t_start

    maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(color('red', 'max rss after search: '), maxrss)

    print(color('yellow','search duration:') + ' %.4f second(s)' % (t_delta))
    success, steps, complexity = res
    fmt = '%d' + color('yellow',' evaluated nodes, ') + '%.8f' + color('yellow',' second(s) per node')
    print(fmt % (complexity['time'], t_delta / max(complexity['time'],1) ))
    if success:
        print(color('green','length of solution:'), max(len(steps) - 1, 0))
        print(color('green', 'initial state and solution steps:'))
        if args.p:
            pretty_print_steps(steps, size)
        else:
            for s in steps:
                print(s)
    else:
        print(color('red','solution not found'))
    print(color('magenta','space complexity:'), complexity['space'], 'nodes in memory')
    print(color('magenta','time complexity:'), complexity['time'], 'evaluated nodes')
    if success and args.v:
        visualizer(steps, size)

