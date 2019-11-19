#include "npuzzle.h"

static int  count_conflicts(int candidate, int solved, int retval)
{
    int i, ic, is, j, jc, js;
    int f, k, counts[4];

    for (i=0; i<4; i++)
        counts[i] = 0;
    for (i=0; i<4; i++)
    {
        ic = (candidate >> ((3 - i) << 2)) & 15;
        if (!ic) continue ;
        for (is=f=0; is<4 && !f; is++)
            f |= (ic == ((solved >> ((3 - is) << 2)) & 15));
        if (!f) continue ;
        for (j=0; j<4; j++)
        {
            if (i==j) continue ;
            jc = (candidate >> ((3 - j) << 2)) & 15;
            if (!jc) continue ;
            for (js=f=0; js<4 && !f; js++)
                f |= (jc == ((solved >> ((3 - js) << 2)) & 15));
            if (!f) continue ;
            counts[i] += ((i > j) && (is < js));
            counts[i] += ((i < j) && (is > js));
        }
    }
    for (i=k=0; i<4; i++)
        k = counts[i] > k ? counts[i] : k;
    if (!k) return (retval << 1);
    for (i=0; i<4; i++)
        if (counts[i] == k) break;
    candidate &= ~(15 << ((3 - i) << 2));
    return count_conflicts(candidate, solved, ++retval);
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
            c <<= 4;
            c |= ((x >> (60 - ((i + (j << 2) ) << 2))) & 15);
            s <<= 4;
            s |= ((GOAL_STATE >> (60 - ((i + (j << 2)) << 2))) & 15);
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
