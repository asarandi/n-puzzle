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

    def count_conflicts(tj, c_row, s_row):
        if tj not in s_row:
            return 0
        if not tj:
            return 0
        c_idx = c_row.index(tj)
        s_idx = s_row.index(tj)
        if c_idx == s_idx:
            return 0
        conflicts = 0
        if c_idx < s_idx:
            c_idx += 1
            while c_idx <= s_idx:
                if c_row[c_idx] in s_row and c_row[c_idx] != 0:
                    conflicts += 1
                c_idx += 1
        elif c_idx > s_idx:
            c_idx -= 1
            while c_idx >= s_idx:
                if c_row[c_idx] in s_row and c_row[c_idx] != 0:
                    conflicts += 1
                c_idx -= 1
        return conflicts

    res = manhattan(candidate, solved, size)                            # XXX
    candidate_rows = [[] for y in range(size)] 
    candidate_columns = [[] for x in range(size)] 
    solved_rows = [[] for y in range(size)] 
    solved_columns = [[] for x in range(size)] 
    for y in range(size):
        for x in range(size):
            idx = y * size + x
            candidate_rows[y].append(candidate[y * size + x])
            candidate_columns[x].append(candidate[y * size + x])
            solved_rows[y].append(solved[y * size + x])
            solved_columns[x].append(solved[y * size + x])
    for i in range(size):
        for t in candidate_rows[i]:
            res += count_conflicts(t, candidate_rows[i], solved_rows[i])
    for i in range(size):
        for t in candidate_columns[i]:
            res += count_conflicts(t, candidate_columns[i], solved_columns[i])
    return res

KV = {
        'hamming':      hamming,
        'gaschnig':     gaschnig,
        'manhattan':    manhattan,
        'conflicts':    linear_conflicts
        }

#
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
