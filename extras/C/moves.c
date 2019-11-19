#include "npuzzle.h"

static int clone_counter;

int get_zero_index(uint64_t x)
{
    int i;

    for (i=0; i<16; i++)
    {
        if (!(x & (15L << (i << 2))))
            return (15 - i);
    }
    return -1;
}

t_vertex **make_moves(t_vertex *v)
{
    int                 i, j;
    static t_vertex     *res[4];
    static uint64_t     x, moves[4];

    for (i=0; i<4; i++)
    {
        res[i] = NULL;
        moves[i] = 0;
    }

    x = v->puzzle;
    i = get_zero_index(x);

    moves[0] = i > 3 ? UP(x, i) : 0;
    moves[1] = i < 12 ? DOWN(x , i) : 0;
    moves[2] = (i & 3) != 3 ? RIGHT(x , i) : 0;
    moves[3] = i & 3 ? LEFT(x , i) : 0;

    for (i=j=0; i<4; i++)
    {
        if ((moves[i]) && (moves[i] != v->parent))
        {
            res[j] = calloc(1, sizeof(t_vertex));
            res[j]->puzzle = moves[i];
            res[j]->parent = v->puzzle;
            res[j++]->counter = ++clone_counter;
        }
    }
    return res;
}
