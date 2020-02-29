#include "GC.h"
#include "Util.h"

#include <gc/gc.h>

#include <stdlib.h>

int glacierGCAlloc(size_t size, char **p) {
  char *alloc = GC_malloc(size);
  if (!alloc)
    return GLC_OOM;
  *p = alloc;
  return GLC_OK;
}

int glacierGCReAlloc(size_t size, char **p) {
  char *tmp = GC_realloc(*p, size);
  if (!tmp)
    return GLC_OOM;
  *p = tmp;
  return GLC_OK;
}

void glacierGCFree(char **p) {
  GC_free(*p);
  *p = NULL;
}
