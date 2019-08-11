#include "Stack.h"

#include "Util.h"

#include <stdbool.h>

static inline bool glacierStackIsValidPointer(int pointer) {
  return pointer >= 0 && pointer < MAX_STACK_SIZE;
}

void glacierStackInit(GlacierStack *stack) { stack->stackPointer = 0; }

int glacierStackPush(GlacierStack *stack, int value) {
  if (!glacierStackIsValidPointer(stack->stackPointer))
    return GLC_STACK_OVERFLOW;
  stack->data[stack->stackPointer++].value = value;
  return GLC_OK;
}

int glacierStackTop(GlacierStack *stack, int *value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  *value = stack->data[headPointer].value;
  return GLC_OK;
}

int glacierStackPop(GlacierStack *stack, int *value) {
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
  GlacierCallStackFrame *frame = &stack->frames[stack->stackPointer - 1];
  if (id < 0 || id >= MAX_FRAME_BINDINGS)
    return GLC_OUT_OF_BUFFER;
  int temp = frame->bindings[id];
  if (temp == -1)
    return GLC_ERROR;
  *value = temp;
  return GLC_OK;
}

int glacierCallStackGetByteCodeOffset(GlacierCallStack *stack, int *bcOffset) {
  GlacierCallStackFrame *frame = &stack->frames[stack->stackPointer - 1];
  *bcOffset = frame->bcOffset;
  return GLC_OK;
}

int glacierCallStackSet(GlacierCallStack *stack, int id, int value) {
  GlacierCallStackFrame *frame = &stack->frames[stack->stackPointer - 1];
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
