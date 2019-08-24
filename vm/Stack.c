#include "Stack.h"

#include "ByteCode.h"
#include "Util.h"

#include <stdbool.h>

static inline bool glacierStackIsValidPointer(int pointer) {
  return pointer >= 0 && pointer < MAX_STACK_SIZE;
}

GlacierValue glacierValueFromInt(uint64_t value) {
  GlacierValue obj;
  obj.typeId = GLC_TYPEID_INT;
  obj.intValue = value;
  return obj;
}

GlacierValue glacierValueFromString(char *value) {
  GlacierValue obj;
  obj.typeId = GLC_TYPEID_STRING;
  obj.stringValue = value;
  return obj;
}

void glacierStackInit(GlacierStack *stack) { stack->stackPointer = 0; }

int glacierStackPush(GlacierStack *stack, GlacierValue value) {
  if (!glacierStackIsValidPointer(stack->stackPointer))
    return GLC_STACK_OVERFLOW;
  stack->data[stack->stackPointer++] = value;
  return GLC_OK;
}

int glacierStackTop(GlacierStack *stack, GlacierValue *value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  *value = stack->data[headPointer];
  return GLC_OK;
}

int glacierStackPop(GlacierStack *stack, GlacierValue *value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  if (value)
    glacierStackTop(stack, value);
  --stack->stackPointer;
  return GLC_OK;
}

void glacierCallStackInit(GlacierCallStack *stack) {
  stack->stackPointer = 0;
  for (int i = 0; i < MAX_STACK_SIZE; ++i)
    glacierCallStackFrameInit(&stack->frames[i], -1);
}

int glacierCallStackPush(GlacierCallStack *stack, int bcOffset) {
  if (!glacierStackIsValidPointer(stack->stackPointer))
    return GLC_STACK_OVERFLOW;
  glacierCallStackFrameInit(&stack->frames[stack->stackPointer], bcOffset);
  stack->stackPointer++;
  return GLC_OK;
}

int glacierCallStackPop(GlacierCallStack *stack) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  --stack->stackPointer;
  return GLC_OK;
}

int glacierCallStackGet(GlacierCallStack *stack, int id, int *value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  GlacierCallStackFrame *frame = &stack->frames[headPointer];
  if (id < 0 || id >= MAX_FRAME_BINDINGS)
    return GLC_OUT_OF_BUFFER;
  int temp = frame->bindings[id];
  if (temp == -1)
    return GLC_ERROR;
  *value = temp;
  return GLC_OK;
}

int glacierCallStackGetByteCodeOffset(GlacierCallStack *stack, int *bcOffset) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  GlacierCallStackFrame *frame = &stack->frames[headPointer];
  *bcOffset = frame->bcOffset;
  return GLC_OK;
}

int glacierCallStackSet(GlacierCallStack *stack, int id, int value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  GlacierCallStackFrame *frame = &stack->frames[headPointer];
  if (id < 0 || id >= MAX_FRAME_BINDINGS)
    return GLC_OUT_OF_BUFFER;
  frame->bindings[id] = value;
  return GLC_OK;
}

void glacierCallStackFrameInit(GlacierCallStackFrame *frame, int bcOffset) {
  frame->bcOffset = bcOffset;
  frame->numBindings = 0;
  for (int i = 0; i < MAX_FRAME_BINDINGS; ++i)
    frame->bindings[i] = -1;
}
