#ifndef GLACIERVM_STACK_H
#define GLACIERVM_STACK_H

#define MAX_STACK_SIZE 1024

// Maybe make this a union and type pun for other types.
typedef struct {
  int value;
} GlacierStackFrame;

typedef struct {
  GlacierStackFrame data[MAX_STACK_SIZE];
  int stackPointer;
} GlacierStack;

void glacierStackInit(GlacierStack *stack);
int glacierStackPush(GlacierStack *stack, int value);
int glacierStackTop(GlacierStack *stack, int *value);
int glacierStackPop(GlacierStack *stack, int *value);

#endif // GLACIERVM_STACK_H
