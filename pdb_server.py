#!/usr/bin/env pypy3
import os
import pickle

pdb_folder = 'PDB/'
dictionaries = {}
for f in os.listdir(pdb_folder):
    sp = f.split('.')
    if sp[0] not in dictionaries:
        dictionaries[sp[0]] = {}
    pattern = []
    for x in sp[1][1:-1].split(','):
        pattern.append(int(x))
    fn = pdb_folder + f
    print('loading', fn)
    db = pickle.load(open(fn, 'rb'))
    dictionaries[sp[0]][tuple(pattern)] = db

print('ready')
mapping = {0:'snail', 1:'zero_first', 2:'zero_last'}

fifo_in = 'pdb_server_in'
fifo_out = 'pdb_server_out'

if not os.path.exists(fifo_in):
    os.mkfifo(fifo_in)
if not os.path.exists(fifo_out):
    os.mkfifo(fifo_out)
    
while True:
#    print('pdb server listening for queries ..')
    with open(fifo_in, 'rb') as server_input:
        while True:
            data = server_input.read()
            if len(data) == 0:
#                print('client closed')
                break
            if len(data) != 9:
#                print('error: expecting data of length 9')
                break
#            print('received query', data)
            db_key = data[0]
            node = []
            for b in data[1:]:
                node.append(b >> 4)
                node.append(b & 15)
#            print(node)
            puzzle_type = mapping[db_key]
#            print(puzzle_type)
            result = 0
            for pattern, hashtable in dictionaries[puzzle_type].items():
                key = 0
                for p in pattern:
                    key <<= 4
                    key += node.index(p)
                result += hashtable[key]
            data = bytearray(data)
            data[0] = result    #reuse, so client can confirm
            with open(fifo_out, 'wb') as server_output:
                server_output.write(data)
                server_output.close()




