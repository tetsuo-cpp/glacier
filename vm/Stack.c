#include "Stack.h"

#include <stdbool.h>

static inline bool glacierStackIsValidPointer(int pointer) {
  return (pointer >= 0 && pointer < MAX_STACK_SIZE);
}

void glacierStackInit(GlacierStack *stack) { stack->stackPointer = 0; }

int glacierStackPush(GlacierStack *stack, int value) {
  if (!glacierStackIsValidPointer(stack->stackPointer))
    return -1;
  stack->data[stack->stackPointer++].value = value;
  return 0;
}

int glacierStackTop(GlacierStack *stack, int *val) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return -1;
  *val = stack->data[headPointer].value;
  return 0;
}

int glacierStackPop(GlacierStack *stack, int *value) {
  int headPointer = stack->stackPointer - 1;
  if (!glacierStackIsValidPointer(headPointer))
    return -1;
  if (value)
    glacierStackTop(stack, value);
  --stack->stackPointer;
  return 0;
}
