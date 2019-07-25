#include "ByteCode.h"
#include <assert.h>

void glacierByteCodeInit(GlacierByteCode *bc, const char *buf, size_t len) {
  bc->buf = buf;
  bc->len = len;
  bc->offset = 0;
}
uint8_t glacierByteCodeReadByte(GlacierByteCode *bc) {
  assert(bc->offset < bc->len);

  uint8_t byteVal = bc->buf[bc->offset];
  bc->offset += 1;
  return byteVal;
}
bool glacierByteCodeEnd(GlacierByteCode *bc) { return (bc->offset >= bc->len); }
