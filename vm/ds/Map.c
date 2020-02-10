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
#define GLC_MAP_MAX_DEPTH 3

static size_t glacierMapHash(GlacierValue value);
static int glacierMapRebuild(GlacierMap *map);

int glacierMapInit(GlacierMap *map) {
  GLC_RET(glacierCAlloc(GLC_MAP_INIT_BUCKET_LEN, sizeof(GlacierMapNode),
                        (char **)&map->buckets));
  map->numBuckets = GLC_MAP_INIT_BUCKET_LEN;
  return GLC_OK;
}

int glacierMapSet(GlacierMap *map, GlacierValue key, GlacierValue value) {
  size_t index = glacierMapHash(key) % map->numBuckets;
  GlacierMapNode *node = &map->buckets[index];
  unsigned int depth = 0;
  if (node->set) {
    GlacierMapNode *current = node;
    while (current->next != NULL)
      current = current->next, ++depth;
    assert(current->set);
    GLC_RET(glacierMAlloc(sizeof(GlacierMapNode), (char **)&current->next));
    node = current->next;
  }
  if (depth >= GLC_MAP_MAX_DEPTH) {
    GLC_RET(glacierMapRebuild(map));
    GLC_RET(glacierMapSet(map, key, value));
    return GLC_OK;
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

int glacierMapRebuild(GlacierMap *map) {
  int ret = GLC_OK;
  GlacierMap newMap = {.buckets = NULL, .numBuckets = map->numBuckets * 2};
  GLC_RET(glacierCAlloc(newMap.numBuckets, sizeof(GlacierMapNode),
                        (char **)&newMap.buckets));
  for (size_t i = 0; i < map->numBuckets; ++i) {
    GlacierMapNode *current = &map->buckets[i];
    while (current != NULL && current->set) {
      GLC_ERR(glacierMapSet(&newMap, current->key, current->value));
      current = current->next;
    }
  }
  glacierMapDestroy(map);
  *map = newMap;
err:
  if (ret != GLC_OK)
    glacierMapDestroy(&newMap);
  return ret;
}
