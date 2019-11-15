#include "npuzzle.h"

static void bubble_down(t_pq *q)
{
    size_t  i, c;
    void    *ptr;

    i = 0;
    while ((c = (i << 1) + 1) < q->num_nodes)
    {
        if (c + 1 < q->num_nodes)
            c = q->cmp(q->nodes[c], q->nodes[c + 1]) <= 0 ? c : c + 1;
        if (q->cmp(q->nodes[i], q->nodes[c]) <= 0)
            break ;
        ptr = q->nodes[c];
        q->nodes[c] = q->nodes[i];
        q->nodes[i] = ptr;
        i = c;
    }
}

void    *pq_extract(t_pq *q)
{
    void    *res;

    res = q->nodes[0];
    q->nodes[0] = q->nodes[--(q->num_nodes)];
    q->nodes[q->num_nodes] = NULL;
    bubble_down(q);
    return res;
}

static void bubble_up(t_pq *q)
{
    size_t  i, p;
    void    *ptr;

    i = q->num_nodes - 1;
    while (i)
    {
        p = (i - 1) >> 1;
        if (q->cmp(q->nodes[p], q->nodes[i]) <= 0)
            break ;
        ptr = q->nodes[p];
        q->nodes[p] = q->nodes[i];
        q->nodes[i] = ptr;
        i = p;
    }
}

static void pq_extend(t_pq *q)
{
    void    *nodes;
    size_t  size;

    size = q->capacity + (sysconf(_SC_PAGESIZE) / sizeof(void *));
    if (!(nodes = realloc(q->nodes, size * sizeof(void *))))
        return (void)fprintf(stderr, "realloc(%lu) failed\n", size);
    q->capacity = size;
    q->nodes = nodes;
}

void pq_insert(t_pq *q, void *node)
{
    if (q->num_nodes + 1 >= q->capacity)
        pq_extend(q);
    q->nodes[q->num_nodes++] = node;
    bubble_up(q);
}

t_pq  *pq_init(int (*cmp)(void *, void *))
{
    t_pq      *q;

    if (!(q = calloc(1, sizeof(t_pq))))
        return NULL;
    q->cmp = cmp;
    return q;
}

void pq_destroy(t_pq *q)
{
    free(q->nodes);
    free(q);
}
