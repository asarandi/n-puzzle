#!/usr/bin/env python3
import mmap
import time


# expecting tuple len 16,  will return bytearray of len 8
def node_to_bytes(node):
    b = bytearray()
    i = 0
    while i < len(node):
        b.append((node[i] << 4) + node[i+1])
        i += 2
    return b

#expecting bytearray of len 8, will return tuple len 16
def bytes_to_node(b):
    lst = []
    for i in b:
        lst.append(i >> 4)
        lst.append(i & 15)
    return tuple(lst)


db_size = 5765760 * 9   #51,891,840 fifty one megabytes
db = mmap.mmap(-1, db_size)

visited_size = 57657600 * 9 # 518,918,400   five hundred eighteen megabytes
visited = mmap.mmap(-1, visited_size)



t = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
z = node_to_bytes(t)

db[4:4+8] = z

with open('testdb.pdb', 'wb') as fp:
    fp.write(db)
    fp.close()

print(z)
print(type(z))
y = bytes_to_node(z)
print(type(y))
print(y)

db.close()
visited.close()



