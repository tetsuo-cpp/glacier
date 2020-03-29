#ifndef GLACIERVM_BYTECODE_H
#define GLACIERVM_BYTECODE_H

#include "Ops.h"

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#define GLC_TYPEID_INT 0x00
#define GLC_TYPEID_STRING 0x01
#define GLC_TYPEID_VECTOR 0x02
#define GLC_TYPEID_MAP 0x03

typedef struct {
  const char *buf;
  size_t len;
  size_t offset;
} GlacierByteCode;

void glacierByteCodeInit(GlacierByteCode *bc, const char *buf, size_t len);
int glacierByteCodeRead8(GlacierByteCode *bc, uint8_t *val);
int glacierByteCodeRead16(GlacierByteCode *bc, uint16_t *val);
int glacierByteCodeRead32(GlacierByteCode *bc, uint32_t *val);
int glacierByteCodeRead64(GlacierByteCode *bc, uint64_t *val);
int glacierByteCodeJump(GlacierByteCode *bc, size_t offset);
bool glacierByteCodeEnd(GlacierByteCode *bc);
int glacierByteCodeTrim(GlacierByteCode *bc);
void glacierByteCodePrint(GlacierByteCode *bc, FILE *fd);

#endif // GLACIERVM_BYTECODE_H
