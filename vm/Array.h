#ifndef GLACIERVM_ARRAY_H
#define GLACIERVM_ARRAY_H

#include <stdlib.h>

typedef struct {
  int *data;
  size_t len;
} GlacierArray;

int glacierArrayInit(GlacierArray *array);
int glacierArraySet(GlacierArray *array, size_t index, int val);
int glacierArrayGet(GlacierArray *array, size_t index, int *val);
void glacierArrayDestroy(GlacierArray *array);

#endif // GLACIERVM_ARRAY_H
