#include "Stack.h"

void glacierStackInit(GlacierStack *stack) { stack->stackPointer = 0; }

int glacierStackPush(GlacierStack *stack, int value) {
  if (stack->stackPointer >= MAX_STACK_SIZE)
    return -1;
  stack->data[stack->stackPointer++].value = value;
  return 0;
}

int glacierStackTop(GlacierStack *stack, int *val) {
  if (stack->stackPointer - 1 < 0)
    return -1;
  *val = stack->data[stack->stackPointer - 1].value;
  return 0;
}

int glacierStackPop(GlacierStack *stack, int *value) {
  if (stack->stackPointer - 1 < 0)
    return -1;
  if (value)
    glacierStackTop(stack, value);
  --stack->stackPointer;
  return 0;
}
