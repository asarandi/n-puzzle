#include "npuzzle.h"

/* FNV-1a */
size_t hash(void *data, size_t size)
{
    size_t hash = 0xcbf29ce484222325L;
    for (size_t i=0; i<size; i++)
    {
        hash ^= *(unsigned char *)(data+i);
        hash *= 0x00000100000001B3L;
    }
    return hash;
}

size_t get_hash(t_vertex *v)
{
    return hash((char *)&v->puzzle, 8);
}

static int __ht_insert(void **entries, size_t capacity, t_vertex *v)
{
    size_t  i;

    i = get_hash(v) % capacity;
    while (entries[i])
    {
        if (((t_vertex *)entries[i])->puzzle == v->puzzle)
            return 0;
        i = (i + 1) % capacity;
    }
    entries[i] = v;
    return 1;
}

static void ht_extend(t_ht *ht)
{
    size_t  new_capacity, count, i;
    void    **new_entries;

    new_capacity = ht->capacity << 1;
    if (!(new_entries = calloc(new_capacity, sizeof(void *))))
        return (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
    for (i=count=0; i < ht->capacity; i++)
    {
        if (ht->entries[i]) {
            if (__ht_insert(new_entries, new_capacity, ht->entries[i]))
                ++count;
        }
        if (count >= ht->num_keys)
            break;
    }
    free(ht->entries);
    ht->entries = new_entries;
    ht->capacity = new_capacity;
}

void        ht_insert(t_ht *ht, t_vertex *v)
{
    if (((ht->num_keys * 100) / ht->capacity) > 75)
        ht_extend(ht);
    if (__ht_insert(ht->entries, ht->capacity, v))
        ++ht->num_keys;
}

t_vertex     *ht_find(t_ht *ht, uint64_t key)
{
    size_t  i;

    i = hash((char *)&key, 8) % ht->capacity;
    while (ht->entries[i])
    {
        if (((t_vertex *)ht->entries[i])->puzzle == key)
            return (t_vertex *)ht->entries[i];
        i = (i + 1) % ht->capacity;
    }
    return NULL;
}

t_ht *ht_init()
{
    t_ht    *ht;

    if (!(ht = calloc(1, sizeof(t_ht))))
        (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
    ht->capacity = 256;
    if (!(ht->entries = calloc(ht->capacity, sizeof(void *))))
        (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
    return ht;
}

void ht_destroy_all(t_ht *ht)
{
    size_t  i;

    for (i=0; i<ht->capacity; i++)
    {
        if (ht->entries[i])
            free(ht->entries[i]);
    }
    free(ht->entries);
    free(ht);
}
