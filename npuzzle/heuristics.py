#from os import path as os_path
#from os import stat as os_stat
from npuzzle import solved_states
from npuzzle.patterns import patterns_db


def patterns(puzzle, solved, size):
    if size != 4:
        return 0
    return patterns_db(puzzle, solved, size)

#    query = bytearray()
#    if solved == solved_states.KV['snail'](size):
#        query.append(0)
#    elif solved == solved_states.KV['zero_first'](size):
#        query.append(1)
#    elif solved == solved_states.KV['zero_last'](size):
#        query.append(2)
#    else:
#        return 0
#    i = 0
#    while i < len(puzzle):
#        b = puzzle[i] << 4
#        b += puzzle[i+1]
#        query.append(b)
#        i += 2
#
#    with open('pdb_server_in', 'wb') as fpi:
#        fpi.write(query)
#        fpi.close()
#    while True:
#        with open('pdb_server_out', 'rb') as fpo:
#            result = fpo.read()
#            if len(result) != 0:
#                break
#            fpo.close()
#            
#    if result[1:] == query[1:]:
#        return result[0]
#    else:
#        print('patterns heuristic error, this shouldnt happend')
#        return 0

def uniform_cost(puzzle, solved, size):
    return 0

def hamming(candidate, solved, size): #aka tiles out of place
    res = 0
    for i in range(size*size):
        if candidate[i] != 0 and candidate[i] != solved[i]:
            res += 1
    return res

def gaschnig(candidate, solved, size):
    res = 0
    candidate = list(candidate)
    solved = list(solved)
    while candidate != solved:
        zi = candidate.index(0)
        if solved[zi] != 0:
            sv = solved[zi]
            ci = candidate.index(sv)
            candidate[ci], candidate[zi] = candidate[zi], candidate[ci]
        else:
            for i in range(size * size):
                if solved[i] != candidate[i]:
                    candidate[i], candidate[zi] = candidate[zi], candidate[i]
                    break
        res += 1
    return res

def manhattan(candidate, solved, size):
    res = 0
    for i in range(size*size):
        if candidate[i] != 0 and candidate[i] != solved[i]:
            ci = solved.index(candidate[i])
            y = (i // size) - (ci // size)
            x = (i % size) - (ci % size)
            res += abs(y) + abs(x)
    return res

def linear_conflicts(candidate, solved, size):

    def count_conflicts(candidate_row, solved_row, size, ans=0):
        counts = [0 for x in range(size)]
        for i, tile_1 in enumerate(candidate_row):
            if tile_1 in solved_row and tile_1 != 0:
                for j, tile_2 in enumerate(candidate_row):
                    if tile_2 in solved_row and tile_2 != 0:
                        if tile_1 != tile_2:
                            if (solved_row.index(tile_1) > solved_row.index(tile_2)) and i < j:
                                counts[i] += 1
                            if (solved_row.index(tile_1) < solved_row.index(tile_2)) and i > j:
                                counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            candidate_row[i] = -1
            ans += 1
            return count_conflicts(candidate_row, solved_row, size, ans)

    res = manhattan(candidate, solved, size)
    candidate_rows = [[] for y in range(size)] 
    candidate_columns = [[] for x in range(size)] 
    solved_rows = [[] for y in range(size)] 
    solved_columns = [[] for x in range(size)] 
    for y in range(size):
        for x in range(size):
            idx = (y * size) + x
            candidate_rows[y].append(candidate[idx])
            candidate_columns[x].append(candidate[idx])
            solved_rows[y].append(solved[idx])
            solved_columns[x].append(solved[idx])
    for i in range(size):
            res += count_conflicts(candidate_rows[i], solved_rows[i], size)
    for i in range(size):
            res += count_conflicts(candidate_columns[i], solved_columns[i], size)
    return res

KV = {
        'hamming':      hamming,
        'gaschnig':     gaschnig,
        'manhattan':    manhattan,
        'conflicts':    linear_conflicts,
        'patterns':     patterns
        }


# if there is a readable pipe called 'pdb_server_in', then
# add 'patterns' string and patterns() function to available heuristics list


#if os_path.exists('pdb_server_in'):
#    if os_stat('pdb_server_in').st_mode & 0o10400:   #readable fifo pipe
#        KV['patterns'] = patterns


#KV = {
#        'hamming':      hamming,
#        'gaschnig':     gaschnig,
#        'manhattan':    manhattan,
#        'conflicts':    linear_conflicts,
#        'misplaced':    misplaced,
#        'suminv':       suminv,
#        'chebyshev':    chebyshev,
#        'euclidean':    euclidean,
#        'euclidean2':   euclidean2
#        }
#
#def euclidean(candidate, solved, size):
#    res = 0
#    for i in range(size*size):
#        if candidate[i] != 0 and candidate[i] != solved[i]:
#            ci = solved.index(candidate[i])
#            y = (i // size) - (ci // size)
#            x = (i % size) - (ci % size)
#            res += sqrt((y*y) + (x*x))
#    return res
#
#def euclidean2(candidate, solved, size):      #not admissible, over estimates
#    res = 0
#    for i in range(size*size):
#        if candidate[i] != 0 and candidate[i] != solved[i]:
#            ci = solved.index(candidate[i])
#            y = (i // size) - (ci // size)
#            x = (i % size) - (ci % size)
#            res += (y*y) + (x*x)
#    return res
#
#def misplaced(candidate, solved, size):     #aka misplaced rows and columns
#    res = 0   
#    for i in range(size*size):
#        if candidate[i] != 0 and candidate[i] != solved[i]:
#            ci = solved.index(candidate[i])
#            if ci // size != i // size:
#                res += 1
#            if ci % size != i % size:
#                res += 1
#    return res
#
#
#def suminv(candidate, solved, size):  #sum inversion, not admissible, over estimates
#    res = 0
#    for i in range(size * size - 1):
#        if candidate[i]:
#            si = solved.index(candidate[i])
#            leftside = solved[:si]
#            rightside = candidate[i + 1:]
#            for k in rightside:
#                if k != 0 and k in leftside:
#                    res += 1
#    return res
#
#def chebyshev(candidate, solved, size):       #not admissible
#    res = 0
#    for i in range(size*size):
#        if candidate[i] != 0 and candidate[i] != solved[i]:
#            ci = solved.index(candidate[i])
#            y = (i // size) - (ci // size)
#            x = (i % size) - (ci % size)
#            res += max(abs(y), abs(x))
#    return res
