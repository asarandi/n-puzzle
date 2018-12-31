#!/usr/bin/env python3

import sys
import os
from copy import deepcopy
from time import sleep
from tkinter import *
#from operator import itemgetter
from heapq import heappush, heappop, heapify

GUI_FONT = ('Arial', 36)
GUI_BOX_SIZE = 100
GUI_BOX_SPACING = 10
GUI_BOX_BORDER_WIDTH = 3
GUI_FRAME_INDEX = 0
GUI_DELAY = 500
GUI_COLOR_1 = '#f5f5dc'
GUI_COLOR_2 = '#e9e9af'
GUI_COLOR_3 = '#dddd88'
GUI_OUTLINE_1 = '#ff0000'
GUI_OUTLINE_2 = '#00ff00'
GUI_OUTLINE_3 = '#0000ff'

def gui_replay(master, canvas, item_matrix, solution, puzzle_size):
    global GUI_FRAME_INDEX

    numbers = solution[GUI_FRAME_INDEX].data
    next_zero = None
    color_this = None
    if GUI_FRAME_INDEX + 1 < len(solution):
        next_zero = solution[GUI_FRAME_INDEX + 1].data.index(0)
        color_this = solution[GUI_FRAME_INDEX].data[next_zero]
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            n = numbers[y+puzzle_size*x]
            BORDER_COLOR = "#000000"
            if n == solution[-1].data[y+puzzle_size*x]:
                BORDER_COLOR = "#00bb00"    #if number is in place, show green cell border
            else:
                BORDER_COLOR = "#bb0000"    #else red cell border

            if n == 0:
                canvas.itemconfig(item_matrix[y][x][0],  outline=GUI_COLOR_1, width=GUI_BOX_BORDER_WIDTH)
            elif n == color_this:
                canvas.itemconfig(item_matrix[y][x][0],  outline=BORDER_COLOR, width=GUI_BOX_BORDER_WIDTH)
            else:
                canvas.itemconfig(item_matrix[y][x][0],  outline=BORDER_COLOR, width=GUI_BOX_BORDER_WIDTH)

            s = str(n)
            if not n:
                s = ''
            canvas.itemconfig(item_matrix[y][x][1], text=s)

    GUI_FRAME_INDEX += 1
    if GUI_FRAME_INDEX >= len(solution):
        GUI_FRAME_INDEX = 0
    canvas.update()

    if GUI_FRAME_INDEX != 0:
        master.after(GUI_DELAY, gui_replay, master, canvas, item_matrix, solution, puzzle_size)

def gui_close(event):
    print(event)
    sys.exit(0)

def gui_item_matrix(canvas, puzzle_size):
    item_matrix = [[[None, None] for x in range(puzzle_size)] for y in range(puzzle_size)]
    for y in range(puzzle_size):
        for x in range(puzzle_size):
            y0 = y * GUI_BOX_SIZE + GUI_BOX_SPACING
            x0 = x * GUI_BOX_SIZE + GUI_BOX_SPACING

            item_matrix[y][x][0] = canvas.create_rectangle(y0,x0,y0+GUI_BOX_SIZE-GUI_BOX_SPACING,x0+GUI_BOX_SIZE-GUI_BOX_SPACING,
                    dash=(5,4,5,3),
                    fill=GUI_COLOR_1)
            item_matrix[y][x][1] = canvas.create_text(
                    (
                        y0 + (GUI_BOX_SIZE - GUI_BOX_SPACING) / 2,
                        x0 + (GUI_BOX_SIZE - GUI_BOX_SPACING) / 2
                        ),
                    font=GUI_FONT,
                    text=''
                    )

    return item_matrix

def visualizer(solution, puzzle_size):
    master = Tk()
    canvas_width = (GUI_BOX_SIZE * puzzle_size) + GUI_BOX_SPACING
    canvas_height = (GUI_BOX_SIZE * puzzle_size) + GUI_BOX_SPACING
    canvas = Canvas(master, width=canvas_width+1, height=canvas_height+1, bg=GUI_COLOR_1, borderwidth=0, highlightthickness=0)
    canvas.pack()
    item_matrix = gui_item_matrix(canvas, puzzle_size)
    os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    master.bind('<Escape>', gui_close)
    master.bind('<Q>', gui_close)
    master.bind('<q>', gui_close)
    master.after(0, gui_replay, master, canvas, item_matrix, solution, puzzle_size)
    master.mainloop()



def error_exit(msg):
    print(msg)
    sys.exit(1)  

def validate_size(data):
    if len(data[0]) != 1:
        error_exit('invalid input')                                                 #first list[] in data must be size of matrix
    size = data.pop(0)[0]
    if size < 2:                                                                    # too small?
        error_exit('invalid input')
    if len(data) != size:                                                           # data[] should be an array of size N lists[]
        error_exit('invalid input')
    for line in data:                                                               # each list[] must be of size N (data must be square matrix)
        if len(line) != size:
            error_exit('invalid input')
    expanded = []
    for line in data:
        for x in line:
            expanded.append(x)
    generated = [x for x in range(size**2)]
    difference = [x for x in generated if x not in expanded]
    if len(difference) != 0:
        error_exit('invalid input')
    return size


def clone_and_swap(data,y0,y1):
    clone = deepcopy(list(data))
    tmp = clone[y0]
    clone[y0] = clone[y1]
    clone[y1] = tmp
    return tuple(clone)


def possible_moves(data, size):
    res = []
    y = data.index(0)
#    for y in range(len(data)):
#            if data[y] == 0:
    if y % size > 0:
        left = clone_and_swap(data,y,y-1)
        res.append(left)
    if (y % size) + 1 < size:
        right = clone_and_swap(data,y,y+1)
        res.append(right)
    if y - size >= 0:
        up = clone_and_swap(data,y,y-size)
        res.append(up)
    if y + size < len(data):
        down = clone_and_swap(data,y,y+size)
        res.append(down)
    return res
                

def seen_before(move, node_lst):
    for node in node_lst:
        if node.data == move:
            return True
    return False


def heuristic_tiles_out_of_place(candidate, solved):
    res = 0
    for y in range(len(solved)):
            if solved[y] != candidate[y]:
                res += 1
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

#
# https://lyfat.wordpress.com/2012/05/22/euclidean-vs-chebyshev-vs-manhattan-distance/
#

def chebyshev_distance(y0,x0,y1,x1):
    return max(abs(y0-y1), abs(x0-x1))

def manhattan_distance(y0,x0,y1,x1):
    return abs(y0-y1) + abs(x0-x1)

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
                res += manhattan_distance(y,x,y1,x1)
#                res += euclidean_distance(y,x,y1,x1)
#                res += chebyshev_distance(y,x,y1,x1)
    return res



NODE_MAX_SCORE = 999999
def select_by_f_score(lst):
#    lst = sorted(lst, key=lambda x: x.n, reverse=True)
    lst = sorted(lst, key=lambda x: x.f)
    return lst[0]

#    res = None
#    res_f = NODE_MAX_SCORE 
#    for e in lst:
#        if e.f < res_f:
#            res = e
#            res_f = e.f
#    return res


def find_node_by_data(data, nodes):
    for node in nodes:
        if node.data == data:
            return node
    return None

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.f = NODE_MAX_SCORE
        self.g = NODE_MAX_SCORE
        self.h = NODE_MAX_SCORE
        self.n = -1


def solved_zero_first(size):
    return tuple([x for x in range(size*size)])

def solved_zero_last(size):
    lst = [x for x in range(1,size*size)]
    return tuple(lst.append(0))

def solved_snail(size):
    lst = [[0 for x in range(size)] for y in range(size)]
    moves = [(0,1),(1,0),(0,-1),(-1,0)]
    row = 0
    col = 0
    i = 1
    final = size * size
    size -= 1
    done = False
    while not done and size > 0:
        for move in moves:
            if done:
                break
            for _ in range(size):
                lst[row][col] = i
                row += move[0]
                col += move[1]
                i += 1
                if i == final:
                    done = True
                    break
        row += 1
        col += 1
        size -= 2

    res = []
    for row in lst:
        for i in row:
            res.append(i)
    return tuple(res)


fn = 'input0.txt'
if len(sys.argv) > 1:
    fn = sys.argv[1]
    
with open(fn) as f:
    data = f.read().splitlines()
    f.close()

data = [line.split('#')[0] for line in data]                                        #remove comments
data = [line for line in data if len(line) > 0]                                     #remove empty lines
data = [[int(x) for x in line.split(' ') if len(x) > 0] for line in data]           #convert to ints

size = validate_size(data)
flat = []
for line in data:
    for itm in line:
        flat.append(itm)
data = tuple(flat)
print('initial state', data)
original = deepcopy(data)


'''
#solved = [int(x) for x in range(size*size)]
#solved[size*size-1] = 0
solved_3 = [1,2,3,8,0,4,7,6,5]
solved_4 = [1,2,3,4,12,13,14,5,11,0,15,6,10,9,8,7]
solved_5 = [1,2,3,4,5,16,17,18,19,6,15,24,0,20,7,14,23,22,21,8,13,12,11,10,9]
if size == 3: solved = solved_3
elif size == 4: solved = solved_4
elif size == 5: solved = solved_5
else: sys.exit(0)
solved = tuple(solved)
'''
solved = solved_snail(size)
print('final state', solved)

root = Node(data)
root.f = 0
root.g = 0
root.h = heuristic(root.data, solved, size)
root.n = 1
opened = []
open_set = {}

heappush(opened, (root.f, root.n, root))

#opened.append(root)

open_set[root.data] = root
closed_set = {}
success = False

node_count = 1
closed_count = 0

magic = (5, 4, 1, 12, 3, 2, 13, 14, 0, 10, 15, 6, 11, 7, 9, 8)

while opened and not success:
#    print(opened)
    f_score, n_score, e = heappop(opened) #select_by_f_score(opened)
    try:
        del open_set[e.data]
    except:
        print('exception',e.data)
        for keys in open_set:
            print('openset', keys)
        print()
        for keys in closed_set:
            print('closedset', keys)
        print()
        sys.exit(0)


    if e.data == solved:
        success = True
        print('success')
        steps = []
        print('current g value', e.g)
        while True:
            steps.append(e)
            if not e.parent:
                break
            e = e.parent
        steps = list(reversed(steps))
        print('length of solution', len(steps))
        for s in steps:
            print(s.data, 'g value', s.g, 'h value', s.h, 'f value', s.f, 'n value', s.n)
        print('current open set', len(open_set))
#        print('total open set count', open_count)
        print('closed set count', len(closed_set))
#        visualizer(steps, size)
        break
    else:

        closed_set[e.data] = e
        closed_count += 1
        moves = possible_moves(e.data, size)
        for m in moves:
            tentative_g = e.g + 1
            if m in closed_set:             #node exists in closed set
                continue
                n = closed_set[m]
                if tentative_g >= n.g:
                    continue
                open_set[m] = n
                del closed_set[m]
                closed_count -= 1
            elif m in open_set:             #node exists in open set
                n = open_set[m]
                if tentative_g >= n.g:
                    continue
                opened.remove((n.f, n.n, n))
                heapify(opened)
            else:
                n = Node(m)                 # create new node
                node_count += 1
                n.n = node_count
                n.h = heuristic(n.data, solved, size)
                open_set[m] = n             # and put it in open set

            n.parent = e
            n.g = tentative_g         
            n.f = n.g + n.h
            heappush(opened, (n.f, n.n, n))
