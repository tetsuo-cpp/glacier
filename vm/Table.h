#ifndef GLACIERVM_TABLE_H
#define GLACIERVM_TABLE_H

#include <stdlib.h>

typedef struct {
  int *data;
  size_t len;
} GlacierTable;

int glacierTableInit(GlacierTable *table);
int glacierTableSet(GlacierTable *table, size_t index, int val);
int glacierTableGet(GlacierTable *table, size_t index, int *val);
void glacierTableDestroy(GlacierTable *table);

#endif // GLACIERVM_TABLE_H
