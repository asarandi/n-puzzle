#include "npuzzle.h"

/* FNV-1a */
uint64_t hash(uint8_t *data, uint64_t size) {
    uint64_t i, hash = 0xcbf29ce484222325L;
    for (i = 0; i < size; i++) {
        hash ^= data[i];
        hash *= 0x00000100000001B3L;
    }
    return hash;
}

uint64_t get_hash(t_vertex *v) { return hash((uint8_t *)&v->puzzle, 8); }

static int __ht_insert(void **entries, size_t capacity, t_vertex *v) {
    uint64_t index;

    index = get_hash(v) % capacity;
    while (entries[index]) {
        if (((t_vertex *)entries[index])->puzzle == v->puzzle)
            return 0;
        index = (index + 1) % capacity;
    }
    entries[index] = v;
    return 1;
}

static void ht_extend(t_ht *ht) {
    uint64_t new_capacity, count, i;
    void **new_entries;

    new_capacity = ht->capacity << 1;
    if (!(new_entries = calloc(new_capacity, sizeof(void *))))
        return (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
    for (i = count = 0; i < ht->capacity; i++) {
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

void ht_insert(t_ht *ht, t_vertex *v) {
    if (((ht->num_keys * 100) / ht->capacity) > 75)
        ht_extend(ht);
    if (__ht_insert(ht->entries, ht->capacity, v))
        ++ht->num_keys;
}

t_vertex *ht_find(t_ht *ht, uint64_t key) {
    uint64_t index;

    index = hash((uint8_t *)&key, 8) % ht->capacity;
    while (ht->entries[index]) {
        if (((t_vertex *)ht->entries[index])->puzzle == key)
            return (t_vertex *)ht->entries[index];
        index = (index + 1) % ht->capacity;
    }
    return NULL;
}

t_ht *ht_init() {
    t_ht *ht;

    if (!(ht = calloc(1, sizeof(t_ht)))) {
        (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
        return NULL;
    }
    ht->capacity = 256;
    if (!(ht->entries = calloc(ht->capacity, sizeof(void *)))) {
        (void)free(ht);
        (void)fprintf(stderr, "%s: calloc() failed\n", __func__);
        return NULL;
    }
    return ht;
}

void ht_destroy_all(t_ht *ht) {
    uint64_t i;

    for (i = 0; i < ht->capacity; i++) {
        if (ht->entries[i])
            free(ht->entries[i]);
    }
    free(ht->entries);
    free(ht);
}
