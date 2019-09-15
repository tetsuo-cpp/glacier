#ifndef GLACIERVM_STACK_H
#define GLACIERVM_STACK_H

#include "ByteCode.h"
#include "Util.h"

#include <stdint.h>

#define MAX_STACK_SIZE 100
#define MAX_FRAME_BINDINGS 100

// Switch over the typeId and then use the appropriate union type.
typedef struct {
  int typeId;
  union {
    uint64_t intValue;
    char *stringValue;
    void *structValue;
  };
} GlacierValue;

// Stack value constructors.
GlacierValue glacierValueFromInt(uint64_t value);
GlacierValue glacierValueFromString(char *value);
GlacierValue glacierValueFromStruct(void *value, int id);

// Debug logger.
static inline void glacierValueLog(GlacierValue *value) {
  switch (value->typeId) {
  case GLC_TYPEID_INT:
    GLC_LOG_DBG("(TypeId=int, Value=%llu)", value->intValue);
    break;
  case GLC_TYPEID_STRING:
    GLC_LOG_DBG("(TypeId=string, Value=%s)", value->stringValue);
    break;
  default:
    GLC_LOG_DBG("(TypeId=%llu)", value->typeId);
    break;
  }
}

typedef struct {
  GlacierValue data[MAX_STACK_SIZE];
  int stackPointer;
} GlacierStack;

void glacierStackInit(GlacierStack *stack);
int glacierStackPush(GlacierStack *stack, GlacierValue value);
int glacierStackTop(GlacierStack *stack, GlacierValue *value);
int glacierStackPop(GlacierStack *stack, GlacierValue *value);

typedef struct {
  GlacierValue bindings[MAX_FRAME_BINDINGS]; // Id => value mapping.
  int bcOffset;                              // Bytecode offset to jump back to.
} GlacierCallStackFrame;

typedef struct {
  GlacierCallStackFrame frames[MAX_STACK_SIZE];
  int stackPointer;
} GlacierCallStack;

void glacierCallStackInit(GlacierCallStack *stack);
int glacierCallStackPush(GlacierCallStack *stack, int bcOffset);
int glacierCallStackPop(GlacierCallStack *stack);
int glacierCallStackGet(GlacierCallStack *stack, int id, GlacierValue *value);
int glacierCallStackSet(GlacierCallStack *stack, int id, GlacierValue value);
int glacierCallStackGetByteCodeOffset(GlacierCallStack *stack, int *bcOffset);
void glacierCallStackFrameInit(GlacierCallStackFrame *frame, int bcOffset);

#endif // GLACIERVM_STACK_H
