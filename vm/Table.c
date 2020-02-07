#include "Table.h"

#include "Util.h"

#define GLC_TABLE_INIT_LEN 2

static int glacierTableGrow(GlacierTable *table, size_t len);

int glacierTableInit(GlacierTable *table) {
  GLC_RET(
      glacierMAlloc(GLC_TABLE_INIT_LEN * sizeof(int), (char **)&table->data));
  table->len = GLC_TABLE_INIT_LEN;
  for (size_t i = 0; i < table->len; ++i)
    table->data[i] = -1;
  return GLC_OK;
}

int glacierTableSet(GlacierTable *table, size_t index, int val) {
  if (index >= table->len) {
    // Double each time.
    size_t newLen = table->len * 2;
    // Unless the index is larger than that.
    if (newLen < index + 1)
      newLen = index + 1;
    GLC_RET(glacierTableGrow(table, newLen));
  }
  int *pos = &table->data[index];
  if (*pos != -1 || val < 0)
    return GLC_ERROR;
  *pos = val;
  return GLC_OK;
}

int glacierTableGet(GlacierTable *table, size_t index, int *val) {
  if (index >= table->len)
    return GLC_OUT_OF_BUFFER;
  int value = table->data[index];
  if (value == -1)
    return GLC_ERROR;
  *val = value;
  return GLC_OK;
}

void glacierTableDestroy(GlacierTable *table) {
  free(table->data);
  table->data = NULL;
  table->len = 0;
}

static int glacierTableGrow(GlacierTable *table, size_t len) {
  size_t oldLen = table->len;
  GLC_RET(glacierReAlloc(len * sizeof(int), (char **)&table->data));
  // Init new slots to -1.
  for (size_t i = oldLen; i < len; ++i)
    table->data[i] = -1;
  table->len = len;
  return GLC_OK;
}
