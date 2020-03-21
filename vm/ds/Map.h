#ifndef GLACIERVM_MAP_H
#define GLACIERVM_MAP_H

#include <stdlib.h>

typedef struct GlacierValue GlacierValue;
typedef struct GlacierMapNode GlacierMapNode;

typedef struct {
  GlacierMapNode *buckets;
  size_t numBuckets;
  void *clHashKey;
} GlacierMap;

int glacierMapInit(GlacierMap *map);
int glacierMapSet(GlacierMap *map, GlacierValue key, GlacierValue value);
int glacierMapGet(GlacierMap *map, GlacierValue key, GlacierValue *value);
void glacierMapDestroy(GlacierMap *map);

#endif // GLACIERVM_MAP_H
