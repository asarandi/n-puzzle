#include "npuzzle.h"

void print_puzzle(t_vertex *v)
{
    int i, nibble;

//    printf("G: %d, H: %d, COUNTER: = %d\n", v->g, v->h, v->counter);
    for (i=0; i<16; i++)
    {
        nibble = (v->puzzle >> ((15 - i) << 2)) & 15;
		printf("%d%s", nibble, i + 1 < 16 ? ", " : "\n");
    }
}

int heuristic(uint64_t x)
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

int cmp(void *ptr_a, void *ptr_b)
{
    int         res;
    t_vertex     *a, *b;

    a = ptr_a;
    b = ptr_b;
    res = (a->g + a->h) - (b->g + b->h);
    return res == 0 ? (a->counter - b->counter) : res;
}
