import pickle
from npuzzle import solved_states

def pattern_only(node, pattern):
    lst = list(node)
    for i, val in enumerate(lst):
        if val not in pattern:
            lst[i] = -1
    return tuple(lst)

files = [
    '4x4-zero_last.1_2_5_9_13.pdb',
    '4x4-zero_last.3_6_10_14_15.pdb',
    '4x4-zero_last.4_7_8_11_12.pdb',
    ]

patterns = [        
        [1,2,5,9,13],
        [3,6,10,14,15],
        [4,7,8,11,12]
        ]

databases = []

for f in files:
    databases.append(pickle.load(open(f, 'rb')))


def patterns_db(candidate, solved, size):
    if solved != solved_states.zero_last(4):
        return 0
    result = 0
    for i, pat in enumerate(patterns):
        result += databases[i][pattern_only(candidate, pat)]
    return result

