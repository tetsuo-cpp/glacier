#include "ByteCode.h"

void glacierByteCodeInit(GlacierByteCode *bc, const char *buf, size_t len) {
  bc->buf = buf;
  bc->len = len;
  bc->offset = 0;
}

int glacierByteCodeRead8(GlacierByteCode *bc, uint8_t *val) {
  if (bc->offset >= bc->len)
    return -1;
  *val = bc->buf[bc->offset];
  bc->offset += 1;
  return 0;
}

int glacierByteCodeRead16(GlacierByteCode *bc, uint16_t *val) {
  if (bc->offset + 1 >= bc->len)
    return -1;
  *val = *((uint16_t *)&bc->buf[bc->offset]);
  bc->offset += 2;
  return 0;
}

bool glacierByteCodeEnd(GlacierByteCode *bc) { return bc->offset >= bc->len; }
