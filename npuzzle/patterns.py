from npuzzle import solved_states
import sqlite3

files = [
        '1_5_6_9_10_13.sqlite3.pdb',
        '7_8_11_12_14_15.sqlite3.pdb',
        '2_3_4.sqlite3.pdb'
        ]

patterns = [
        (1,5,6,9,10,13),
        (7,8,11,12,14,15),
        (2,3,4)
        ]

connections = []
cursors = []

for idx, fn in enumerate(files):
    conn = sqlite3.connect(fn)
    connections.append(conn)
    c = conn.cursor()
    cursors.append(c)

def patterns_db(candidate, solved, size):
    if solved != solved_states.zero_last(4):
        return 0
    result = 0
    for i, pat in enumerate(patterns):
        sql_key = 0
        for p in pat:
            sql_key <<= 4
            sql_key += candidate.index(p)
        cursors[i].execute('SELECT value FROM kv WHERE key=?;', (sql_key,))
        result += cursors[i].fetchone()[0]
    return result

