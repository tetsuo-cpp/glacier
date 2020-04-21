#include "Map.h"

#include "../GC.h"
#include "../Stack.h"

#include <clhash.h>

#include <assert.h>
#include <string.h>

struct GlacierMapNode {
  GlacierValue key;
  GlacierValue value;
  GlacierMapNode *next;
  bool set;
};

#define GLC_MAP_INIT_BUCKET_LEN 2
#define GLC_MAP_MAX_DEPTH 3

static size_t glacierMapHash(void *clHashKey, GlacierValue value);
static int glacierMapRebuild(GlacierMap *map);
static bool glacierMapKeyEq(GlacierValue lhs, GlacierValue rhs);

int glacierMapInit(GlacierMap *map) {
  map->buckets = NULL;
  GLC_RET(glacierGCAlloc(GLC_MAP_INIT_BUCKET_LEN * sizeof(GlacierMapNode),
                         (char **)&map->buckets));
  map->numBuckets = GLC_MAP_INIT_BUCKET_LEN;
  // Seed this properly later.
  map->clHashKey = get_random_key_for_clhash(UINT64_C(0x23a23cf5033c3c81),
                                             UINT64_C(0xb3816f6a2c68e530));
  return GLC_OK;
}

int glacierMapSet(GlacierMap *map, GlacierValue key, GlacierValue value) {
  size_t index = glacierMapHash(map->clHashKey, key) % map->numBuckets;
  GlacierMapNode *node = &map->buckets[index];
  unsigned int depth = 0;
  if (node->set) {
    GlacierMapNode *current = node;
    while (current->next != NULL)
      current = current->next, ++depth;
    assert(current->set);
    GLC_RET(glacierGCAlloc(sizeof(GlacierMapNode), (char **)&current->next));
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
  size_t index = glacierMapHash(map->clHashKey, key) % map->numBuckets;
  if (index >= map->numBuckets)
    return GLC_KEY_MISS;
  GlacierMapNode *node = &map->buckets[index];
  for (; node; node = node->next) {
    if (node->set && glacierMapKeyEq(node->key, key)) {
      *value = node->value;
      return GLC_OK;
    }
  }
  return GLC_KEY_MISS;
}

int glacierMapUnset(GlacierMap *map, GlacierValue key) {
  size_t index = glacierMapHash(map->clHashKey, key) % map->numBuckets;
  if (index >= map->numBuckets)
    return GLC_KEY_MISS;
  GlacierMapNode *prev = NULL;
  GlacierMapNode *node = &map->buckets[index];
  for (; node; prev = node, node = node->next)
    if (node->set && glacierMapKeyEq(node->key, key))
      goto remove;
  return GLC_KEY_MISS;
remove:
  if (prev) {
    prev->next = node->next;
    glacierGCFree((char **)&node);
  } else {
    GlacierMapNode *nextNode = node->next;
    if (nextNode) {
      // Bitwise copy so we're pointing to the one after next.
      // Looks as if we just duplicated the second node and "removed" the first.
      *node = *nextNode;
      // Now free the second since it's redundant.
      glacierGCFree((char **)&nextNode);
    } else
      // This means we're the only node in this bucket. Just unset it.
      node->set = false;
  }
  return GLC_OK;
}

void glacierMapDestroy(GlacierMap *map) {
  if (map->buckets)
    glacierGCFree((char **)&map->buckets);
  map->numBuckets = 0;
  free(map->clHashKey);
  map->clHashKey = NULL;
}

size_t glacierMapHash(void *clHashKey, GlacierValue value) {
  switch (value.typeId) {
  case GLC_TYPEID_INT:
    return clhash(clHashKey, (char *)&value.intValue, 8);
  case GLC_TYPEID_STRING:
    return clhash(clHashKey, value.stringValue, strlen(value.stringValue));
  default:
    assert(!"unsupported hash key");
  }
  return 0;
}

int glacierMapRebuild(GlacierMap *map) {
  int ret = GLC_OK;
  GlacierMap newMap = {.buckets = NULL, .numBuckets = map->numBuckets * 2};
  GLC_RET(glacierGCAlloc(newMap.numBuckets * sizeof(GlacierMapNode),
                         (char **)&newMap.buckets));
  // Seed this properly later.
  newMap.clHashKey = get_random_key_for_clhash(UINT64_C(0x23a23cf5033c3c81),
                                               UINT64_C(0xb3816f6a2c68e530));
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

bool glacierMapKeyEq(GlacierValue lhs, GlacierValue rhs) {
  if (lhs.typeId != rhs.typeId)
    return false;
  if (lhs.typeId == GLC_TYPEID_INT)
    return lhs.intValue == rhs.intValue;
  else if (lhs.typeId == GLC_TYPEID_STRING)
    return (strcmp(lhs.stringValue, rhs.stringValue) == 0);
  else {
    assert(!"Can only use int or string keys for a map");
    return false;
  }
}
