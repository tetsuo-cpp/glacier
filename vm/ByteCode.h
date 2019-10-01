#ifndef GLACIERVM_BYTECODE_H
#define GLACIERVM_BYTECODE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#define GLC_BYTECODE_STRUCT_DEF 0x00
#define GLC_BYTECODE_FUNCTION_DEF 0x01
#define GLC_BYTECODE_SET_VAR 0x02
#define GLC_BYTECODE_GET_VAR 0x03
#define GLC_BYTECODE_CALL_FUNC 0x04
#define GLC_BYTECODE_RETURN 0x05
#define GLC_BYTECODE_RETURN_VAL 0x06
#define GLC_BYTECODE_ADD 0x07
#define GLC_BYTECODE_INT 0x08
#define GLC_BYTECODE_STRING 0x09
#define GLC_BYTECODE_SUBTRACT 0x0A
#define GLC_BYTECODE_MULTIPLY 0x0B
#define GLC_BYTECODE_DIVIDE 0x0C
#define GLC_BYTECODE_FUNCTION_JMP 0x0D
#define GLC_BYTECODE_HEADER_END 0x0F
#define GLC_BYTECODE_PRINT 0x10
#define GLC_BYTECODE_EQ 0x11
#define GLC_BYTECODE_JUMP_IF_TRUE 0x12
#define GLC_BYTECODE_JUMP_IF_FALSE 0x13
#define GLC_BYTECODE_JUMP 0x14
#define GLC_BYTECODE_STRUCT 0x15
#define GLC_BYTECODE_GET_STRUCT_MEMBER 0x16
#define GLC_BYTECODE_SET_STRUCT_MEMBER 0x17

#define GLC_TYPEID_INT 0x00
#define GLC_TYPEID_STRING 0x01

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
