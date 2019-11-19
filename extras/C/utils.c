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

int cmp(void *ptr_a, void *ptr_b)
{
    int         res;
    t_vertex     *a, *b;

    a = ptr_a;
    b = ptr_b;
    res = (a->g + a->h) - (b->g + b->h);
    return res == 0 ? (a->counter - b->counter) : res;
}
