#include "Vector.h"

void glacierVectorInit(GlacierVector *vector) {
  vector->data = NULL;
  vector->len = 0;
  vector->capacity = 0;
}
