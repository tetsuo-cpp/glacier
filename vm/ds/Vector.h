#ifndef GLACIERVM_VECTOR_H
#define GLACIERVM_VECTOR_H

#include "../Stack.h"

typedef struct {
  GlacierValue *data;
  size_t len;
  size_t capacity;
} GlacierVector;

int glacierVectorInit(GlacierVector *vector);
int glacierVectorPush(GlacierVector *vector, GlacierValue value);
int glacierVectorPop(GlacierVector *vector);
int glacierVectorSet(GlacierVector *vector, size_t index, GlacierValue val);
int glacierVectorGet(GlacierVector *vector, size_t index, GlacierValue *val);
void glacierVectorDestroy(GlacierVector *vector);

#endif // GLACIERVM_VECTOR_H
