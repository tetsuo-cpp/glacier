#include "Map.h"

#include "../Stack.h"

#include <assert.h>

struct GlacierMapNode {
  GlacierValue key;
  GlacierValue value;
  GlacierMapNode *next;
  bool set;
};

#define GLC_MAP_INIT_BUCKET_LEN 2

static size_t glacierMapHash(GlacierValue value);

int glacierMapInit(GlacierMap *map) {
  GLC_RET(glacierCAlloc(GLC_MAP_INIT_BUCKET_LEN,
                        sizeof(GLC_MAP_INIT_BUCKET_LEN),
                        (char **)&map->buckets));
  map->numBuckets = GLC_MAP_INIT_BUCKET_LEN;
  return GLC_OK;
}

int glacierMapSet(GlacierMap *map, GlacierValue key, GlacierValue value) {
  size_t index = glacierMapHash(key) % map->numBuckets;
  if (index >= map->numBuckets) {
    // Grow buckets.
    return GLC_OUT_OF_BUFFER;
  }
  GlacierMapNode *node = &map->buckets[index];
  if (node->set) {
    GlacierMapNode *current = node;
    while (current->next != NULL)
      current = current->next;
    assert(current->set);
    GLC_RET(glacierMAlloc(sizeof(GlacierMapNode), (char **)&current->next));
    node = current->next;
  }
  node->key = key;
  node->value = value;
  node->next = NULL;
  node->set = true;
  return GLC_OK;
}

int glacierMapGet(GlacierMap *map, GlacierValue key, GlacierValue *value) {
  size_t index = glacierMapHash(key) % map->numBuckets;
  if (index >= map->numBuckets)
    return GLC_KEY_MISS;
  GlacierMapNode *node = &map->buckets[index];
  if (!node->set)
    return GLC_KEY_MISS;
  *value = node->value;
  return GLC_OK;
}

void glacierMapDestroy(GlacierMap *map) {
  free(map->buckets);
  map->numBuckets = 0;
}

// Maybe use City hash later.
size_t glacierMapHash(GlacierValue value) {
  (void)value;
  return 0;
}
