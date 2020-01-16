#include "Array.h"

#include "Util.h"

#define GLC_ARRAY_INIT_LEN 10

static int glacierArrayGrow(GlacierArray *array, size_t len);

int glacierArrayInit(GlacierArray *array) {
  GLC_RET(glacierMAlloc(GLC_ARRAY_INIT_LEN, (char **)&array->data));
  array->len = GLC_ARRAY_INIT_LEN;
  for (size_t i = 0; i < array->len; ++i)
    array->data[i] = -1;
  return GLC_OK;
}

int glacierArraySet(GlacierArray *array, size_t index, int val) {
  if (index >= array->len)
    GLC_RET(glacierArrayGrow(array, array->len * 2));
  int *pos = &array->data[index];
  if (*pos != -1 || val < 0)
    return GLC_ERROR;
  *pos = val;
  return GLC_OK;
}

int glacierArrayGet(GlacierArray *array, size_t index, int *val) {
  if (index >= array->len)
    return GLC_OUT_OF_BUFFER;
  int value = array->data[index];
  if (value == -1)
    return GLC_ERROR;
  *val = value;
  return GLC_OK;
}

static int glacierArrayGrow(GlacierArray *array, size_t len) {
  size_t oldLen = array->len;
  GLC_RET(glacierReAlloc(len, (char **)&array->data));
  // Init new slots to -1.
  for (size_t i = oldLen - 1; i < len; ++i)
    array->data[i] = -1;
  array->len = len;
  return GLC_OK;
}
