import mmap
from npuzzle import solved_states
import sys

def pattern_only(node, pattern, filler):
    lst = list(node)
    for i, val in enumerate(lst):
        if val not in pattern:
            lst[i] = filler
    return tuple(lst)

def node_to_bytes(node):
    b = bytearray()
    i = 0
    while i < len(node):
        b.append((node[i] << 4) + node[i+1])
        i += 2
    return bytes(b)

def bytes_to_node(b):
    lst = []
    for i in b:
        lst.append(i >> 4)
        lst.append(i & 15)
    return tuple(lst)

def database_get(node, database):
#    print('database_get(); node = ', node)
    RECORD_SIZE = 9
    NUM_RECORDS = len(database) // RECORD_SIZE
#    print(RECORD_SIZE, NUM_RECORDS, len(database))
    b = node_to_bytes(node)
#    print(b)
    idx = (hash(b) % NUM_RECORDS) * RECORD_SIZE
    idx = 0
    while True:
        rec = database[idx:idx + 8]
#        print('rec', rec)
#        if sum(rec) == 0:
#            return None
        if rec == b:
            return int(database[idx+8])
        idx += RECORD_SIZE
        if idx >= len(database):
            return None

files = [
    '(1, 5, 6, 9, 10, 13).pdb',
    '(7, 8, 11, 12, 14, 15).pdb',
    '(2, 3, 4).pdb'
    ]

patterns = [
        (1,5,6,9,10,13),
        (7,8,11,12,14,15),
        (2,3,4)
        ]

fillers = [
        2,
        2,
        1
        ]

databases = []

for fn in files:
    with open(fn, 'rb') as fp:
        m = mmap.mmap(fp.fileno(), 0, prot=mmap.PROT_READ)
        i = 0
        d = {}
        while i < len(m):
            rec = m[i:i+8]
            val = m[i+8]
            if sum(rec) != 0:
                d[bytes_to_node(rec)] = val
            i += 9
        print('database loaded:', fn, len(d), 'records, size = ', sys.getsizeof(d))


        databases.append(d)
        m.close()
        fp.close()

print('total size in memory', sys.getsizeof(databases))

def patterns_db(candidate, solved, size):
    if solved != solved_states.zero_last(4):
        return 0
    result = 0
    for i, pat in enumerate(patterns):
        node = pattern_only(candidate, patterns[i], fillers[i])
        r = databases[i][node]
        if r == None:
            print('this shouldnt happen')
        result += r
    return result

