#!/usr/bin/env python3
import mmap
import pickle

input_files = [
    '(1, 5, 6, 9, 10, 13).4x4_zerolast.binary.pdb',
    '(7, 8, 11, 12, 14, 15).4x4_zerolast.binary.pdb',
    '(2, 3, 4).4x4_zerolast.binary.pdb'
]

for i, fn in enumerate(input_files):
    d = {}
    with open(fn, 'rb') as fp:
        m = mmap.mmap(fp.fileno(), 0, prot=mmap.PROT_READ)
        i = 0
        while i < len(m):
            k = int.from_bytes(m[i:i+3], byteorder='big', signed=False)
            v = int(m[i+3])
            d[k] = v
            i += 4
        m.close()
        fp.close()
        print('done with', fn)
        pickle.dump(d, open(fn + '.dict', 'wb'))
