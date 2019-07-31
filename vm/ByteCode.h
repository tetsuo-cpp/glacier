#ifndef GLACIERVM_BYTECODE_H
#define GLACIERVM_BYTECODE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define GLACIER_BYTECODE_STRUCT_DEF 0x00
#define GLACIER_BYTECODE_FUNCTION_DEF 0x01
#define GLACIER_BYTECODE_SET_VAR 0x02
#define GLACIER_BYTECODE_GET_VAR 0x03
#define GLACIER_BYTECODE_CALL_FUNC 0x04
#define GLACIER_BYTECODE_RETURN 0x05
#define GLACIER_BYTECODE_RETURN_VAL 0x06
#define GLACIER_BYTECODE_ADD 0x07
#define GLACIER_BYTECODE_INT 0x08
#define GLACIER_BYTECODE_STRING 0x09

#define GLACIER_TYPEID_INT 0x00
#define GLACIER_TYPEID_STRING 0x01

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
bool glacierByteCodeEnd(GlacierByteCode *bc);

#endif // GLACIERVM_BYTECODE_H
