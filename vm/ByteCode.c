#include "ByteCode.h"

#include "Util.h"

void glacierByteCodeInit(GlacierByteCode *bc, const char *buf, size_t len) {
  bc->buf = buf;
  bc->len = len;
  bc->offset = 0;
}

int glacierByteCodeRead8(GlacierByteCode *bc, uint8_t *val) {
  if (bc->offset >= bc->len)
    return GLC_OUT_OF_BUFFER;
  *val = bc->buf[bc->offset];
  bc->offset += 1;
  return GLC_OK;
}

int glacierByteCodeRead16(GlacierByteCode *bc, uint16_t *val) {
  if (bc->offset + 1 >= bc->len)
    return GLC_OUT_OF_BUFFER;
  *val = *((uint16_t *)&bc->buf[bc->offset]);
  bc->offset += 2;
  return GLC_OK;
}

int glacierByteCodeRead32(GlacierByteCode *bc, uint32_t *val) {
  if (bc->offset + 3 >= bc->len)
    return GLC_OUT_OF_BUFFER;
  *val = *((uint32_t *)&bc->buf[bc->offset]);
  bc->offset += 4;
  return GLC_OK;
}

int glacierByteCodeRead64(GlacierByteCode *bc, uint64_t *val) {
  if (bc->offset + 7 >= bc->len)
    return GLC_OUT_OF_BUFFER;
  *val = *((uint64_t *)&bc->buf[bc->offset]);
  bc->offset += 8;
  return GLC_OK;
}

int glacierByteCodeJump(GlacierByteCode *bc, size_t offset) {
  if (offset < 0 || offset >= bc->len)
    return GLC_OUT_OF_BUFFER;
  bc->offset = offset;
  return GLC_OK;
}

bool glacierByteCodeEnd(GlacierByteCode *bc) { return bc->offset >= bc->len; }

int glacierByteCodeTrim(GlacierByteCode *bc) {
  if (bc->offset < 0 || bc->offset >= bc->len)
    return GLC_OUT_OF_BUFFER;
  bc->len -= bc->offset;
  bc->buf += bc->offset;
  bc->offset = 0;
  return GLC_OK;
}

#define COLUMN_WIDTH 10

void glacierByteCodePrint(GlacierByteCode *bc, FILE *fd) {
  for (size_t i = 0; i < bc->len; ++i) {
    if (i != 0 && i % COLUMN_WIDTH == 0)
      fprintf(fd, "\n");
    if (i == bc->offset)
      fprintf(fd, "[0x%02hhx]", bc->buf[i]);
    else
      fprintf(fd, " 0x%02hhx ", bc->buf[i]);
  }
  fprintf(fd, "\n");
}
