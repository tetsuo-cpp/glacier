#ifndef GLACIERVM_BYTECODE_H
#define GLACIERVM_BYTECODE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define GLACIER_BYTECODE_STRUCT_DEF 0x00

#define GLACIER_TYPEID_INT 0x00
#define GLACIER_TYPEID_STRING 0x01

typedef struct {
  const char *buf;
  size_t len;
  size_t offset;
} GlacierByteCode;

void glacierByteCodeInit(GlacierByteCode *bc, const char *buf, size_t len);
uint8_t glacierByteCodeReadByte(GlacierByteCode *bc);
bool glacierByteCodeEnd(GlacierByteCode *bc);

#endif // GLACIERVM_BYTECODE_H
