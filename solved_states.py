def zero_first(size):
    return tuple([x for x in range(size*size)])

def zero_last(size):
    lst = [x for x in range(1,size*size)]
    lst.append(0)
    return tuple(lst)

def snail(size):
    lst = [[0 for x in range(size)] for y in range(size)]
    moves = [(0,1),(1,0),(0,-1),(-1,0)]
    row = 0
    col = 0
    i = 1
    final = size * size
    size -= 1
    while i is not final and size > 0:
        for move in moves:
            if i is final: break
            for _ in range(size):
                lst[row][col] = i
                row += move[0]
                col += move[1]
                i += 1
                if i is final: break
        row += 1
        col += 1
        size -= 2
    res = []
    for row in lst:
        for i in row:
            res.append(i)
    return tuple(res)

KV = {
    'zero_first':   zero_first,
    'zero_last':    zero_last,
    'snail':        snail
}
