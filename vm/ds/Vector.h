#ifndef GLACIERVM_VECTOR_H
#define GLACIERVM_VECTOR_H

#include "../Stack.h"

typedef struct {
  GlacierValue *data;
  size_t len;
  size_t capacity;
} GlacierVector;

void glacierVectorInit(GlacierVector *vector);
int glacierVectorPush(GlacierVector *vector, GlacierValue *value);
int glacierVectorPop(GlacierVector *vector);
void glacierVectorDestroy(GlacierVector *vector);

#endif // GLACIERVM_VECTOR_H
