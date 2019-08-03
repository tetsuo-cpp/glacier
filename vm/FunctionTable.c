#include "FunctionTable.h"

#include "Util.h"

#include <string.h>

void glacierFunctionTableInit(GlacierFunctionTable *ft) {
  memset(ft->data, -1, sizeof(ft->data));
}

int glacierFunctionTableSet(GlacierFunctionTable *ft, int functionId,
                            int offset) {
  if (functionId < 0 || functionId >= MAX_FUNCTION_NUMBER)
    return GLC_OUT_OF_BUFFER;
  int *pos = &ft->data[functionId];
  if (*pos != -1 || offset < 0)
    return GLC_ERROR;
  *pos = offset;
  return GLC_OK;
}

int glacierFunctionTableGet(GlacierFunctionTable *ft, int functionId,
                            int *offset) {
  if (functionId < 0 | functionId >= MAX_FUNCTION_NUMBER)
    return GLC_OUT_OF_BUFFER;
  int value = ft->data[functionId];
  if (value == -1)
    return GLC_ERROR;
  *offset = value;
  return GLC_OK;
}
