from npuzzle import solved_states
import pickle

#files = ['PDB/snail.[1,12,11,10,9,8].pdb', 'PDB/snail.[13,14,15].pdb', 'PDB/snail.[2,3,4,5,6,7].pdb']
#files = ['PDB/zero_first.[1,2,3,7,11,15].pdb', 'PDB/zero_first.[4,5,6,9,10,14].pdb', 'PDB/zero_first.[8,12,13].pdb']
#files = ['PDB/zero_last.[1,5,6,9,10,13].pdb','PDB/zero_last.[2,3,4].pdb','PDB/zero_last.[7,8,11,12,14,15].pdb']

files = ['PDB771/zero_last.[1,5,6,9,10,13,14].pdb', 'PDB771/zero_last.[3,4,7,8,11,12,15].pdb', 'PDB771/zero_last.[2].pdb']

ENABLED = True

dictionaries = {}

if ENABLED:
    for f in files:
        sp = f.split('.')
        pattern = []
        for x in sp[1][1:-1].split(','):
            pattern.append(int(x))
        db = pickle.load(open(f, 'rb'))
        dictionaries[tuple(pattern)] = db
        print('pickle loaded:', f)

def patterns_db(candidate, solved, size):
    result = 0
    if not ENABLED:
        return result
    for pattern in dictionaries:
        key = 0
        for p in pattern:
            key <<= 4
            key += candidate.index(p)
        result += dictionaries[pattern][key]
    return result

