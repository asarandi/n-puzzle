#include "npuzzle.h"

int main(int ac, char **av)
{
    t_pq        *pq;
    t_ht        *ht;
    t_vertex    *root, *v = NULL, *tmp, **moves;
    int         i, tentative_g;
    size_t      is_open = 0, is_closed = 0;

    root = calloc(1, sizeof(t_vertex));
    root->puzzle = 0x597138aeb4f26d0cL; //sample4_2000.txt

    if (ac == 17)
    {
        for (i=1; i<17; i++)
        {
            root->puzzle <<= 4;
            root->puzzle |= atoi(av[i]) & 15;
        }
    }

    root->h = heuristic(root->puzzle);

    ht = ht_init();
    pq = pq_init(&cmp);
    pq_insert(pq, root);

    while (pq->num_nodes)
    {
        v = (t_vertex *)pq_extract(pq);
        if (v->puzzle == GOAL_STATE)
            break ;
        if (v->is_closed)
            continue ;
        v->is_closed = 1;
        tentative_g = v->g + 1;
        moves = make_moves(v);
        for (i=0; i<4; i++)
        {
            if (!moves[i]) break ;
            if ((tmp = ht_find(ht, moves[i]->puzzle)))
            {
                free(moves[i]);
                moves[i] = tmp;
            }
            if (moves[i]->is_closed)
                continue ;
            if ((moves[i]->is_open) && (moves[i]->g <= tentative_g))
                continue ;
            if (!tmp)
                moves[i]->h = heuristic(moves[i]->puzzle);
            moves[i]->is_open = 1;
            moves[i]->g = tentative_g;
            moves[i]->parent = v->puzzle;
            ht_insert(ht, moves[i]);
            pq_insert(pq, moves[i]);
        }
    }

    while (v)
    {
        print_puzzle(v);
        v = ht_find(ht, v->parent);
    }
    print_puzzle(root);
    printf("pq->num_nodes = %ld pq->capacity = %ld\n", pq->num_nodes, pq->capacity);
    printf(" ht->num_keys = %ld ht->capacity = %ld\n",  ht->num_keys, ht->capacity);
    for (size_t i=0; i<ht->capacity; i++)
    {
        if (ht->entries[i])
        {
            is_open += ((t_vertex *)ht->entries[i])->is_open;
            is_closed += ((t_vertex *)ht->entries[i])->is_closed;
        }
    }
    printf("is_open = %ld, is_closed = %ld\n", is_open, is_closed);

    pq_destroy(pq);
    ht_destroy_all(ht);
    return 0;
}
