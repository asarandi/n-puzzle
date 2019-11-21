#include "npuzzle.h"

static int  count_conflicts(int candidate, int solved, int res)
{
    int i, j, ti, tj;
    int f, k, counts[4];

    for (i=0; i<4; i++)
        counts[i] = 0;
    for (i=0; i<4; i++)
    {
        if (!(k = (candidate >> ((3 - i) << 2)) & 15)) continue ;
        for (ti=f=0; ti<4; ti++)
            if ((f = (k == ((solved >> ((3 - ti) << 2)) & 15)))) break ;
        if (!f) continue ;
        for (j=0; j<4; j++)
        {
            if (i==j) continue ;
            if (!(k = (candidate >> ((3 - j) << 2)) & 15)) continue ;
            for (tj=f=0; tj<4; tj++)
                if ((f = (k == ((solved >> ((3 - tj) << 2)) & 15)))) break ;
            if (!f) continue ;
            counts[i] += ((i > j) && (ti < tj));
            counts[i] += ((i < j) && (ti > tj));
        }
    }
    for (i=k=0; i<4; i++)
        k = counts[i] > k ? counts[i] : k;
    if (!k) return (res << 1);
    for (i=0; i<4; i++)
        if (counts[i] == k) break;
    candidate &= ~(15 << ((3 - i) << 2));
    return count_conflicts(candidate, solved, ++res);
}

static int linear_conflicts(uint64_t x)
{
    int i, j, c, s, res;

    for (i=res=0; i<4; i++)
    {
        c = (int)((x >> ((3 - i) << 4)) & 0xffff);
        s = (int)((GOAL_STATE >> ((3 - i) << 4)) & 0xffff);
        res += count_conflicts(c, s, 0);
        for (j=c=s=0; j<4; j++)
        {
            c = (c << 4) | ((x >> (60 - ((i + (j << 2)) << 2))) & 15);
            s = (s << 4) | ((GOAL_STATE >> (60 - ((i + (j << 2)) << 2))) & 15);
        }
        res += count_conflicts(c, s, 0);
    }
    return res;
}

static int manhattan_distance(uint64_t x)
{
    int i, j, nibble, res;

    for (i=res=0; i<16; i++)
    {
        nibble = (x >> ((15 - i) << 2)) & 15;
        if (!nibble)
            continue;
        j = nibble - 1;
        res += ABS((i >> 2) - (j >> 2)) + ABS((i & 3) - (j & 3));
    }
    return res;
}

int heuristic(uint64_t x)
{
    return manhattan_distance(x) + linear_conflicts(x);
}
