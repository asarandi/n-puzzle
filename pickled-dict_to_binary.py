#!/usr/bin/env python3
import pickle

input_files = [
    '(1, 5, 6, 9, 10, 13).4x4_zerolast.pickled.dict.pdb',
    '(7, 8, 11, 12, 14, 15).4x4_zerolast.pickled.dict.pdb',
    '(2, 3, 4).4x4_zerolast.pickled.dict.pdb'
    ]


output_files = [
    '(1, 5, 6, 9, 10, 13).4x4_zerolast.binary.pdb',
    '(7, 8, 11, 12, 14, 15).4x4_zerolast.binary.pdb',
    '(2, 3, 4).4x4_zerolast.binary.pdb'
    ]

for i, fn in enumerate(input_files):
    d = pickle.load(open(fn, 'rb'))
    print('loaded', fn)
    with open(output_files[i], 'wb') as fp:
        for k,v in d.items():
            k <<= 8
            k += v
            b = k.to_bytes(4, byteorder='big')
            fp.write(b)
        fp.close()
    print('wrote', output_files[i])


