#ifndef GLACIERVM_GC_H
#define GLACIERVM_GC_H

#include <stdlib.h>

int glacierGCAlloc(size_t size, char **p);
int glacierGCReAlloc(size_t size, char **p);
void glacierGCFree(char **p);

#endif // GLACIERVM_GC_H
