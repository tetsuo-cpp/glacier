#include "Map.h"

#include "../Stack.h"

struct GlacierMapNode {
  GlacierValue key;
  GlacierValue value;
  GlacierMapNode *next;
};

int glacierMapInit(GlacierMap *map) {
  (void)map;
  return GLC_OK;
}

int glacierMapSet(GlacierMap *map, GlacierValue key, GlacierValue value) {
  (void)map;
  (void)key;
  (void)value;
  return GLC_OK;
}

int glacierMapGet(GlacierMap *map, GlacierValue key, GlacierValue *value) {
  (void)map;
  (void)key;
  (void)value;
  return GLC_OK;
}

void glacierMapDestroy(GlacierMap *map) { (void)map; }
