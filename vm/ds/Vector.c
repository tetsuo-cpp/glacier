#include "Vector.h"

#include "../GC.h"
#include "../Stack.h"
#include "../Util.h"

#define GLC_VECTOR_INIT_CAPACITY 2

int glacierVectorInit(GlacierVector *vector) {
  vector->data = NULL;
  GLC_RET(glacierGCAlloc(GLC_VECTOR_INIT_CAPACITY * sizeof(GlacierValue),
                         (char **)&vector->data));
  vector->len = 0;
  vector->capacity = GLC_VECTOR_INIT_CAPACITY;
  return GLC_OK;
}

int glacierVectorPush(GlacierVector *vector, GlacierValue value) {
  if (vector->len == vector->capacity) {
    size_t newCapacity = vector->capacity * 2;
    GLC_RET(glacierGCReAlloc(newCapacity * sizeof(GlacierValue),
                             (char **)&vector->data));
    vector->capacity = newCapacity;
  }
  vector->data[vector->len++] = value;
  return GLC_OK;
}

int glacierVectorPop(GlacierVector *vector) {
  if (vector->len <= 0)
    return GLC_OUT_OF_BUFFER;
  --vector->len;
  return GLC_OK;
}

int glacierVectorSet(GlacierVector *vector, size_t index, GlacierValue val) {
  if (index >= vector->len)
    return GLC_OUT_OF_BUFFER;
  vector->data[index] = val;
  return GLC_OK;
}

int glacierVectorGet(GlacierVector *vector, size_t index, GlacierValue *val) {
  if (index >= vector->len)
    return GLC_OUT_OF_BUFFER;
  *val = vector->data[index];
  return GLC_OK;
}

void glacierVectorDestroy(GlacierVector *vector) {
  if (vector->data)
    glacierGCFree((char **)&vector->data);
  vector->len = 0;
  vector->capacity = 0;
}
