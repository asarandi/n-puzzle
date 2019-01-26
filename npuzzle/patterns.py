from npuzzle import solved_states
import pickle

files = [      
    '1_5_6_9_10_13.pickled.dict.pdb',
    '7_8_11_12_14_15.pickled.dict.pdb',
    '2_3_4.pickled.dict.pdb'
    ]

patterns = [
        (1,5,6,9,10,13),
        (7,8,11,12,14,15),
        (2,3,4)
        ]

dictionaries = []

for fn in files:
    dictionaries.append(pickle.load(open(fn, 'rb')))
    print('pickle loaded:', fn)

def patterns_db(candidate, solved, size):
    if solved != solved_states.zero_last(4):
        return 0
    result = 0
    for i, pat in enumerate(patterns):
        key = 0
        for p in pat:
            key <<= 4
            key += candidate.index(p)
        result += dictionaries[i][key]
    return result

