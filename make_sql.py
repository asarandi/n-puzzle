#!/usr/bin/env pypy3
import mmap
import sys
import sqlite3

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

input_files = [
    '(1, 5, 6, 9, 10, 13).pdb',
    '(7, 8, 11, 12, 14, 15).pdb',
    '(2, 3, 4).pdb'
    ]


output_files = [
        '1_5_6_9_10_13.sqlite3.pdb',
        '7_8_11_12_14_15.sqlite3.pdb',
        '2_3_4.sqlite3.pdb'
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




for idx, fn in enumerate(input_files):
    with open(fn, 'rb') as fp:
        m = mmap.mmap(fp.fileno(), 0, prot=mmap.PROT_READ)
        conn = sqlite3.connect(output_files[idx])
        c = conn.cursor()
        c.execute('CREATE TABLE kv (key INT, value INT);');
        i = 0
        while i < len(m):
            rec = m[i:i+8]
            val = m[i+8]
            if sum(rec) != 0:
                node = bytes_to_node(rec)
                sql_key = 0
                for k in patterns[idx]:
                    sql_key <<= 4 
                    sql_key += node.index(k)
                sql_kv = (sql_key, val,)
                c.execute('INSERT INTO kv VALUES (?,?);', sql_kv)
            i += 9

        conn.commit()
        conn.close()
        m.close()
        fp.close()
        print('done with', fn)


