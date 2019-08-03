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

int glacierStackTop(GlacierStack *stack, int *val) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return GLC_STACK_OVERFLOW;
  *val = stack->data[headPointer].value;
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
