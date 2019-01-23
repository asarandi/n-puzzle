#!/usr/bin/env pypy3

import argparse
from npuzzle import solved_states


parser = argparse.ArgumentParser(description='pdbgen for n-puzzle solver')
parser.add_argument('solution', help='solved state', choices=list(solved_states.KV.keys()))
args = parser.parse_args()


PUZZLE_SIZE = 4

'''
https://algorithmsinsight.files.wordpress.com/2016/04/6-6-3.jpg



1 2            3 4
5            6             7 8
9            a             b c
d            e             f -


1 2                       3 4
5                       6 7 8
9           a b c
d           e f -


1 2 3 4
c d e 5
b - f 6
a 9 8 7



zero_last 4x4,    6-6-3  pattern groups

[green]     [blue]     [red]
1                      2 3 4
5 6           7 8
9 a           b c
d           e f -


1 2 3 4 5 6 7 8 9 a b c d e f 0
y 0 0 0 1 1 0 0 1 1 0 0 1 0 0 0     green   [1,5,6,9,10,13]
0 0 0 0 0 0 1 1 0 0 1 1 0 1 1 0     blue    [7,8,11,12,14,15]
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0     red     [2,3,4]



'''
print(solved_states.KV[args.solution](PUZZLE_SIZE))

green = [1,5,6,9,10,13]
blue =  [7,8,11,12,14,15]
red =   [2,3,4]

initial_board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
initial_green = [1,0,0,0,5,6,0,0,9,10, 0, 0,13, 0, 0,0]

