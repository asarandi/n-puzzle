#!/usr/bin/env python3

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


for i in range(13):
    print(solved_snail(i))
    print()
