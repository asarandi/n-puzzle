#ifndef NPUZZLE_H
# define NPUZZLE_H

# include <ctype.h>
# include <stdio.h>
# include <unistd.h>
# include <limits.h>
# include <stdint.h>
# include <stdlib.h>
# include <string.h>
# include <stdbool.h>

# define GOAL_STATE (0x123456789abcdef0L)
# define ABS(i)     ((i) < 0 ? -(i) : (i))

# define UP(x,z)    ((x & ~(15L << ((15 - ((z) - 4)) << 2))) | ((x & (15L << ((15 - ((z) - 4)) << 2))) >> (4 << 2)))
# define LEFT(x,z)  ((x & ~(15L << ((15 - ((z) - 1)) << 2))) | ((x & (15L << ((15 - ((z) - 1)) << 2))) >> (1 << 2)))
# define DOWN(x,z)  ((x & ~(15L << ((15 - ((z) + 4)) << 2))) | ((x & (15L << ((15 - ((z) + 4)) << 2))) << (4 << 2)))
# define RIGHT(x,z) ((x & ~(15L << ((15 - ((z) + 1)) << 2))) | ((x & (15L << ((15 - ((z) + 1)) << 2))) << (1 << 2)))

typedef struct      s_vertex
{
    uint8_t         g;
    uint8_t         h;
    uint8_t         is_open;
    uint8_t         is_closed;
    int             counter;
    uint64_t        puzzle;
    uint64_t        parent;

} t_vertex;

    int             cmp(void *ptr_a, void *ptr_b);
    int             heuristic(uint64_t x);
    t_vertex        **make_moves(t_vertex *v);
    void            print_puzzle(t_vertex *v);

/* t_pq */

typedef struct      s_priority_queue {
    size_t          capacity;
    size_t          num_nodes;
    int             (*cmp)(void *, void *);
    void            **nodes;
} t_pq;

    t_pq            *pq_init(int (*cmp)(void *, void *));
    void            *pq_extract(t_pq *q);
    void            pq_insert(t_pq *q, void *node);
    void            pq_destroy(t_pq *q);

/* ht */

typedef struct      s_hash_table {
    size_t          capacity;
    size_t          num_keys;
    void            **entries;
} t_ht;

    t_vertex        *ht_find(t_ht *ht, uint64_t key);
    t_ht            *ht_init();
    void            ht_insert(t_ht *ht, t_vertex *v);
    void            ht_destroy_all(t_ht *ht);

#endif
